import random

import pyautogui

from screenshot import Screenshot
from sizes import BoundingBox, Dimensions


class DeviceOperator:
    def __init__(self, bounding_box: BoundingBox) -> None:
        self.bounding_box = bounding_box

        self.screenshot = Screenshot()

    def tap(self, position: tuple[int, int]) -> None:
        pyautogui.moveTo(*position)
        pyautogui.click()

    def random_tap(self, dimensions: Dimensions) -> None:
        x = random.uniform(dimensions.left, dimensions.right)
        y = random.uniform(dimensions.top, dimensions.bottom)
        self.tap((x, y))

    def swipe() -> None:
        pass

    def command() -> None:
        pass
