from django.test import TestCase
from django.contrib.auth.models import User
from .models import Package, Build

class PackageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.package = Package.objects.create(
            user=self.user,
            name='testpackage',
            version='1.0',
            repository_url='https://github.com/user/repo.git'
        )

    def test_package_creation(self):
        self.assertEqual(self.package.name, 'testpackage')
        self.assertEqual(self.package.user.username, 'testuser')

class BuildModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.package = Package.objects.create(
            user=self.user,
            name='testpackage',
            version='1.0',
            repository_url='https://github.com/user/repo.git'
        )
        self.build = Build.objects.create(package=self.package)

    def test_build_creation(self):
        self.assertEqual(self.build.status, 'Pending')
        self.assertEqual(self.build.package.name, 'testpackage')
