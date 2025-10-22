from celery import shared_task
from celery import shared_task
from .models import AutomationRule, TaskLog
from .instagram_service import InstagramService
from .ai_service import AIService
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
    ai_service = AIService() if AutomationRule.objects.filter(use_ai_reply=True, is_active=True).exists() else None

    for rule in active_rules:
        try:
            account = rule.post.account
            service = InstagramService(proxy=account.proxy)
            service.login_with_session(json.loads(account.session_data))

            comments = service.cl.media_comments(rule.post.post_id)
            keywords = [k.strip().lower() for k in rule.keywords.split(',')]

            for comment in comments:
                if TaskLog.objects.filter(replied_comment_id=comment.pk).exists():
                    continue

                if any(keyword in comment.text.lower() for keyword in keywords):
                    comment_reply = rule.comment_reply_text
                    direct_reply = rule.direct_reply_text

                    if rule.use_ai_reply and ai_service:
                        ai_generated_reply = ai_service.generate_smart_reply(comment.text)
                        comment_reply = ai_generated_reply
                        direct_reply = ai_generated_reply

                    if rule.send_comment and comment_reply:
                        service.send_comment(rule.post.post_id, comment_reply)
                        TaskLog.objects.create(rule=rule, description=f"Responded to comment {comment.pk} with a comment: '{comment_reply}'", replied_comment_id=comment.pk, is_success=True)
                        time.sleep(random.randint(15, 45))

                    if rule.send_direct and direct_reply:
                        # As noted before, this part has limitations.
                        # For now, we log the attempt.
                        TaskLog.objects.create(rule=rule, description=f"DM to {comment.user.username} for comment {comment.pk} not sent (feature not fully implemented). Reply would have been: '{direct_reply}'", replied_comment_id=comment.pk, is_success=False)
                        time.sleep(random.randint(15, 45))

        except Exception as e:
            TaskLog.objects.create(rule=rule, description=f"Error processing rule: {str(e)}", is_success=False)