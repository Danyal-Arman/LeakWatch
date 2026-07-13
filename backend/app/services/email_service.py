import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_security_email(name, email, report):

    subject = "⚠️ Security Alert - Weak Password Detected"

    html = f"""
    <html>
    <body style="font-family:Arial">

        <h2>Security Alert</h2>

        <p>Hello <b>{name}</b>,</p>

        <p>
        Our AI-powered monitoring system detected that your account password
        is considered <b>{report['severity'].upper()}</b> risk on platform EduGlide.
        </p>

        <h3>Rule Analysis</h3>

        <ul>
            <li><b>Score:</b> {report['score']}</li>
            <li><b>Severity:</b> {report['severity']}</li>
        </ul>

        <h3>AI Analysis</h3>

        <ul>
            <li><b>Confidence:</b> {report['ai']['confidence']}%</li>
            <li><b>Reason:</b> {report['ai']['reason']}</li>
        </ul>

        <p>
        We strongly recommend changing your password immediately on platform EduGlide.
        </p>

        <br>

        <p>
        Regards,<br>
        AI Security Monitoring System
        </p>

    </body>
    </html>
    """

    msg = MIMEMultipart()

    msg["From"] = EMAIL_FROM
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(html, "html"))

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)

    server.starttls()

    server.login(SMTP_USER, SMTP_PASS)

    server.sendmail(
        EMAIL_FROM,
        email,
        msg.as_string()
    )

    server.quit()