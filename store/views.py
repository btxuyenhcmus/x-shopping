# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from category.models import Category
from store.models import Product, ReviewRating
from store.forms import ReviewForm

import os


NUMBER_PER_PAGE = os.environ.get('PRODUCT_PER_PAGE')


def store(request, category_slug=None):
    products = Product.objects.filter(is_available=True).order_by('id')
    links = Category.objects.all()
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)

    page = request.GET.get('page') or 1
    paginator = Paginator(products, NUMBER_PER_PAGE)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'links': links
    }

    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug=None):
    single_product = Product.objects.get(slug=product_slug)
    context = {
        'single_product': single_product
    }
    return render(request, 'store/product_detail.html', context=context)


def search(request):
    links = Category.objects.all()
    q = request.GET.get('q') or ''
    products = Product.objects.order_by(
        '-created_date').filter(Q(name__icontains=q) | Q(description__icontains=q))
    page = request.GET.get('page') or 1
    paginator = Paginator(products, NUMBER_PER_PAGE)
    paged_products = paginator.get_page(page)
    product_count = products.count()
    context = {
        'products': paged_products,
        'q': q,
        'product_count': product_count,
        'links': links
    }
    return render(request, 'store/store.html', context=context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(
                request, "Thank you! Your review has been updated.")
            return redirect(url)
        except Exception:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_date['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "Thank you! Your review has been submitted.")
                return redirect(url)
