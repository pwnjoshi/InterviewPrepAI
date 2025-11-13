from django.contrib import admin
from .models import Resume, Question, InterviewSession, Profile

admin.site.site_title = "Nexora Admin Portal"
admin.site.site_header = "Nexora Admin Portal"
admin.site.index_title = "Welcome to Nexora Admin Portal"


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'uploaded_at')
    search_fields = ('username', 'email')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_short_question', 'level', 'get_keywords')
    search_fields = ('question_text', 'level')
    list_filter = ('level',)
    
    def get_short_question(self, obj):
        if not obj.question_text:
            return 'No question text'
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    get_short_question.short_description = 'Question'
    
    def get_keywords(self, obj):
        if not obj.keywords:
            return 'No keywords'
        return ', '.join(obj.keywords) if isinstance(obj.keywords, list) else 'Invalid format'
    get_keywords.short_description = 'Keywords'


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'username', 'score', 'created_at')
    search_fields = ('session_id', 'username')
    list_filter = ('created_at', 'score')
    readonly_fields = ('session_id', 'created_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email', 'unique_user_id', 'created_at')
    search_fields = ('name', 'email', 'unique_user_id')
    list_filter = ('created_at',)
    readonly_fields = ('unique_user_id', 'created_at')