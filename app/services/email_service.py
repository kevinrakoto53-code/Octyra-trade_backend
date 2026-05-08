import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


async def send_trade_alert(
    to_email: str,
    asset: str,
    action: str,
    price: float,
    bot_name: str
) -> bool:
    subject = f"OCTYRA Alert — {action} {asset}"

    html = f"""
    <html>
    <body style="font-family: Arial; background: #0a0a0a; color: #ffffff; padding: 20px;">
        <h2 style="color: #f97316;">OCTYRA Trading Alert 🐙</h2>
        <p>Ton bot <strong>{bot_name}</strong> vient d'exécuter un trade !</p>
        <table style="border-collapse: collapse; width: 100%;">
            <tr>
                <td style="padding: 8px; color: #f97316;">Asset</td>
                <td style="padding: 8px;">{asset}</td>
            </tr>
            <tr>
                <td style="padding: 8px; color: #f97316;">Action</td>
                <td style="padding: 8px;">{action}</td>
            </tr>
            <tr>
                <td style="padding: 8px; color: #f97316;">Prix</td>
                <td style="padding: 8px;">${price}</td>
            </tr>
        </table>
        <p style="color: #888; font-size: 12px;">OCTYRA — Intelligent Trading powered by AI</p>
    </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.SMTP_USER
    message["To"] = to_email
    message.attach(MIMEText(html, "html"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        return True
    except Exception as e:
        print(f"Erreur email: {e}")
        return False