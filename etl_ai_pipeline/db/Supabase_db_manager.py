import asyncio
import logging
from typing import Optional, Dict, Any, List
import os
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial

from ..settings import settings
from dotenv import load_dotenv
from supabase.client import Client, create_client
from supabase.lib.client_options import ClientOptions
from postgrest import APIResponse
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class User:
    """User model representing the database structure."""
    id: str
    email: str
    name: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class SupabaseDBManager:
    """Manager for Supabase database operations."""

    def __init__(self, max_connections: int = 10):
        """
        Initialize the database manager with connection pooling.
        
        Args:
            max_connections: Maximum number of concurrent database connections
        """
        load_dotenv()
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_SERVICE_KEY
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing Supabase credentials in environment variables")
        
        # Initialize connection pool
        self.pool = ThreadPoolExecutor(max_workers=max_connections)
        
        # Configure client options for better performance
        self.client_options = ClientOptions(
            schema="public",
            headers={"X-Client-Info": "supabase-py/production"},
            postgrest_client_timeout=30
        )
        
        # Initialize the client
        try:
            self.client: Client = create_client(
                self.supabase_url, 
                self.supabase_key,
                options=self.client_options
            )
            logger.info("Successfully initialized Supabase client")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_user(self, email: str, name: str, metadata: Optional[Dict[str, Any]] = None) -> User:
        """
        Asynchronously create a new user in the database with retry logic.
        
        Args:
            email: User's email address
            name: User's name
            metadata: Optional additional user data
            
        Returns:
            User object
            
        Raises:
            DatabaseError: If user creation fails
        """
        try:
            data = {
                "email": email,
                "name": name,
                "metadata": metadata,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Execute in thread pool to prevent blocking
            result = await asyncio.get_event_loop().run_in_executor(
                self.pool,
                lambda: self.client.table("users").insert(data).execute()
            )
            
            if not result.data:
                raise DatabaseError("No data returned from user creation")
                
            user_data = result.data[0]
            print('User datasssss: ', user_data)
            logger.info(f"Successfully created user with ID: {user_data['id']}")
            
            return User(
                id=user_data["id"],
                email=user_data["email"],
                name=user_data["name"],
                created_at=datetime.fromisoformat(user_data["created_at"]),
                metadata=user_data.get("metadata")
            )
            
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise DatabaseError(f"User creation failed: {str(e)}")
    
    def close(self):
        """
        Close the database connection pool
        """
        try:
            if hasattr(self, 'pool'):
                self.pool.shutdown(wait=True)
            logger.info("Databázové spojenia úspešne uzavreté")
        except Exception as e:
            logger.error(f"Chyba pri zatváraní databázových spojení: {e}")



async def main():
    """Test the implementation with async operations."""
    db_manager = SupabaseDBManager()
    print("Supabase DB Manager initialized")
    
    try:
        # Test user creation
        test_user = await db_manager.create_user(
            email="test4@example.com",
            name="Test User3",
            metadata={"role": "test"}
        )
        print(f"Created user: {test_user}")
        
    #     # Test batch user creation
    #     test_users = await asyncio.gather(*[
    #         db_manager.create_user(
    #             email=f"test{i}@example.com",
    #             name=f"Test User {i}",
    #             metadata={"role": "test"}
    #         )
    #         for i in range(3)
    #     ])
    #     print(f"Created batch users: {test_users}")
        
    #     # Test batch user retrieval
    #     user_ids = [user.id for user in test_users]
    #     retrieved_users = await db_manager.get_users_batch(user_ids)
    #     print(f"Retrieved users: {retrieved_users}")
        
    #     # Test batch user deletion
    #     deletion_results = await db_manager.delete_users_batch(user_ids)
    #     print(f"Deletion results: {deletion_results}")
        
    except Exception as e:
        logger.error(f"Error during testing: {e}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())