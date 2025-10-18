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


class InstagramPostsView(APIView):
    def get(self, request):
        try:
            account = InstagramAccount.objects.get(user=request.user)
            service = InstagramService()
            service.login_with_session(json.loads(account.session_data))
            user_id = service.cl.user_id_from_username(account.username)
            posts = service.get_user_posts(user_id)

            # We need to serialize the post objects from instagrapi
            post_data = [{'id': p.pk, 'code': p.code, 'thumbnail_url': p.thumbnail_url, 'caption_text': p.caption_text} for p in posts]

            return Response(post_data)
        except InstagramAccount.DoesNotExist:
            return Response({'error': 'Instagram account not linked.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AutomationRuleViewSet(viewsets.ModelViewSet):
    queryset = AutomationRule.objects.all()
    serializer_class = AutomationRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users should only be able to see their own automation rules.
        # This requires linking rules to users, which we do via InstagramAccount -> MonitoredPost
        user_accounts = InstagramAccount.objects.filter(user=self.request.user)
        user_posts = MonitoredPost.objects.filter(account__in=user_accounts)
        return AutomationRule.objects.filter(post__in=user_posts)

    def perform_create(self, serializer):
        # When creating a rule, ensure the post belongs to the user
        post_id = serializer.validated_data.get('post').id
        user_accounts = InstagramAccount.objects.filter(user=self.request.user)
        user_posts = MonitoredPost.objects.filter(account__in=user_accounts)
        if not user_posts.filter(id=post_id).exists():
            raise permissions.PermissionDenied("You do not have permission to create a rule for this post.")
        serializer.save()


class TaskLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskLog.objects.all()
    serializer_class = TaskLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users should only see logs for their own rules
        user_accounts = InstagramAccount.objects.filter(user=self.request.user)
        user_posts = MonitoredPost.objects.filter(account__in=user_accounts)
        user_rules = AutomationRule.objects.filter(post__in=user_posts)
        return TaskLog.objects.filter(rule__in=user_rules)