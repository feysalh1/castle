"""
Email service for Children's Castle application.
This module provides email sending functionality using SendGrid.
"""

import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
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
    Send an email using SendGrid

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_content (str): HTML content of the email
        from_email (str, optional): Sender email address. Defaults to system default.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sender_email = from_email or os.getenv('SENDER_EMAIL', 'noreply@childrenscastle.app')

        message = Mail(
            from_email=sender_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )

        response = sg.send(message)
        if response.status_code in [200, 201, 202]:
            logger.info(f"Email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"Failed to send email. Status code: {response.status_code}")
            return False

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