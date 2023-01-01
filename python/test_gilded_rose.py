"""Gilded Rose test suite."""
from typing import Iterator
import pytest
from _pytest.mark.structures import ParameterSet
from gilded_rose import Item, GildedRose


def items_are_same(item1: Item, item2: Item) -> bool:
    """Return whether two Item objects are indistinguishable."""
    if (
        item1.name == item2.name
        and item1.sell_in == item2.sell_in
        and item1.quality == item2.quality
    ):
        return True
    return False


def item_variants() -> Iterator[ParameterSet]:
    """Yield the items to test.

    Yield a tuple containing:
        - An Item object.
        - The same item, after 1 day has passed."""
    variants = {
        "Generic item - new": (
            Item("+5 Dexterity Vest", 10, 20),
            Item("+5 Dexterity Vest", 9, 19),
        ),
        "Generic item - expiration": (
            Item("+5 Dexterity Vest", 0, 10),
            Item("+5 Dexterity Vest", -1, 8),
        ),
        "Generic item - min value": (
            Item("+5 Dexterity Vest", -5, 0),
            Item("+5 Dexterity Vest", -6, 0),
        ),
        "Aged brie - new": (Item("Aged Brie", 2, 0), Item("Aged Brie", 1, 1)),
        "Aged brie - expiration": (Item("Aged Brie", 0, 2), Item("Aged Brie", -1, 4)),
        "Aged brie - max value": (
            Item("Aged Brie", -24, 50),
            Item("Aged Brie", -25, 50),
        ),
        "Sulfuras 1": (
            Item("Sulfuras, Hand of Ragnaros", 0, 80),
            Item("Sulfuras, Hand of Ragnaros", 0, 80),
        ),
        "Sulfuras 2": (
            Item("Sulfuras, Hand of Ragnaros", -1, 80),
            Item("Sulfuras, Hand of Ragnaros", -1, 80),
        ),
        "Backstage pass - new": (
            Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 14, 21),
        ),
        "Backstage pass - 10 days left": (
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 25),
            Item("Backstage passes to a TAFKAL80ETC concert", 9, 27),
        ),
        "Backstage pass - 5 days left": (
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 35),
            Item("Backstage passes to a TAFKAL80ETC concert", 4, 38),
        ),
        "Backstage pass - expiration": (
            Item("Backstage passes to a TAFKAL80ETC concert", 0, 50),
            Item("Backstage passes to a TAFKAL80ETC concert", -1, 0),
        ),
        "Backstage pass - after expiration": (
            Item("Backstage passes to a TAFKAL80ETC concert", -1, 0),
            Item("Backstage passes to a TAFKAL80ETC concert", -2, 0),
        ),
        "Backstage pass - 10 days left, max value": (
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 49),
            Item("Backstage passes to a TAFKAL80ETC concert", 9, 50),
        ),
        "Backstage pass - 5 days left, max value": (
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 48),
            Item("Backstage passes to a TAFKAL80ETC concert", 4, 50),
        ),
    }
    for key, value in variants.items():
        yield pytest.param(value, id=key)


@pytest.mark.parametrize("item", item_variants())
def test_single_item(item) -> None:
    """Test a single item after 1 day has passed."""
    shop = GildedRose(items=[item[0]])
    shop.update_quality()
    updated_item = shop.items[0]
    expected_item = item[1]
    assert items_are_same(updated_item, expected_item)
