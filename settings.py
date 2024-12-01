from sizes import BoundingBox, Dimensions
from utils import load_json

# Bounding box when the iPhone mirroring window
# of the reference device is placed at (0, 0)
BASE_DEVICE_BOUNDING_BOX = BoundingBox(top=40, left=6, right=420, bottom=934)
# UI range measured with reference device
BASE_UIS_DIMENSIONS = {
    k: Dimensions(**v) for k, v in load_json("./data/base_uis_dimensions.json").items()
}

# Registered image ranges for comparison
DIMENSIONS = {
    k: Dimensions(**v) for k, v in load_json("./data/dimensions.json").items()
}

HANDLERS_DATA = load_json("./data/handlers.json")

#! Do not rewrite any code above this

# Bounding box for your device's iPhone mirroring window when placed at (0, 0)
# [TODO]
# Press `Command + Shift + 4` to display the coordinates
# Specify the value of the argument while looking at the coordinates
DEVICE_BOUNDING_BOX = BoundingBox(top=37, left=5, right=434, bottom=964)
