from django.contrib import admin

from .models import Event


@admin.register(Event)
class UrlsListAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True

    model = Event

    list_display = ('received_date', 'event_name', 'event_id', 'parsed_date', 'status')

    list_filter = ('status',)

    list_per_page = 100
