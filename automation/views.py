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

# English: API view for logging into an Instagram account.
# Persian: این ویو، اندپوینت API برای ورود به اکانت اینستاگرام را فراهم می‌کند.
class InstagramLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        service = InstagramService()
        try:
            session_data = service.login(username, password)
            account, created = InstagramAccount.objects.update_or_create(
                user=request.user,
                defaults={'username': username, 'session_data': json.dumps(session_data)}
            )
            return Response({'status': 'success', 'account_id': account.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# English: API view to fetch the user's Instagram posts.
# Persian: این ویو، اندپوینت API برای دریافت پست‌های اینستاگرام کاربر را فراهم می‌کند.
class InstagramPostsView(APIView):
    def get(self, request):
        try:
            account = InstagramAccount.objects.get(user=request.user)
            service = InstagramService()
            service.login_with_session(json.loads(account.session_data))
            user_id = service.cl.user_id_from_username(account.username)
            posts = service.get_user_posts(user_id)

            post_data = [{'pk': p.pk, 'code': p.code, 'thumbnail_url': p.thumbnail_url, 'caption_text': p.caption_text} for p in posts]

            return Response(post_data)
        except InstagramAccount.DoesNotExist:
            return Response({'error': 'Instagram account not linked.'}, status=status.HTTP_400_BAD_REQUEST)
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