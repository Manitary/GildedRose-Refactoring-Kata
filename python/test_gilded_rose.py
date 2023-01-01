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
