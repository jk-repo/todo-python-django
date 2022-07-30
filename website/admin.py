from django.contrib import admin

from website.models import ToDos

# Register your models here.

@admin.register(ToDos)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ['user', 'todo', 'is_completed', 'is_valid']
    list_filter = ("user",)
    search_fields = ['user']
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()