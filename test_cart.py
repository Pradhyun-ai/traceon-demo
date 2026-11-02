import pytest
from shop.cart import Cart


def make():
    c = Cart()
    c.add("book", 19.99, 3)
    return c


def test_subtotal():
    assert make().subtotal() == pytest.approx(59.97)


def test_negative_quantity_rejected():           # bug 1
    with pytest.raises(ValueError):
        Cart().add("pen", 1.5, -2)


def test_remove_missing_item_is_noop():          # bug 2
    Cart().remove("ghost")


def test_discount_rounds_to_cents():             # bug 3
    assert make().apply_discount(15) == 50.97


def test_average_price_empty_cart():             # bug 4
    assert Cart().average_item_price() == 0


@pytest.mark.skip(reason="feature #5 not built yet")
def test_export_receipt():
    assert "book" in make().export_receipt()
