class Cart:
    def __init__(self):
        self.items = {}

    def add(self, name, price, qty=1):
        # BUG #1: negative quantities are accepted
        if name in self.items:
            self.items[name]["qty"] += qty
        else:
            self.items[name] = {"price": price, "qty": qty}

    def remove(self, name):
        # BUG #2: raises KeyError if the item is not in the cart
        del self.items[name]

    def subtotal(self):
        return sum(i["price"] * i["qty"] for i in self.items.values())

    def apply_discount(self, percent):
        # BUG #3: rounds to 1 decimal place instead of 2
        return round(self.subtotal() * (1 - percent / 100), 1)

    def average_item_price(self):
        # BUG #4: ZeroDivisionError on an empty cart
        return self.subtotal() / sum(i["qty"] for i in self.items.values())

    # FEATURE #5: export_receipt() is not implemented yet
