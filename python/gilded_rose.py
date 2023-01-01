"""Gilded Rose module.

Specifications at GildedRoseRequirements.txt

Important: do not alter the Item class!"""

from enum import IntEnum, StrEnum


class Quality(IntEnum):
    """Special item qualities."""

    MIN = 0
    MAX = 50
    SULFURAS = 80


class SpecialItem(StrEnum):
    """Items with special properties identified by their unique name."""

    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BRIE = "Aged Brie"
    BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class SulfurasQualityError(ValueError):
    """Sulfuras, Hand of Ragnaros always has quality 80."""


class ItemQualityError(ValueError):
    """Non-legendary items must have value between 0 and 50 (included)."""


def is_valid_item(item: Item) -> bool:
    """Return whether the item is valid.

    Requirements:
        - "Sulfuras, Hand of Ragnaros" must have quality 80.
        - For any other item, 0 <= quality <= 50."""
    if item.name == SpecialItem.SULFURAS:
        if item.quality != Quality.SULFURAS:
            raise SulfurasQualityError
    elif item.quality < Quality.MIN or item.quality > Quality.MAX:
        raise ItemQualityError
    return True


class GildedRose:
    """Class that handles the Gilded Rose inventory."""

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
        """Update an item."""
        if item.name == SpecialItem.SULFURAS:
            return
        if item.name == SpecialItem.BRIE:
            item.quality = min(
                item.quality + (1 if item.sell_in > 0 else 2), Quality.MAX
            )
        elif item.name == SpecialItem.BACKSTAGE_PASS:
            if item.sell_in <= 0:
                item.quality = Quality.MIN
            elif item.quality < Quality.MAX:
                if item.sell_in <= 5:
                    item.quality += 3
                elif item.sell_in <= 10:
                    item.quality += 2
                else:
                    item.quality += 1
                item.quality = min(item.quality, Quality.MAX)
        else:
            if item.quality > Quality.MIN:
                item.quality = max(
                    item.quality - (1 if item.sell_in > 0 else 2), Quality.MIN
                )

        item.sell_in -= 1
        return
