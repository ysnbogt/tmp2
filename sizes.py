class BoundingBox:
    def __init__(self, top: int, left: int, right: int, bottom: int) -> None:
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def center(self) -> tuple[int, int]:
        # Consider screen size
        return (self.left + (self.width // 2), self.top + (self.height // 2))


class Dimensions:
    def __init__(self, top: int, left: int, width: int, height: int) -> None:
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height
