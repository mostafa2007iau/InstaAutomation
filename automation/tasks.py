from celery import shared_task
from .models import AutomationRule, TaskLog
from .instagram_service import InstagramService
import json
import time
import random

# English: A Celery shared task to process all active automation rules.
#          This task runs periodically in the background.
# Persian: این یک تسک پس‌زمینه Celery برای پردازش تمام قوانین فعال اتوماسیون است.
#          این تسک به صورت دوره‌ای در پس‌زمینه اجرا می‌شود.
@shared_task
def process_automation_rules():
    """
    English: Fetches all active automation rules and processes them one by one.
    Persian: تمام قوانین فعال اتوماسیون را دریافت کرده و آن‌ها را یک به یک پردازش می‌کند.
    """
    active_rules = AutomationRule.objects.filter(is_active=True)

    for rule in active_rules:
        try:
            account = rule.post.account
            service = InstagramService()
            # English: Log in to Instagram using the stored session data.
            # Persian: با استفاده از اطلاعات نشست ذخیره شده، به اینستاگرام وارد می‌شود.
            service.login_with_session(json.loads(account.session_data))

            # English: Fetch recent comments for the monitored post.
            # Persian: کامنت‌های اخیر پست مانیتور شده را دریافت می‌کند.
            comments = service.cl.media_comments(rule.post.post_id)

            keywords = [k.strip().lower() for k in rule.keywords.split(',')]

            for comment in comments:
                # English: Check if we have already replied to this comment to avoid spam.
                # Persian: بررسی می‌کند که آیا قبلا به این کامنت پاسخ داده‌ایم تا از اسپم جلوگیری شود.
                if TaskLog.objects.filter(replied_comment_id=comment.pk).exists():
                    continue

                # English: Check if any keyword exists in the comment text.
                # Persian: بررسی می‌کند که آیا هیچ یک از کلمات کلیدی در متن کامنت وجود دارد یا خیر.
                if any(keyword in comment.text.lower() for keyword in keywords):
                    if rule.reply_type == 'comment':
                        service.send_comment(rule.post.post_id, rule.reply_text)
                        TaskLog.objects.create(rule=rule, description=f"Responded to comment {comment.pk} with a comment.", replied_comment_id=comment.pk, is_success=True)
                    elif rule.reply_type == 'direct':
                        # NOTE (English): The ability to send a direct message in response to a comment is not fully implemented.
                        # The instagrapi library requires the user's Instagram primary key (PK) to send a DM.
                        # While comment objects contain user information, they do not reliably provide the user's PK.
                        # A more advanced implementation might involve additional lookups or a different approach to get the user's PK.
                        # For now, we log that the DM was not sent.
                        #
                        # نکته (فارسی): قابلیت ارسال دایرکت در پاسخ به کامنت به طور کامل پیاده‌سازی نشده است.
                        # کتابخانه instagrapi برای ارسال دایرکت به شناسه‌ی اصلی کاربر در اینستاگرام (PK) نیاز دارد.
                        # اگرچه اطلاعات کاربر در آبجکت کامنت وجود دارد، اما PK کاربر به طور قابل اتکا در دسترس نیست.
                        # برای پیاده‌سازی کامل این قابلیت، به روش‌های پیشرفته‌تری نیاز است.
                        # در حال حاضر، فقط یک گزارش مبنی بر عدم ارسال دایرکت ثبت می‌شود.
                        TaskLog.objects.create(rule=rule, description=f"DM to {comment.user.username} for comment {comment.pk} not sent (feature not fully implemented).", replied_comment_id=comment.pk, is_success=False)

                    # English: Add a random delay to respect Instagram's rate limits and appear more human.
                    # Persian: یک تاخیر تصادفی برای رعایت محدودیت‌های اینستاگرام و شبیه‌سازی رفتار انسانی اضافه می‌شود.
                    time.sleep(random.randint(30, 120))

        except Exception as e:
            TaskLog.objects.create(rule=rule, description=f"Error processing rule: {str(e)}", is_success=False)