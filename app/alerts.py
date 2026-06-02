import smtplib, httpx, logging
from email.message import EmailMessage
from app.config import settings

log = logging.getLogger("alerts")

async def dispatch_alert(site, entry, status: str):
    msg = (f"[{status}] {site.name} ({site.url})\n"
           f"Status code: {entry.status_code}\n"
           f"Response: {entry.response_time_ms:.0f} ms\n"
           f"Error: {entry.error or '-'}")
    await _slack(msg)
    await _telegram(msg)
    _email(f"{status}: {site.name}", msg)

async def _slack(text):
    if not settings.slack_webhook_url: return
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            await c.post(settings.slack_webhook_url, json={"text": text})
    except Exception as e: log.warning("slack: %s", e)

async def _telegram(text):
    if not settings.telegram_bot_token: return
    url = f"[api.telegram.org](https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage)"
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            await c.post(url, json={"chat_id": settings.telegram_chat_id, "text": text})
    except Exception as e: log.warning("telegram: %s", e)

def _email(subject, body):
    if not settings.smtp_host or not settings.alert_email_to: return
    em = EmailMessage()
    em["From"] = settings.smtp_user
    em["To"] = settings.alert_email_to
    em["Subject"] = subject
    em.set_content(body)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as s:
            s.starttls()
            s.login(settings.smtp_user, settings.smtp_pass)
            s.send_message(em)
    except Exception as e: log.warning("email: %s", e)
