from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import QuizResponse

class HomeView(TemplateView):
    template_name = 'core/home.html'

def quiz_submit(request):
    if request.method == 'POST':
        hair_type = request.POST.get('hair_type')
        scalp_type = request.POST.get('scalp_type')
        concerns = request.POST.getlist('concerns')
        porosity = request.POST.get('porosity', '')

        # Save to database
        QuizResponse.objects.create(
            hair_type=hair_type,
            scalp_type=scalp_type,
            concerns=concerns,
            porosity=porosity
        )

        # Save in session
        request.session['quiz_result'] = {
            'hair_type': hair_type,
            'scalp_type': scalp_type,
            'concerns': concerns,
            'porosity': porosity,
        }

        return redirect('quiz_result')

    return redirect('home')

def quiz_result(request):
    result = request.session.get('quiz_result')
    if not result:
        return redirect('home')
    return render(request, 'core/quiz_result.html', {'result': result})