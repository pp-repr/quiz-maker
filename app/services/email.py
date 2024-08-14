from fastapi import BackgroundTasks
from app.config.settings import get_settings
from app.models.user import User
from app.config.email import send_email
from app.utils.context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from app.config.security import get_hash_password

settings = get_settings()


async def send_account_verification_email(user: User, background_tasks: BackgroundTasks):
    string_context = user.get_context(context=USER_VERIFY_ACCOUNT)
    token = get_hash_password(string_context)
    activate_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'activate_url': activate_url
    }
    subject = f"Account Verification - {settings.APP_NAME}"
    await send_email(
        subject=subject,
        recipients=[user.email],
        template_body=data,
        template_name="account-verification.html",
        background_tasks=background_tasks
    )
    
    
async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        subject=subject,
        recipients=[user.email],
        template_body=data,
        template_name="account-verification-confirmation.html",
        background_tasks=background_tasks
    )
