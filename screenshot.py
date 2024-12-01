from typing import Any

from mss import mss
from PIL import Image

from sizes import Dimensions


class Screenshot:
    def __init__(self) -> None:
        self.sct = mss()

        self._image = None

    def capture(self, dimensions: Dimensions) -> Any:
        image = self.sct.grab(
            {
                "top": dimensions.top,
                "left": dimensions.left,
                "width": dimensions.width,
                "height": dimensions.height,
            }
        )
        image = Image.frombytes("RGB", image.size, image.bgra, "raw", "BGRX")
        self._image = image
        return self

    def get(self) -> None | Any:
        return self._image

    def show(self) -> None:
        if self._image is None:
            return
        self._image.show()
        return self

    def save(self, file_path: str) -> None:
        if self._image is None:
            return
        self._image.save(file_path)
        return self
