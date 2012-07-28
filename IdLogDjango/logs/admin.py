from django.contrib import admin
from logs.models import LogEntry,Category,Relation


class PreceedingInline(admin.TabularInline):
    verbose_name_plural='Preceeders'
    model=Relation
    fk_name = 'succeeder'
    extra=2
    
class SucceedingInline(admin.TabularInline):
    verbose_name_plural='Successors'
    model=Relation
    fk_name = 'preceeder'
    extra=2
    
class EntryInline(admin.TabularInline):
    verbose_name_plural='Entries in this category'
    model=LogEntry
    extra=1    

class CategoryAdmin(admin.ModelAdmin):
    inlines=[EntryInline]
    search_fields = ['categoryName']
    date_hierarchy = 'creationDate'
    list_filter = ['creationDate']
    list_display=('categoryName','creationDate','getEntries')
    

class LogAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content Information',   {'fields': ['category','content']}),
        ('Active', {'fields': ['activeFlag'],'classes': ['collapse']}),       
    ]
    inlines=[PreceedingInline,SucceedingInline]
    list_display=('content','category','user','entryDate','getPreceeders','getSucceeders')
    list_filter = ['category','user']
    search_fields = ['content']
    date_hierarchy = 'entryDate'
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()



admin.site.register(LogEntry,LogAdmin)
admin.site.register(Category,CategoryAdmin)


