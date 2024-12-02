import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import ImageGrab, ImageTk

from settings import DEVICE_BOUNDING_BOX


class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry(
            f"1000x{DEVICE_BOUNDING_BOX.top + DEVICE_BOUNDING_BOX.height}"
        )

        self.top = DEVICE_BOUNDING_BOX.top
        self.left = DEVICE_BOUNDING_BOX.left
        self.width = DEVICE_BOUNDING_BOX.width
        self.height = DEVICE_BOUNDING_BOX.height
        self.dimensions_file = "./data/dimensions.json"

        self.image_save_dir = "./images"
        os.makedirs(self.image_save_dir, exist_ok=True)

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.grid(row=0, column=0, sticky="nsew")

        self.controls_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        self.controls_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.label = tk.Label(self.image_frame, bg="black")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.create_controls()

        self.dimensions_dict = self.load_dimensions()
        self.update_dimensions_dropdown()

        self.update_image()

    def create_controls(self):
        tk.Label(self.controls_frame, text="Dimensions").grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(self.controls_frame, text="Top").grid(row=1, column=0, sticky="w")
        self.top_entry = tk.Entry(self.controls_frame, width=10)
        self.top_entry.insert(0, str(self.top))
        self.top_entry.grid(row=1, column=0)

        tk.Label(self.controls_frame, text="Height").grid(row=4, column=0, sticky="w")
        self.height_entry = tk.Entry(self.controls_frame, width=10)
        self.height_entry.insert(0, str(self.height))
        self.height_entry.grid(row=4, column=0)

        tk.Button(
            self.controls_frame,
            text="Update",
            command=self.update_dimensions,
        ).grid(row=5, column=0, pady=0, ipadx=39, sticky="w")

        tk.Label(self.controls_frame, text="").grid(row=6, column=0, sticky="w")
        tk.Label(self.controls_frame, text="Dimensions Name").grid(
            row=7, column=0, sticky="w"
        )
        self.dimension_name_entry = tk.Entry(self.controls_frame, width=22)
        self.dimension_name_entry.grid(row=8, column=0)
        tk.Button(self.controls_frame, text="Save", command=self.save_dimensions).grid(
            row=8, column=1, columnspan=2, pady=0, ipadx=13
        )

        tk.Label(self.controls_frame, text="").grid(row=9, column=0, sticky="w")
        tk.Label(self.controls_frame, text="Select Dimensions").grid(
            row=10,
            column=0,
            sticky="w",
        )
        self.dimensions_dropdown = ttk.Combobox(self.controls_frame, state="readonly")
        self.dimensions_dropdown.grid(row=11, column=0)
        tk.Button(
            self.controls_frame, text="Load", command=self.load_selected_dimension
        ).grid(row=11, column=1, columnspan=2, pady=0, ipadx=13)

        tk.Label(self.controls_frame, text="").grid(row=12, column=0, sticky="w")
        tk.Label(self.controls_frame, text="Image Name").grid(
            row=13,
            column=0,
            sticky="w",
        )
        self.image_name_entry = tk.Entry(self.controls_frame, width=22)
        self.image_name_entry.grid(row=14, column=0)
        tk.Button(self.controls_frame, text="Save", command=self.save_image).grid(
            row=14, column=1, columnspan=2, pady=0, ipadx=13
        )

    def load_dimensions(self):
        if os.path.exists(self.dimensions_file):
            try:
                with open(self.dimensions_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dimensions file: {e}")
        return {}

    def save_dimensions(self):
        name = self.dimension_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name for the dimensions.")
            return

        self.dimensions_dict[name] = {
            "top": self.top,
            "left": self.left,
            "width": self.width,
            "height": self.height,
        }

        try:
            with open(self.dimensions_file, "w") as f:
                json.dump(self.dimensions_dict, f, indent=4)
            self.update_dimensions_dropdown()
            messagebox.showinfo("Success", f"Dimensions '{name}' saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save dimensions: {e}")

    def update_dimensions_dropdown(self):
        self.dimensions_dropdown["values"] = list(self.dimensions_dict.keys())

    def load_selected_dimension(self):
        selected = self.dimensions_dropdown.get()
        if selected in self.dimensions_dict:
            dim = self.dimensions_dict[selected]
            self.top = dim["top"]
            self.left = dim["left"]
            self.width = dim["width"]
            self.height = dim["height"]

            self.top_entry.delete(0, tk.END)
            self.top_entry.insert(0, str(self.top))
            self.left_entry.delete(0, tk.END)
            self.left_entry.insert(0, str(self.left))
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(self.width))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(self.height))
            messagebox.showinfo(
                "Success", f"Dimensions '{selected}' loaded successfully."
            )
        else:
            messagebox.showerror("Error", "Selected dimensions not found.")

    def save_image(self):
        image_name = self.image_name_entry.get().strip()
        if not image_name:
            messagebox.showerror("Error", "Please enter a file name for the image.")
            return

        bbox = (self.left, self.top, self.left + self.width, self.top + self.height)
        screenshot = ImageGrab.grab(bbox)
        image_path = os.path.join(self.image_save_dir, f"{image_name}.png")

        selected_dimension = self.dimensions_dropdown.get()

        try:
            screenshot.save(image_path)

            handlers_file = "./data/handlers.json"
            if os.path.exists(handlers_file):
                with open(handlers_file, "r") as f:
                    handlers_data = json.load(f)
            else:
                handlers_data = {}

            handlers_data[image_name] = {
                "image_path": image_path,
                "dimensions_type": selected_dimension,
            }

            with open(handlers_file, "w") as f:
                json.dump(handlers_data, f, indent=4)

            messagebox.showinfo("Success", f"Image saved successfully at {image_path}.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

    def update_dimensions(self):
        self.top = int(self.top_entry.get())
        self.left = int(self.left_entry.get())
        self.width = int(self.width_entry.get())
        self.height = int(self.height_entry.get())

    def update_image(self):
        bbox = (self.left, self.top, self.left + self.width, self.top + self.height)
        screenshot = ImageGrab.grab(bbox)
        tk_image = ImageTk.PhotoImage(screenshot)
        self.label.config(image=tk_image)
        self.label.image = tk_image

        self.root.after(100, self.update_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
