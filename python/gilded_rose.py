"""Gilded Rose module.

Specifications at GildedRoseRequirements.txt

Important: do not alter the Item class!"""

from enum import IntEnum, StrEnum


class Quality(IntEnum):
    """Special item quality values."""

    MIN = 0
    MAX = 50
    SULFURAS = 80


class SpecialItem(StrEnum):
    """Item names that are bound to special properties."""

    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BRIE = "Aged Brie"
    BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
    CONJURED = "Conjured"


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class SulfurasExpirationError(ValueError):
    """Sulfuras, Hand of Ragnaros never has to be sold."""


class SulfurasQualityError(ValueError):
    """Sulfuras, Hand of Ragnaros always has quality 80."""


class ItemQualityError(ValueError):
    """Non-legendary items must have value between 0 and 50 (included)."""


def is_valid_item(item: Item) -> bool:
    """Return whether the item is valid.

    Requirements:
        - "Sulfuras, Hand of Ragnaros" never has to be sold.
        - "Sulfuras, Hand of Ragnaros" must have quality 80.
        - For any other item, 0 <= quality <= 50."""
    if item.name == SpecialItem.SULFURAS:
        if item.quality != Quality.SULFURAS:
            raise SulfurasQualityError
        if item.sell_in > 0:
            raise SulfurasExpirationError
    elif item.quality < Quality.MIN or item.quality > Quality.MAX:
        raise ItemQualityError
    return True


class ItemDecay:
    """Group the various methods to compute item decay."""

    @staticmethod
    def generic_item(item: Item) -> None:
        """Decay of a generic item."""
        if item.quality > Quality.MIN:
            item.quality = max(
                item.quality - (1 if item.sell_in > 0 else 2), Quality.MIN
            )
        item.sell_in -= 1

    @staticmethod
    def aged_brie(item: Item) -> None:
        """Decay of Aged Brie."""
        if item.quality < Quality.MAX:
            item.quality = min(
                item.quality + (1 if item.sell_in > 0 else 2), Quality.MAX
            )
        item.sell_in -= 1

    @staticmethod
    def sulfuras(item: Item) -> None:
        """Decay of Sulfuras, Hand of Ragnaros."""

    @staticmethod
    def backstage_pass(item: Item) -> None:
        """Decay of a backstage pass."""
        if item.sell_in <= 0:
            item.quality = Quality.MIN
        elif item.quality < Quality.MAX:
            if item.sell_in <= 5:
                item.quality = min(item.quality + 3, Quality.MAX)
            elif item.sell_in <= 10:
                item.quality = min(item.quality + 2, Quality.MAX)
            else:
                item.quality = min(item.quality + 1, Quality.MAX)
        item.sell_in -= 1

    @staticmethod
    def conjured_item(item: Item) -> None:
        """Decay of a conjured item."""
        if item.quality > Quality.MIN:
            item.quality = max(
                item.quality - (2 if item.sell_in > 0 else 4), Quality.MIN
            )
        item.sell_in -= 1


class GildedRose:
    """Handle the Gilded Rose inventory."""

    def __init__(self, items) -> None:
        for item in items:
            is_valid_item(item)
        self.items = items

    def update_quality(self) -> None:
        """Update the inventory after a day has passed."""
        for item in self.items:
            self.update_item(item)

    @staticmethod
    def update_item(item: Item) -> None:
        """Update an item after a day has passed."""
        if item.name == SpecialItem.SULFURAS:
            ItemDecay.sulfuras(item)
        elif item.name == SpecialItem.BRIE:
            ItemDecay.aged_brie(item)
        elif item.name == SpecialItem.BACKSTAGE_PASS:
            ItemDecay.backstage_pass(item)
        elif item.name.startswith(SpecialItem.CONJURED):
            ItemDecay.conjured_item(item)
        else:
            ItemDecay.generic_item(item)
