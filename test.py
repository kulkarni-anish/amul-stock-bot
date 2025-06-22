import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
TO_EMAIL = os.environ.get('TO_EMAIL')

msg = MIMEText('This is a test email from your Amul bot script.')
msg['Subject'] = 'Test Email'
msg['From'] = EMAIL
msg['To'] = TO_EMAIL

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

print("Test email sent!")