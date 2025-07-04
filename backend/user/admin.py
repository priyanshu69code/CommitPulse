from django.contrib import admin
from .models import User, GitHubTokern

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    readonly_fields = ('id',)

@admin.register(GitHubTokern)
class GitHubTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')
    search_fields = ('user__email', 'token')
    list_filter = ('user',)
    ordering = ('user__email',)
    readonly_fields = ('id',)

    def has_add_permission(self, request):
        return True
