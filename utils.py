from PIL import Image, ImageTk

def load_icon(filename):
    try:
        return ImageTk.PhotoImage(Image.open(filename).resize((16, 16), Image.Resampling.LANCZOS))
    except Exception:
        return None

def load_icons():
    return {"folder": load_icon("folder_icon.png")}
