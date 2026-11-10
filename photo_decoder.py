from pathlib import Path
import tkinter as tk
from tkinter import filedialog, TclError
import mimetypes
import base64
from langchain_core.messages import HumanMessage


# 2. Choose an image from your computer
def choose_image_file() -> Path:
    """Open a local file picker."""

    root = None
    filename = ""

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        filename = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp"),
                ("All files", "*.*"),
            ],
        )

    except TclError:
        filename = input("Image path: ").strip().strip('"').strip("'")

    finally:
        if root is not None:
            root.destroy()

    if not filename:
        raise SystemExit("No image selected.")

    return Path(filename).expanduser()


# 3. Convert image to Base64 Data URL
def image_to_data_url(image_path: Path) -> str:

    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))

    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Not an image file: {image_path}")

    image_data = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    return f"data:{mime_type};base64,{image_data}"


# 4. Build a message containing text + image
def build_image_message(
    image_path: Path,
    prompt 
) -> HumanMessage:

    return HumanMessage(
        content=[
            {
                "type": "text",
                "text": "prompt"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_to_data_url(image_path)
                }
            }
        ]
    )
