from decimal import Decimal
from .models import Accessory


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart_session_id')
        if not cart:
            cart = self.session['cart_session_id'] = {}
        self.cart = cart

    def add(self, accessory, quantity=1, override_quantity=False):
        accessory_id = str(accessory.id)
        if accessory_id not in self.cart:
            self.cart[accessory_id] = {'quantity': 0, 'price': str(accessory.price)}

        if override_quantity:
            self.cart[accessory_id]['quantity'] = quantity
        else:
            self.cart[accessory_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, accessory):
        accessory_id = str(accessory.id)
        if accessory_id in self.cart:
            del self.cart[accessory_id]
            self.save()

    def __iter__(self):
        accessory_ids = self.cart.keys()
        accessories = Accessory.objects.filter(id__in=accessory_ids)
        cart = self.cart.copy()

        for accessory in accessories:
            cart[str(accessory.id)]['accessory'] = accessory

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart_session_id']
        self.save()
