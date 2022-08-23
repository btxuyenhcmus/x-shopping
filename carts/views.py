from django.shortcuts import render


def cart(request, total=0, quantity=0, cart_items=None):
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': None,
        'tax': None,
        'grand_total': None
    }
    return render(request, 'store/cart.html', context=context)
