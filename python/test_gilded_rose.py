"""Gilded Rose test suite."""
from typing import Iterator
import pytest
from _pytest.mark.structures import ParameterSet
from gilded_rose import (
    Item,
    GildedRose,
    ItemQualityError,
    SulfurasQualityError,
    SulfurasExpirationError,
    SpecialItem,
    Quality,
)


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
            Item("+5 Dexterity Vest", -5, Quality.MIN),
            Item("+5 Dexterity Vest", -6, Quality.MIN),
        ),
        "Aged brie - new": (Item(SpecialItem.BRIE, 2, 0), Item(SpecialItem.BRIE, 1, 1)),
        "Aged brie - expiration": (
            Item(SpecialItem.BRIE, 0, 2),
            Item(SpecialItem.BRIE, -1, 4),
        ),
        "Aged brie - max value": (
            Item(SpecialItem.BRIE, -24, Quality.MAX),
            Item(SpecialItem.BRIE, -25, Quality.MAX),
        ),
        "Sulfuras 1": (
            Item(SpecialItem.SULFURAS, 0, Quality.SULFURAS),
            Item(SpecialItem.SULFURAS, 0, Quality.SULFURAS),
        ),
        "Sulfuras 2": (
            Item(SpecialItem.SULFURAS, -1, Quality.SULFURAS),
            Item(SpecialItem.SULFURAS, -1, Quality.SULFURAS),
        ),
        "Backstage pass - new": (
            Item(SpecialItem.BACKSTAGE_PASS, 15, 20),
            Item(SpecialItem.BACKSTAGE_PASS, 14, 21),
        ),
        "Backstage pass - 10 days left": (
            Item(SpecialItem.BACKSTAGE_PASS, 10, 25),
            Item(SpecialItem.BACKSTAGE_PASS, 9, 27),
        ),
        "Backstage pass - 5 days left": (
            Item(SpecialItem.BACKSTAGE_PASS, 5, 35),
            Item(SpecialItem.BACKSTAGE_PASS, 4, 38),
        ),
        "Backstage pass - expiration": (
            Item(SpecialItem.BACKSTAGE_PASS, 0, 50),
            Item(SpecialItem.BACKSTAGE_PASS, -1, Quality.MIN),
        ),
        "Backstage pass - after expiration": (
            Item(SpecialItem.BACKSTAGE_PASS, -1, Quality.MIN),
            Item(SpecialItem.BACKSTAGE_PASS, -2, Quality.MIN),
        ),
        "Backstage pass - 10 days left, max value": (
            Item(SpecialItem.BACKSTAGE_PASS, 10, 49),
            Item(SpecialItem.BACKSTAGE_PASS, 9, Quality.MAX),
        ),
        "Backstage pass - 5 days left, max value": (
            Item(SpecialItem.BACKSTAGE_PASS, 5, 48),
            Item(SpecialItem.BACKSTAGE_PASS, 4, Quality.MAX),
        ),
        "Conjured item - new": (
            Item("Conjured Mana Cake", 3, 20),
            Item("Conjured Mana Cake", 2, 18),
        ),
        "Conjured item - expiration": (
            Item("Conjured Mana Cake", 0, 14),
            Item("Conjured Mana Cake", -1, 10),
        ),
        "Conjured item - min value": (
            Item("Conjured Mana Cake", -3, 2),
            Item("Conjured Mana Cake", -4, Quality.MIN),
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


def invalid_items() -> Iterator[ParameterSet]:
    """Yield invalid items to test.

    Yield a tuple containing:
        - An Item object.
        - The expected error to be raised."""
    variants = {
        "Generic item - over maximum": (
            Item("+5 Dexterity Vest", 10, 51),
            ItemQualityError,
        ),
        "Generic item - under minimum": (
            Item("+5 Dexterity Vest", -5, -1),
            ItemQualityError,
        ),
        "Sulfuras - wrong value 1": (
            Item(SpecialItem.SULFURAS, 0, 51),
            SulfurasQualityError,
        ),
        "Sulfuras - wrong value 2": (
            Item(SpecialItem.SULFURAS, 0, -1),
            SulfurasQualityError,
        ),
        "Sulfuras - wrong value 3": (
            Item(SpecialItem.SULFURAS, 0, 10),
            SulfurasQualityError,
        ),
        "Sulfuras - wrong expiration": (
            Item(SpecialItem.SULFURAS, 1, 80),
            SulfurasExpirationError,
        ),
    }
    for key, value in variants.items():
        yield pytest.param(value, id=key)


@pytest.mark.parametrize("item", invalid_items())
def test_invalid_item(item) -> None:
    """Test a single item after 1 day has passed."""
    expected_exception = item[1]
    with pytest.raises(expected_exception):
        GildedRose(items=[item[0]])
