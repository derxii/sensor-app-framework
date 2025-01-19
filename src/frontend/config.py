from pathlib import Path

images_dir = Path(__file__).parent.parent.joinpath("images")
default_width = 960
default_height = 576

def get_image_path(name: str):
    return str(images_dir.joinpath(name))