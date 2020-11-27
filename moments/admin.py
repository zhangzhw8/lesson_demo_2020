from django.contrib import admin

# Register your models here.
from moments.models import WeChatUser, Status, Reply


class StatusAdmin(admin.ModelAdmin):
    list_display = ["user", "pics", "pub_time"]
    date_hierarchy = "pub_time"
    list_filter = ["user", "text"]
    search_fields = ["user__user__username", "text", "pics"]


admin.site.register(WeChatUser)
admin.site.register(Status, StatusAdmin)
admin.site.register(Reply)