from fastapi import BackgroundTasks
from app.config.settings import get_settings
from app.models.user import User
from app.config.email import send_email
from app.utils.context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from app.auth.utils import get_hash_password

settings = get_settings()


async def send_email_with_template(user: User, subject: str, template_name: str, template_data: dict, background_tasks: BackgroundTasks):
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        **template_data
    }
    await send_email(
        subject=subject,
        recipients=[user.email],
        template_name=template_name,
        template_body=data,
        background_tasks=background_tasks
    )


async def send_account_verification_email(user: User, background_tasks: BackgroundTasks):
    token = get_hash_password(user.get_context(context=USER_VERIFY_ACCOUNT))
    activate_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"
    subject = f"Account Verification - {settings.APP_NAME}"
    template_data = {'activate_url': activate_url}
    
    await send_email_with_template(
        user=user,
        subject=subject,
        template_name="account-verification.html",
        template_data=template_data,
        background_tasks=background_tasks
    )


async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    subject = f"Welcome - {settings.APP_NAME}"
    template_data = {'login_url': f'{settings.FRONTEND_HOST}'}
    
    await send_email_with_template(
        user=user,
        subject=subject,
        template_name="account-verification-confirmation.html",
        template_data=template_data,
        background_tasks=background_tasks
    )


async def send_password_reset_email(user: User, background_tasks: BackgroundTasks):
    token = get_hash_password(user.get_context(FORGOT_PASSWORD))
    reset_url = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
    subject = f"Reset Password - {settings.APP_NAME}"
    template_data = {'activate_url': reset_url}
    
    await send_email_with_template(
        user=user,
        subject=subject,
        template_name="password-reset.html",
        template_data=template_data,
        background_tasks=background_tasks
    )
