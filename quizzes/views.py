from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import Quiz, Question, Choice, QuizResult
from .forms import QuizForm, QuestionForm, ChoiceForm
from notifications.utils import notify_all_users


@login_required
def quiz_list(request):
    if request.user.is_staff_admin:
        quizzes = Quiz.objects.all().select_related('author')
    else:
        quizzes = Quiz.objects.filter(is_published=True).select_related('author')

    # Check which ones user already attempted
    attempted_ids = set(QuizResult.objects.filter(user=request.user).values_list('quiz_id', flat=True))

    return render(request, 'quizzes/quiz_list.html', {
        'quizzes': quizzes,
        'attempted_ids': attempted_ids,
    })


@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if not quiz.is_published and not request.user.is_staff_admin:
        messages.error(request, "This quiz is not available yet.")
        return redirect('quizzes:list')

    already_attempted = QuizResult.objects.filter(quiz=quiz, user=request.user).exists()
    if already_attempted:
        result = QuizResult.objects.get(quiz=quiz, user=request.user)
        return redirect('quizzes:results', pk=pk)

    questions = quiz.questions.prefetch_related('choices').all()
    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'time_limit_seconds': quiz.time_limit * 60,
    })


@login_required
def quiz_submit(request, pk):
    if request.method != 'POST':
        return redirect('quizzes:detail', pk=pk)

    quiz = get_object_or_404(Quiz, pk=pk, is_published=True)

    # Check already attempted
    if QuizResult.objects.filter(quiz=quiz, user=request.user).exists():
        messages.warning(request, "You have already attempted this quiz.")
        return redirect('quizzes:results', pk=pk)

    questions = quiz.questions.prefetch_related('choices').all()
    score = 0
    max_score = 0

    for question in questions:
        max_score += question.point_value
        selected_choice_id = request.POST.get(f'question_{question.pk}')
        if selected_choice_id:
            try:
                choice = question.choices.get(pk=selected_choice_id)
                if choice.is_correct:
                    score += question.point_value
            except Choice.DoesNotExist:
                pass

    QuizResult.objects.create(
        quiz=quiz,
        user=request.user,
        score=score,
        max_score=max_score,
    )
    messages.success(request, f"Quiz submitted! You scored {score}/{max_score}")
    return redirect('quizzes:results', pk=pk)


@login_required
def quiz_results(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    try:
        result = QuizResult.objects.get(quiz=quiz, user=request.user)
    except QuizResult.DoesNotExist:
        messages.error(request, "You haven't attempted this quiz yet.")
        return redirect('quizzes:detail', pk=pk)

    # All results for leaderboard
    all_results = QuizResult.objects.filter(quiz=quiz).select_related('user').order_by('-score')[:10]
    return render(request, 'quizzes/quiz_results.html', {
        'quiz': quiz,
        'result': result,
        'all_results': all_results,
    })


@login_required
def quiz_create(request):
    if not request.user.is_staff_admin:
        messages.error(request, "Only admins can create quizzes.")
        return redirect('quizzes:list')

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.author = request.user
            quiz.save()

            # Process questions and choices from POST
            question_count = int(request.POST.get('question_count', 0))
            for i in range(1, question_count + 1):
                q_text = request.POST.get(f'question_{i}_text', '').strip()
                q_points = int(request.POST.get(f'question_{i}_points', 1))
                if not q_text:
                    continue
                question = Question.objects.create(
                    quiz=quiz, text=q_text,
                    point_value=q_points, order=i
                )
                for j in range(1, 5):
                    c_text = request.POST.get(f'question_{i}_choice_{j}', '').strip()
                    c_correct = request.POST.get(f'question_{i}_correct') == str(j)
                    if c_text:
                        Choice.objects.create(question=question, text=c_text, is_correct=c_correct)

            # Notify all users if published
            if quiz.is_published:
                notify_all_users(
                    notification_type='quiz',
                    message=f"New quiz available: '{quiz.title}' — Take it now!",
                    link=f"/quizzes/{quiz.pk}/",
                    exclude_user=request.user,
                )
            messages.success(request, f"Quiz '{quiz.title}' created successfully!")
            return redirect('quizzes:list')
    else:
        quiz_form = QuizForm()

    return render(request, 'quizzes/quiz_create.html', {'quiz_form': quiz_form})


@login_required
def quiz_edit(request, pk):
    if not request.user.is_staff_admin:
        messages.error(request, "Only admins can edit quizzes.")
        return redirect('quizzes:list')
    quiz = get_object_or_404(Quiz, pk=pk)
    was_published = quiz.is_published

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            # Notify if newly published
            if quiz.is_published and not was_published:
                notify_all_users(
                    notification_type='quiz',
                    message=f"New quiz available: '{quiz.title}' — Take it now!",
                    link=f"/quizzes/{quiz.pk}/",
                    exclude_user=request.user,
                )
            messages.success(request, "Quiz updated!")
            return redirect('quizzes:list')
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'quizzes/quiz_edit.html', {'form': form, 'quiz': quiz})


@login_required
def quiz_delete(request, pk):
    if not request.user.is_staff_admin:
        messages.error(request, "Only admins can delete quizzes.")
        return redirect('quizzes:list')
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, "Quiz deleted.")
        return redirect('quizzes:list')
    return render(request, 'quizzes/quiz_confirm_delete.html', {'quiz': quiz})
