from django.contrib import admin

# Register your models here.

from app1.models import Person,Order

class PersonAdmin(admin.ModelAdmin):
    """
    创建PersonAdmin类，继承于admin.ModelAdmin
    """
    # 配置展示列表，在Person板块下的列表展示
    list_display = ('first_name','last_name')
    # 配置过滤查询字段，在Person板块下右侧过滤框
    list_filter = ('first_name','last_name')
    # 配置可以搜索的字段，在Person板块下右侧搜索框
    search_fields = ('first_name',)
    # 配置只读字段展示，设置后该字段不可编辑
    readonly_fields = ('create_at','update_at')
#绑定Person模型到PersonAdmin管理后台
admin.site.register(Person,PersonAdmin)

