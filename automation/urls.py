from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    InstagramLoginView,
    InstagramPostsView,
    AutomationRuleViewSet,
    TaskLogViewSet
)

router = DefaultRouter()
router.register(r'rules', AutomationRuleViewSet, basename='automationrule')
router.register(r'logs', TaskLogViewSet, basename='tasklog')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('instagram/login/', InstagramLoginView.as_view(), name='instagram-login'),
    path('instagram/posts/', InstagramPostsView.as_view(), name='instagram-posts'),
    path('', include(router.urls)),
]