from django.db import models
from django.contrib.auth.models import User

# English: Represents a user's linked Instagram account.
# Persian: این مدل، اکانت اینستاگرام متصل شده یک کاربر را نمایندگی می‌کند.
class InstagramAccount(models.Model):
    # English: The user in our system.
    # Persian: کاربر موجود در سیستم ما.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instagram_accounts')
    # English: The Instagram username.
    # Persian: نام کاربری اینستاگرام.
    username = models.CharField(max_length=255, unique=True)
    # English: Stores the JSON data of the instagrapi session.
    # Persian: داده‌های مربوط به نشست (session) در کتابخانه instagrapi را به صورت JSON ذخیره می‌کند.
    session_data = models.TextField()
    # English: Optional proxy URL for this account's requests.
    # Persian: آدرس پراکسی اختیاری برای درخواست‌های این اکانت.
    proxy = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., http://user:pass@host:port")

    def __str__(self):
        return self.username

# English: Represents an Instagram post that is being monitored for comments.
# Persian: این مدل، یک پست اینستاگرام که برای کامنت‌ها مانیتور می‌شود را نمایندگی می‌کند.
class MonitoredPost(models.Model):
    # English: The Instagram account that owns this post.
    # Persian: اکانت اینستاگرامی که این پست به آن تعلق دارد.
    account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    # English: The unique ID of the Instagram post.
    # Persian: شناسه‌ی منحصر به فرد پست در اینستاگرام.
    post_id = models.CharField(max_length=255, unique=True)
    # English: The URL of the post for easy access.
    # Persian: آدرس URL پست برای دسترسی آسان.
    post_url = models.URLField()

    def __str__(self):
        return self.post_url

# English: Defines a rule for automated replies.
# Persian: این مدل، یک قانون برای پاسخ‌دهی خودکار را تعریف می‌کند.
class AutomationRule(models.Model):
    # English: The post to which this rule applies.
    # Persian: پستی که این قانون برای آن اعمال می‌شود.
    post = models.ForeignKey(MonitoredPost, on_delete=models.CASCADE, related_name='rules')
    # English: Comma-separated keywords that trigger the automation.
    # Persian: کلمات کلیدی که با کاما از هم جدا شده‌اند و باعث فعال شدن ربات می‌شوند.
    keywords = models.TextField(help_text="Comma-separated keywords")

    # English: Flags to enable different reply types.
    # Persian: فلگ‌هایی برای فعال‌سازی انواع مختلف پاسخ.
    send_comment = models.BooleanField(default=False)
    send_direct = models.BooleanField(default=False)

    # English: The text to be sent as a comment reply. Can be blank.
    # Persian: متنی که به عنوان پاسخ کامنت ارسال می‌شود. می‌تواند خالی باشد.
    comment_reply_text = models.TextField(blank=True)
    # English: The text to be sent as a direct message. Can be blank.
    # Persian: متنی که به عنوان دایرکت ارسال می‌شود. می‌تواند خالی باشد.
    direct_reply_text = models.TextField(blank=True)

    # English: Flag to enable AI-generated replies.
    # Persian: فلگی برای فعال‌سازی پاسخ‌های تولید شده توسط هوش مصنوعی.
    use_ai_reply = models.BooleanField(default=False)

    # English: Whether the rule is currently active.
    # Persian: مشخص می‌کند که آیا این قانون در حال حاضر فعال است یا خیر.
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rule for {self.post.post_url}"

# English: Logs the actions performed by the automation tasks.
# Persian: این مدل، گزارش اقدامات انجام شده توسط تسک‌های خودکار را ثبت می‌کند.
class TaskLog(models.Model):
    # English: The rule that triggered this log entry.
    # Persian: قانونی که این گزارش به آن مرتبط است.
    rule = models.ForeignKey(AutomationRule, on_delete=models.SET_NULL, null=True)
    # English: The timestamp of the log entry.
    # Persian: زمان ثبت گزارش.
    timestamp = models.DateTimeField(auto_now_add=True)
    # English: A description of the action taken.
    # Persian: توضیحی در مورد اقدام انجام شده.
    description = models.TextField()
    # English: Whether the action was successful.
    # Persian: مشخص می‌کند که آیا اقدام موفقیت‌آمیز بوده است یا خیر.
    is_success = models.BooleanField(default=True)
    # English: The ID of the comment that was replied to, to prevent duplicate replies.
    # Persian: شناسه‌ی کامنتی که به آن پاسخ داده شده است، برای جلوگیری از پاسخ‌های تکراری.
    replied_comment_id = models.CharField(max_length=255, null=True, blank=True, help_text="The ID of the comment that was replied to.")

    def __str__(self):
        return f"Log at {self.timestamp}"