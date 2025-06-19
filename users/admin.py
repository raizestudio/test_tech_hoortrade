from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import AdminUser, Author, Spectator

admin.site.register(AdminUser)


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email")


admin.site.register(Spectator)
