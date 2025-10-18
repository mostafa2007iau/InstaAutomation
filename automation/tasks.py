from celery import shared_task
from .models import AutomationRule, TaskLog, MonitoredPost, InstagramAccount
from .instagram_service import InstagramService
import json
import time
import random

@shared_task
def process_automation_rules():
    """
    This task fetches all active automation rules and processes them.
    """
    active_rules = AutomationRule.objects.filter(is_active=True)

    for rule in active_rules:
        try:
            account = rule.post.account
            service = InstagramService()
            service.login_with_session(json.loads(account.session_data))

            # To avoid checking too often, we can store the last checked timestamp
            # For now, we'll just fetch recent comments
            comments = service.cl.media_comments(rule.post.post_id)

            keywords = [k.strip().lower() for k in rule.keywords.split(',')]

            for comment in comments:
                # Check if we have already replied to this comment
                if TaskLog.objects.filter(replied_comment_id=comment.pk).exists():
                    continue

                if any(keyword in comment.text.lower() for keyword in keywords):
                    if rule.reply_type == 'comment':
                        service.send_comment(rule.post.post_id, rule.reply_text)
                        TaskLog.objects.create(rule=rule, description=f"Responded to comment {comment.pk} with a comment.", replied_comment_id=comment.pk, is_success=True)
                    elif rule.reply_type == 'direct':
                        # NOTE: The ability to send a direct message in response to a comment is not fully implemented.
                        # The instagrapi library requires the user's Instagram primary key (PK) to send a DM.
                        # While comment objects contain user information, they do not reliably provide the user's PK.
                        # A more advanced implementation might involve additional lookups or a different approach to get the user's PK.
                        # For now, we log that the DM was not sent.
                        TaskLog.objects.create(rule=rule, description=f"DM to {comment.user.username} for comment {comment.pk} not sent (feature not fully implemented).", replied_comment_id=comment.pk, is_success=False)

                    # Respect Instagram's rate limits
                    time.sleep(random.randint(30, 120))

        except Exception as e:
            TaskLog.objects.create(rule=rule, description=f"Error processing rule: {str(e)}", is_success=False)