"""Gilded Rose module.

Specifications at GildedRoseRequirements.txt

Important: do not alter the Item class!"""


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
    if item.name == "Sulfuras, Hand of Ragnaros":
        if item.quality != 80:
            raise SulfurasQualityError
    elif item.quality < 0 or item.quality > 50:
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
    def update_item(item) -> None:
        """Update an item."""
        if (
            item.name != "Aged Brie"
            and item.name != "Backstage passes to a TAFKAL80ETC concert"
        ):
            if item.quality > 0:
                if item.name != "Sulfuras, Hand of Ragnaros":
                    item.quality = item.quality - 1
        else:
            if item.quality < 50:
                item.quality = item.quality + 1
                if item.name == "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in < 11:
                        if item.quality < 50:
                            item.quality = item.quality + 1
                    if item.sell_in < 6:
                        if item.quality < 50:
                            item.quality = item.quality + 1
        if item.name != "Sulfuras, Hand of Ragnaros":
            item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            if item.name != "Aged Brie":
                if item.name != "Backstage passes to a TAFKAL80ETC concert":
                    if item.quality > 0:
                        if item.name != "Sulfuras, Hand of Ragnaros":
                            item.quality = item.quality - 1
                else:
                    item.quality = item.quality - item.quality
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
