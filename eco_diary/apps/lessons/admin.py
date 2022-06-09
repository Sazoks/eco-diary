from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )


@admin.register(models.Research)
class ResearchAdmin(admin.ModelAdmin):
    pass


class SliderInline(admin.StackedInline):
    extra = 0
    model = models.Slide


class PracticalTaskStepInline(admin.StackedInline):
    extra = 0
    model = models.PracticalTaskStep


class AddMaterialInline(admin.StackedInline):
    extra = 0
    model = models.AddMaterial


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    inlines = (
        SliderInline,
        PracticalTaskStepInline,
        AddMaterialInline,
    )
    fieldsets = (
        (_('Системная информация'), {
            'fields': ('url_pattern', 'description', 'unit'),
        }),
        (_('Основная информация'), {
            'fields': (
                'title', 'preview', 'serial_number',
                'background_image', 'practical_title',
            ),
        }),
        (_('Это интересно'), {
            'fields': ('interesting_img', 'interesting_text'),
        }),
        (_('Факт'), {
            'fields': ('fact_img', 'fact_text'),
        }),
    )
    list_filter = ('unit', )


class TrainerAnswerInline(admin.StackedInline):
    extra = 0
    model = models.TrainerAnswer


@admin.register(models.Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('text', )
    list_display_links = ('text', )
    inlines = (
        TrainerAnswerInline,
    )


class GameAnswerInline(admin.StackedInline):
    extra = 0
    model = models.GameAnswer


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('text', )
    list_display_links = ('text', )
    inlines = (
        GameAnswerInline,
    )
