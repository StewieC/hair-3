from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transformation, TransformationComment
from shop.models import Product

def gallery_home(request):
    """Display all transformations with filtering options"""
    hair_type = request.GET.get('hair_type', 'all')
    concern = request.GET.get('concern', 'all')
    
    transformations = Transformation.objects.all()
    
    # Filter by hair type
    if hair_type and hair_type != 'all':
        transformations = transformations.filter(hair_type=hair_type)
    
    # Filter by concern
    if concern and concern != 'all':
        transformations = transformations.filter(concern_addressed=concern)
    
    context = {
        'transformations': transformations,
        'selected_hair_type': hair_type,
        'selected_concern': concern,
        'hair_types': Transformation.HAIR_TYPES,
        'concerns': Transformation.CONCERNS,
    }
    return render(request, 'gallery/gallery_home.html', context)


def transformation_detail(request, transformation_id):
    """Display single transformation with comments"""
    transformation = get_object_or_404(Transformation, id=transformation_id)
    comments = transformation.comments.all()
    
    context = {
        'transformation': transformation,
        'comments': comments,
    }
    return render(request, 'gallery/transformation_detail.html', context)


def add_transformation(request):
    """Form to add new transformation"""
    if request.method == 'POST':
        # Create transformation
        transformation = Transformation.objects.create(
            user_name=request.POST.get('user_name', 'Anonymous'),
            before_photo_url=request.POST.get('before_photo_url'),
            after_photo_url=request.POST.get('after_photo_url'),
            hair_type=request.POST.get('hair_type'),
            concern_addressed=request.POST.get('concern_addressed'),
            time_period=request.POST.get('time_period'),
            title=request.POST.get('title'),
            story=request.POST.get('story'),
            routine_description=request.POST.get('routine_description'),
        )
        
        # Add products if selected
        product_ids = request.POST.getlist('products_used')
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            transformation.products_used.set(products)
        
        messages.success(request, "Your transformation has been shared! Thank you for inspiring others! 🎉")
        return redirect('transformation_detail', transformation_id=transformation.id)
    
    # Get all products for selection
    products = Product.objects.all()
    
    context = {
        'products': products,
        'hair_types': Transformation.HAIR_TYPES,
        'concerns': Transformation.CONCERNS,
        'time_periods': Transformation.TIME_PERIODS,
    }
    return render(request, 'gallery/add_transformation.html', context)


def like_transformation(request, transformation_id):
    """Like a transformation"""
    transformation = get_object_or_404(Transformation, id=transformation_id)
    transformation.likes += 1
    transformation.save()
    return redirect('transformation_detail', transformation_id=transformation.id)


def add_comment(request, transformation_id):
    """Add comment to transformation"""
    transformation = get_object_or_404(Transformation, id=transformation_id)
    
    if request.method == 'POST':
        TransformationComment.objects.create(
            transformation=transformation,
            commenter_name=request.POST.get('commenter_name', 'Anonymous'),
            comment_text=request.POST.get('comment_text'),
        )
        messages.success(request, "Comment added!")
    
    return redirect('transformation_detail', transformation_id=transformation.id)