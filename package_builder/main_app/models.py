from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    repository_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'version', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.version})'

class Build(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Building', 'Building'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Error', 'Error'),
    ]

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='builds')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Build #{self.id} for {self.package.name}'
