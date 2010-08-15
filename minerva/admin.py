from django.contrib import admin

from minerva import models


class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "meaning", "level", "sub_level", "language")
    list_filter = ["language"]

class ProgressAdmin(admin.ModelAdmin):
    list_display = ("student_string", "word", "correct", "attempts")
    # TODO: Make a column that is "correct / attempts" for readability.
    list_filter = ["student"]

admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Progress, ProgressAdmin)

