from django.contrib import admin

from minerva import models


class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "meaning", "level", "sub_level", "lang_code")
    list_filter = ["lang_code"]

class ProgressAdmin(admin.ModelAdmin):
    list_display = ("student_string", "word", "correct", "attempts")
    # TODO: Make a column that is "correct / attempts" for readability.
    list_filter = ["student"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "language_pref")
    list_filter = ["language_pref"]

class SessionProgressAdmin(admin.ModelAdmin):
    list_display = ("student_string", "word", "weight", "correct")
    list_filter = ["student"]

admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Progress, ProgressAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.SessionProgress, SessionProgressAdmin)
admin.site.register(models.Language)

