## Requirements

- Unused Mac
- Unused iPhone

## Procedure

Enable iPhone mirroring by updating the Mac and iPhone software and matching Apple accounts. Place the mirroring window in the top-left corner `(0, 0)`.

### 1. Specify Device Size

Press <kbd>Command + Shift + 4</kbd> to display coordinates and specify the arguments for `DEVICE_BOUNDING_BOX` in `settings.py`.

### 2. Run `tmp.py` to Capture Comparison Images

| Input Item      | Description |
| --------------- | ----------- |
| Range           | Specify the image range for comparison (`top, height`).<br>Choose a range with minimal movement, such as effects, and high information density to ensure uniqueness. |
| Range Name      | Save the range with a name. |
| Range Selection | Select a previously saved range. |
| Image File Name | Save the image of the selected range with a name. |

When saving an image, a handler is registered in `./data/handlers.json`.
If you register a new range, select the range once and then save the image.

The image file name is directly registered as a handler in `ui.json` under the range's key name. Ensure the screen and the key name in `ui.json` match for the desired action.

```zsh
$ # brew install python-tk@3.11
$ python3.11 tmp.py
```

### 3. Run `main.py`

> [!TIP]
> It is recommended to take a screenshot on the device and open the camera roll to check the operation.

```zsh
$ python3.11 main.py
```

Register Custom Handlers
You can register custom handlers by adding methods with names ending in `_handler` to the Handlers class in `main.py`.

The `make_worker()` method allows you to create an image comparison worker with the following:

- Path to the image file for comparison
- The `Dimensions` object of the range that matches the comparison image
- A function to execute if the comparison matches, or a key name registered in `./data/base_uis_dimensions.json` to invoke
- Optional: Seconds to wait after the image match

```py
def something_handler(self) -> None:
    def callback() -> None:
        pass

    self.make_worker("./images/something.png", DIMENSIONS["something"], callback, 5)
```

## Optional Handler Properties

- `wait_time`: Seconds to wait after the image comparison completes and the registered process is executed
