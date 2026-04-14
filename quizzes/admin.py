from django.contrib import admin
from .models import Quiz, Question, Choice, QuizResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    min_num = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'time_limit', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    actions = ['publish_quizzes', 'unpublish_quizzes']

    def publish_quizzes(self, request, queryset):
        queryset.update(is_published=True)
    publish_quizzes.short_description = "Publish selected quizzes"

    def unpublish_quizzes(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_quizzes.short_description = "Unpublish selected quizzes"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'point_value')
    inlines = [ChoiceInline]

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed_at')
    list_filter = ('quiz', 'completed_at')
