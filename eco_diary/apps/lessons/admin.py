from django.contrib import admin

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


class AddMaterialInline(admin.StackedInline):
    extra = 0
    model = models.AddMaterial


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    inlines = (
        SliderInline,
        AddMaterialInline,
    )


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
