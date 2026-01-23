from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tip

def tips_list(request):
    tips = Tip.objects.all()
    return render(request, 'tips/tips_list.html', {'tips': tips})

def add_tip(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        hair_type = request.POST.get('hair_type', '')
        author_name = request.POST.get('author_name', 'Anonymous')

        Tip.objects.create(
            title=title,
            content=content,
            hair_type=hair_type,
            author_name=author_name
        )
        messages.success(request, "Tip posted successfully!")
        return redirect('tips_list')

    return render(request, 'tips/add_tip.html')