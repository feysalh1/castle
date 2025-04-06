"""
Email service for Children's Castle application.
This module provides email sending functionality.
"""

import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template_string

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default templates
PASSWORD_RESET_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Password Reset - Children's Castle</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header h1 {
            color: #4a6da7;
        }
        .content {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
        }
        .button {
            display: inline-block;
            background-color: #4a6da7;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #777;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Children's Castle</h1>
    </div>
    <div class="content">
        <p>Hello {{ username }},</p>
        <p>We received a request to reset your password for your Children's Castle account.</p>
        <p>To reset your password, please click the button below:</p>
        <div style="text-align: center;">
            <a href="{{ reset_url }}" class="button">Reset Password</a>
        </div>
        <p>If you didn't request a password reset, you can safely ignore this email.</p>
        <p>This link will expire in {{ expire_time }} hour(s).</p>
        <p>Thank you,<br>Children's Castle Team</p>
    </div>
    <div class="footer">
        <p>This is an automated message, please do not reply.</p>
    </div>
</body>
</html>
"""

def send_email(to_email, subject, html_content, from_email=None):
    """
    Send an email using the default Python smtplib
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_content (str): HTML content of the email
        from_email (str, optional): Sender email address. Defaults to system default.
        
    Returns:
        bool: True if successful, False otherwise
    """
    # SMTP server configuration
    smtp_server = os.environ.get('SMTP_SERVER', 'localhost')
    smtp_port = int(os.environ.get('SMTP_PORT', 25))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    sender_email = from_email or os.environ.get('SENDER_EMAIL', 'noreply@childrenscastle.app')
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        
        # Use TLS if available
        if smtp_username and smtp_password:
            server.starttls()
            server.login(smtp_username, smtp_password)
        
        # Send email
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

def send_password_reset_email(user, token, reset_url):
    """
    Send a password reset email to a user
    
    Args:
        user: User model object with username and email
        token (str): Password reset token
        reset_url (str): Complete URL for password reset
        
    Returns:
        bool: True if successful, False otherwise
    """
    subject = "Children's Castle - Password Reset Request"
    
    # Render the password reset template
    html_content = render_template_string(
        PASSWORD_RESET_TEMPLATE,
        username=user.username,
        reset_url=reset_url,
        expire_time=1  # Token expiration time in hours
    )
    
    return send_email(user.email, subject, html_content)

def get_mock_email_content(to_email, subject, html_content):
    """
    Get mock email content for development and testing
    This is a fallback when SMTP is not configured
    
    Args:
        to_email (str): Recipient email
        subject (str): Email subject
        html_content (str): HTML content
        
    Returns:
        str: Formatted email content
    """
    return f"""
    To: {to_email}
    Subject: {subject}
    Content-Type: text/html
    
    {html_content}
    """