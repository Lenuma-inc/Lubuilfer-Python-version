from rest_framework import viewsets, permissions, status
from .models import Package, Build
from .serializers import PackageSerializer, BuildSerializer
from .tasks import build_package
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope
from django.conf import settings
import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)

class IsOwner(permissions.BasePermission):
    """Проверяет, что пользователь является владельцем объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class PackageViewSet(viewsets.ModelViewSet):
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Package.objects.all()

    def get_queryset(self):
        return Package.objects.filter(user=self.request.user)

class BuildViewSet(viewsets.ModelViewSet):
    serializer_class = BuildSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Build.objects.all()

    def get_queryset(self):
        return Build.objects.filter(package__user=self.request.user)

    def perform_create(self, serializer):
        build = serializer.save()
        build_package.delay(build.id)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def webhook(request):
    secret_token = settings.WEBHOOK_SECRET
    signature = request.headers.get('X-Hub-Signature-256')

    if not signature:
        return Response({'error': 'Signature missing'}, status=status.HTTP_403_FORBIDDEN)

    sha_name, signature_hash = signature.split('=')
    mac = hmac.new(secret_token.encode(), msg=request.body, digestmod=hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature_hash):
        return Response({'error': 'Invalid signature'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    repo_url = data.get('repository', {}).get('git_http_url')
    if not repo_url:
        return Response({'error': 'Repository URL not found in payload'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        package = Package.objects.get(repository_url=repo_url)
        build = Build.objects.create(package=package)
        build_package.delay(build.id)
        return Response({'status': 'Build started'}, status=status.HTTP_202_ACCEPTED)
    except Package.DoesNotExist:
        return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
