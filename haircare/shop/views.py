from django.shortcuts import render
from .models import Product

def shop_home(request):
    hair_type = request.GET.get('hair_type', 'all')
    
    if hair_type and hair_type != 'all':
        products = Product.objects.filter(hair_type=hair_type)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'selected_hair_type': hair_type,
        'hair_types': [choice[0] for choice in Product.HAIR_TYPES],
    }
    return render(request, 'shop/shop_home.html', context)