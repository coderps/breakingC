from django.contrib import admin
from bc.models import *
from datetime import timedelta


class StuffAdminView(admin.ModelAdmin):
    list_display = ['id', 'where', 'name', 'points',
                    'frequency', 'last_done', 'active']
    list_filter = ['where', 'frequency']


class ShopAdminView(admin.ModelAdmin):
    list_display = ['id', 'item', 'cost', 'active']


class DoneOnFilter(admin.SimpleListFilter):
    title = 'done on'
    parameter_name = 'done_on'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('day_before_yesterday', 'Day before yesterday'),
        ]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'today':
            return queryset.filter(done_on=today)
        elif self.value() == 'yesterday':
            yesterday = today - timedelta(days=1)
            return queryset.filter(done_on=yesterday)
        elif self.value() == 'day_before_yesterday':
            day_before_yesterday = today - timedelta(days=2)
            return queryset.filter(done_on=day_before_yesterday)
        else:
            return queryset


class StuffRecordAdminView(admin.ModelAdmin):
    list_display = ['id', 'player', 'get_where',
                    'get_what', 'value', 'get_points', 'get_done_on']
    list_filter = ['player', DoneOnFilter, 'record__where']

    def get_done_on(self, obj):
        return obj.done_on.strftime('%d-%m-%Y')
    get_done_on.short_description = 'DONE ON'

    def get_where(self, obj):
        return obj.record.where.capitalize()
    get_where.short_description = 'WHERE'

    def get_what(self, obj):
        return obj.record.name
    get_what.short_description = 'WHAT'

    def get_points(self, obj):
        return float(obj.record.points) * float(obj.value)
    get_points.short_description = 'POINTS'


class SettingAdminView(admin.ModelAdmin):
    list_display = ['id', 'what', 'value', 'when', 'yad', 'active']


# Register your models here.
admin.site.register(Stuff, StuffAdminView)
admin.site.register(StuffRecord, StuffRecordAdminView)
admin.site.register(Shop, ShopAdminView)
admin.site.register(ShopRecord)
admin.site.register(Stat)
admin.site.register(Vacation)
admin.site.register(VacationRecord)
admin.site.register(Setting, SettingAdminView)
