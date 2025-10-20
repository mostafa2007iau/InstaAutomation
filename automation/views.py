from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import InstagramAccount, MonitoredPost, AutomationRule, TaskLog
from .serializers import (
    UserSerializer,
    InstagramAccountSerializer,
    MonitoredPostSerializer,
    AutomationRuleSerializer,
    TaskLogSerializer,
)
from .instagram_service import InstagramService
import json

# English: API view for user registration.
# Persian: این ویو، اندپوینت API برای ثبت‌نام کاربران را فراهم می‌کند.
class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# English: API view for adding a new Instagram account.
# Persian: این ویو، اندپوینت API برای افزودن یک اکانت جدید اینستاگرام را فراهم می‌کند.
class InstagramLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        proxy = request.data.get('proxy')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        service = InstagramService(proxy=proxy)
        try:
            session_data = service.login(username, password)
            account, created = InstagramAccount.objects.update_or_create(
                username=username,
                user=request.user,
                defaults={'session_data': json.dumps(session_data), 'proxy': proxy}
            )
            return Response(InstagramAccountSerializer(account).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InstagramSessionLoginView(APIView):
    def post(self, request):
        sessionid = request.data.get('sessionid')
        csrftoken = request.data.get('csrftoken')
        user_id = request.data.get('user_id')
        proxy = request.data.get('proxy')

        if not all([sessionid, csrftoken, user_id]):
            return Response({'error': 'sessionid, csrftoken, and user_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        session_data = {
            "uuids": {}, "mid": "", "ig_u_rur": "", "ig_www_claim": "", "authorization_data": {},
            "cookies": { "csrftoken": csrftoken, "sessionid": sessionid, "ds_user_id": user_id },
            "last_login": None, "device_settings": {}, "user_agent": "", "country": "US",
            "country_code": 1, "locale": "en_US", "timezone_offset": 0
        }

        service = InstagramService(proxy=proxy)
        try:
            username = service.login_with_session(session_data)
            account, created = InstagramAccount.objects.update_or_create(
                username=username,
                user=request.user,
                defaults={'session_data': json.dumps(session_data), 'proxy': proxy}
            )
            return Response(InstagramAccountSerializer(account).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f"Login failed. Please check your session details. Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)


# English: ViewSet for managing connected Instagram accounts.
# Persian: این ویو، مجموعه‌ای از اندپوینت‌های API برای مدیریت اکانت‌های اینستاگرام متصل شده را فراهم می‌کند.
class InstagramAccountViewSet(viewsets.ModelViewSet):
    serializer_class = InstagramAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.instagram_accounts.all()


# English: API view to fetch the user's Instagram posts for a specific account.
# Persian: این ویو، اندپوینت API برای دریافت پست‌های اینستاگرام کاربر برای یک اکانت مشخص را فراهم می‌کند.
class InstagramPostsView(APIView):
    def get(self, request):
        account_id = request.query_params.get('account_id')
        if not account_id:
            return Response({'error': 'account_id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = InstagramAccount.objects.get(pk=account_id, user=request.user)
            service = InstagramService(proxy=account.proxy)
            service.login_with_session(json.loads(account.session_data))
            user_id = service.cl.user_id_from_username(account.username)
            posts = service.get_user_posts(user_id)

            post_data = [{'pk': p.pk, 'code': p.code, 'thumbnail_url': p.thumbnail_url, 'caption_text': p.caption_text} for p in posts]

            return Response(post_data)
        except InstagramAccount.DoesNotExist:
            return Response({'error': 'Instagram account not found or you do not have permission.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# English: ViewSet for managing automation rules (CRUD operations).
# Persian: این ویو، مجموعه‌ای از اندپوینت‌های API برای مدیریت قوانین (ایجاد، خواندن، ویرایش، حذف) را فراهم می‌کند.
class AutomationRuleViewSet(viewsets.ModelViewSet):
    serializer_class = AutomationRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        English: Restricts the returned rules to the current user.
                 Can be filtered by `post_id` query parameter.
        Persian: قوانین نمایش داده شده را به کاربر فعلی محدود می‌کند.
                 قابلیت فیلتر بر اساس پارامتر `post_id` در URL وجود دارد.
        """
        queryset = AutomationRule.objects.filter(post__account__user=self.request.user)
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post__post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        """
        English: Automatically creates a MonitoredPost if it doesn't exist for the user.
        Persian: به صورت خودکار یک `MonitoredPost` ایجاد می‌کند اگر برای کاربر وجود نداشته باشد.
        """
        post_pk = self.request.data.get('post_pk')
        post_url = self.request.data.get('post_url')

        if not post_pk:
            raise permissions.PermissionDenied("Post ID (post_pk) is required.")

        try:
            account = InstagramAccount.objects.get(user=self.request.user)
        except InstagramAccount.DoesNotExist:
            raise permissions.PermissionDenied("User does not have a linked Instagram account.")

        monitored_post, created = MonitoredPost.objects.get_or_create(
            post_id=post_pk,
            account=account,
            defaults={'post_url': post_url or f"https://www.instagram.com/p/{post_pk}/"}
        )

        serializer.save(post=monitored_post)


# English: Read-only ViewSet for viewing task logs.
# Persian: این ویو، اندپوینت API فقط-خواندنی برای مشاهده گزارش‌های عملکرد را فراهم می‌کند.
class TaskLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        English: Restricts the returned logs to the current user's rules.
        Persian: گزارش‌های نمایش داده شده را به قوانینی که متعلق به کاربر فعلی است محدود می‌کند.
        """
        user_accounts = InstagramAccount.objects.filter(user=self.request.user)
        user_posts = MonitoredPost.objects.filter(account__in=user_accounts)
        user_rules = AutomationRule.objects.filter(post__in=user_posts)
        return TaskLog.objects.filter(rule__in=user_rules)