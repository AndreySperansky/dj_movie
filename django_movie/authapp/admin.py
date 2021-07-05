from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'username', 'email', )
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'username', 'email',)
    # какие поля будут участвовать в поиске
    search_fields = ('username', 'email',)



admin.site.register(User, UserAdmin)