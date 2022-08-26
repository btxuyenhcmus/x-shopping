# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from carts.models import Cart, CartItem
from store.models import Product


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 2 / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        tax = grand_total = 0
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context=context)


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(pk=product_id)
    if current_user.is_authenticated:
        cart_item = CartItem.objects.create(
            product=product, user=current_user, quantity=1)
        cart_item.save()
        return redirect('cart')
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
    cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    pass


def remove_cart_item(request, product_id, cart_item_id):
    pass


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    pass