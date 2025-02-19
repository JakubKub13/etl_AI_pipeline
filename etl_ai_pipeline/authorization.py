from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .settings import settings

class BearerAuthenticator:
    """
    Class to handle Bearer token authentication.
    """
    
    def __init__(self):
        self.security = HTTPBearer()
    
    async def __call__(
        self, 
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> str:
        """
        Verify Bearer token against environment variable API key.
        
        Args:
            credentials (HTTPAuthorizationCredentials): The Bearer token credentials
            
        Returns:
            str: The verified token
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            token = credentials.credentials
            if token != settings.API_KEY:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return token
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
