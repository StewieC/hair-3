from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductReview

def shop_home(request):
    hair_type = request.GET.get('hair_type', 'all')
    sort_by = request.GET.get('sort', 'featured')  # NEW: sorting
    
    if hair_type and hair_type != 'all':
        products = Product.objects.filter(hair_type=hair_type)
    else:
        products = Product.objects.all()
    
    #  Sorting options
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        # Sort by average rating (we'll calculate in template for now)
        products = products.order_by('-featured', '-created_at')

    context = {
        'products': products,
        'selected_hair_type': hair_type,
        'hair_types': [choice[0] for choice in Product.HAIR_TYPES],
        'sort_by': sort_by,
    }
    return render(request, 'shop/shop_home.html', context)


# NEW: Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    # Calculate rating distribution
    rating_distribution = {
        5: reviews.filter(rating=5).count(),
        4: reviews.filter(rating=4).count(),
        3: reviews.filter(rating=3).count(),
        2: reviews.filter(rating=2).count(),
        1: reviews.filter(rating=1).count(),
    }
    
    context = {
        'product': product,
        'reviews': reviews,
        'rating_distribution': rating_distribution,
        'average_rating': product.average_rating(),
        'review_count': product.review_count(),
    }
    return render(request, 'shop/product_detail.html', context)


# Add Review
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        ProductReview.objects.create(
            product=product,
            reviewer_name=request.POST.get('reviewer_name', 'Anonymous'),
            hair_type=request.POST.get('hair_type'),
            rating=int(request.POST.get('rating')),
            title=request.POST.get('title'),
            review_text=request.POST.get('review_text'),
            would_recommend=request.POST.get('would_recommend') == 'yes',
            image_url=request.POST.get('image_url', '')
        )
        messages.success(request, "Thank you for your review!")
        return redirect('product_detail', product_id=product.id)
    
    return render(request, 'shop/add_review.html', {'product': product})


#  Mark review as helpful
def mark_helpful(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    review.helpful_count += 1
    review.save()
    return redirect('product_detail', product_id=review.product.id)