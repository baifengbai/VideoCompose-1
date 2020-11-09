from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

"""
@Author: WSWSCSJ
"""

class NullPermission(BasePermission):
    """
    占位权限
    """
    def has_permission(self, request, view):
        return True

class RootPermission(BasePermission):
    """
    开发者权限
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if request.user.username == "root":
            return True
        return False

class SubGetOnlyPermission(BasePermission):
    """
    子账户只允许GET方法
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if request.user.main_account or request.method in ["GET"]:
            return True
        return False

class SubPostOnlyPermission(BasePermission):
    """
    子账户只允许POST方法
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if request.user.main_account or request.method in ["POST"]:
            return True
        return False

class GetOnlyPermission(BasePermission):
    """
    只允许GET方法
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if request.method in ["GET"]:
            return True
        return False

class MainAccountPermission(BasePermission):
    """
    校验是否主账户
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if request.user.main_account:
            return True
        return False

class ShopPermission(BasePermission):
    """
    子账户只有GET方法的权限
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        _user = request.user
        if _user.main_account:
            return True
        if not _user.main_account and request.method in ["GET"]:
            return True
        return False

class PermissionGroupPermission(BasePermission):
    """
    子账户只有GET方法的权限
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        _user = request.user
        if _user.main_account:
            return True
        if not _user.main_account and request.method in ["GET"]:
            return True
        return False

class SubAccountPermission(BasePermission):
    """
    校验是否子账户
    """
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        if request.user.main_account:
            return False
        return True