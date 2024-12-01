import json
from typing import Any

import numpy as np
from PIL import Image

from sizes import Dimensions


def load_json(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def trim_image(image: Any, dimensions: Dimensions) -> Any:
    if isinstance(image, Image.Image):
        image = np.array(image)

    if not isinstance(image, np.ndarray):
        raise ValueError(
            "Unsupported image format. Expected a PIL Image or NumPy array."
        )

    cropped_image = image[
        dimensions.top : dimensions.bottom, dimensions.left : dimensions.right
    ]

    return Image.fromarray(cropped_image)


def get_method_names(cls: Any) -> list[str]:
    result = []
    for method_name in dir(cls):
        if callable(getattr(cls, method_name)):
            result.append(method_name)
    return result
