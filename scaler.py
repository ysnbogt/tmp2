from sizes import BoundingBox, Dimensions


class Scaler:
    def __init__(self, base: BoundingBox, target: BoundingBox) -> None:
        self.base = base
        self.target = target

    def scale(self, base_box: Dimensions) -> Dimensions:
        scale_x = self.target.width / self.base.width
        scale_y = self.target.height / self.base.height

        scaled_top = (base_box.top - self.base.top) * scale_y + self.target.top
        scaled_left = (base_box.left - self.base.left) * scale_x + self.target.left
        scaled_width = base_box.width * scale_x
        scaled_height = base_box.height * scale_y

        result = Dimensions(
            top=int(scaled_top),
            left=int(scaled_left),
            width=int(scaled_width),
            height=int(scaled_height),
        )
        return result
