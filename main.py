import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

import cv2
import numpy as np

from device_operator import DeviceOperator
from scaler import Scaler
from settings import (BASE_DEVICE_BOUNDING_BOX, BASE_UIS_DIMENSIONS,
                      DEVICE_BOUNDING_BOX, DIMENSIONS, HANDLERS_DATA)
from sizes import Dimensions
from utils import get_method_names, trim_image


class Handlers:
    def __init__(
        self,
        device_operator: DeviceOperator,
        uis_dimensions: dict[str, Dimensions],
        scaler: Scaler = None,
        delay: float = 1.0,
        match_threshold: float = 0.7,
    ) -> None:
        self.uis_dimensions = uis_dimensions
        self.scaler = scaler
        self.delay = delay
        self.match_threshold = match_threshold

        self.device_operator = device_operator
        self.screenshot_image = None

    def make_worker(
        self,
        base_image_path: str,
        dimensions: Dimensions,
        callback: Callable | str,
        wait_time: float = 5,
    ) -> None:
        base_image = cv2.imread(base_image_path)
        while True:
            while True:
                if not self.screenshot_image:
                    continue
                target_image = trim_image(self.screenshot_image, dimensions)
                if self.check_match(base_image, target_image):
                    time.sleep(self.delay)
                    if type(callback) is str:
                        self.device_operator.random_tap(self.get_dimensions(callback))
                    else:
                        callback()
                    break
                time.sleep(wait_time)
            time.sleep(wait_time)

    def concede_handler(self) -> None:
        def callback() -> None:
            self.device_operator.random_tap(self.get_dimensions("battle_menu"))
            time.sleep(random.uniform(1, 2))
            self.device_operator.random_tap(self.get_dimensions("concede_confirmation"))
            time.sleep(random.uniform(1, 2))
            self.device_operator.random_tap(self.get_dimensions("concede"))

        self.make_worker("./images/your_turn.png", DIMENSIONS["your_turn"], callback, 5)

    def capture_handler(self) -> None:
        device_dimensions = Dimensions(
            top=0,
            left=0,
            width=DEVICE_BOUNDING_BOX.width,
            height=DEVICE_BOUNDING_BOX.height,
        )
        while True:
            image = self.device_operator.screenshot.capture(device_dimensions).get()
            self.screenshot_image = image
            time.sleep(1)

    def check_match(self, a: Any, b: Any) -> bool:
        a_gray = cv2.cvtColor(np.array(a), cv2.COLOR_RGB2GRAY)
        b_gray = cv2.cvtColor(np.array(b), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(a_gray, b_gray, cv2.TM_CCOEFF_NORMED)
        _, max_value, _, _ = cv2.minMaxLoc(result)
        return self.match_threshold <= max_value

    def get_dimensions(self, ui_name: str) -> Dimensions:
        dimensions = self.uis_dimensions[ui_name]
        if self.scaler is None:
            return dimensions
        return self.scaler.scale(dimensions)


if __name__ == "__main__":
    for handler_name, data in HANDLERS_DATA.items():

        def create_handler(
            image_path: str,
            dimensions: Dimensions,
            ui_name: str,
            wait_time: float,
        ) -> Any:
            def handler(self: Handlers) -> None:
                self.make_worker(image_path, dimensions, ui_name, wait_time)

            return handler

        dimensions_type = data.get("dimensions_type")
        handler = create_handler(
            image_path=data.get("image_path"),
            dimensions=DIMENSIONS[dimensions_type],
            wait_time=data.get("wait_time", 5),
            ui_name=handler_name,
        )
        setattr(Handlers, f"{handler_name}_handler", handler)

    handlers = Handlers(
        device_operator=DeviceOperator(DEVICE_BOUNDING_BOX),
        uis_dimensions=BASE_UIS_DIMENSIONS,
        scaler=Scaler(BASE_DEVICE_BOUNDING_BOX, DEVICE_BOUNDING_BOX),
    )
    handlers.device_operator.tap(DEVICE_BOUNDING_BOX.center)
    handler_names = [m for m in get_method_names(Handlers) if m.endswith("_handler")]
    with ThreadPoolExecutor() as executor:
        for handler_name in handler_names:
            executor.submit(getattr(handlers, handler_name))
