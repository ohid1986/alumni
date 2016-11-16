from django.contrib import admin


from .models import Person, Membership, ExecMember, Event,Gallery, Child,Constitution

# Register your models here.



admin.site.register(Event)
admin.site.register(Gallery)

admin.site.register(Membership)
admin.site.register(ExecMember)
admin.site.register(Constitution)

admin.site.register(Child)

from datetime import datetime





@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # list view

    list_display = (
        'name', 'passing_year', 'organization')
    list_filter = ('name',)
    search_fields = ('name', 'passing_year')
    # form view
    fieldsets = (
        (None, {
            'fields': (
                'name', 'organization', 'user', 'passing_year',
            )}),
        ('Related', {
            'fields': (
                'category', )}),
    )






