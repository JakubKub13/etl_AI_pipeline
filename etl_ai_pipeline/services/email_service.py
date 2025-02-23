import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import List, Optional
from pydantic import EmailStr
from ..settings import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending email notifications."""
    
    def __init__(self):
        """Initialize email service with configuration."""
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.SENDER_EMAIL

    async def send_analysis_report(
        self,
        recipient_email: EmailStr,
        subject: str,
        report_content: str,
        cc: Optional[List[EmailStr]] = None
    ) -> bool:
        """
        Send analysis report via email.
        
        Args:
            recipient_email (EmailStr): Recipient email address
            subject (str): Email subject
            report_content (str): Report content in HTML format
            cc (Optional[List[EmailStr]]): CC recipients
            
        Returns:
            bool: True if email was sent successfully
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ", ".join(cc)
            
            msg.attach(MIMEText(report_content, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Analysis report sent to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise