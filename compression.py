from PIL import Image, ImageChops, ImageEnhance  # Pillow
import os

def compression_difference(image_path, save_path):
    img = Image.open(image_path).convert("RGB")
    # JPEG compression works on RGB channels

    low = save_path.replace(".jpg", "_low.jpg")
    high = save_path.replace(".jpg", "_high.jpg")

    img.save(low, "JPEG", quality=70)
    img.save(high, "JPEG", quality=95)

    # quality 70 creates moderates compression artifacts while 95 preserves near original quality.
    # contrast between them highlights inconsistencies caused by image tampering

    diff = ImageChops.difference(
        Image.open(low),
        Image.open(high)
    )

    enhancer = ImageEnhance.Brightness(diff)
    compression_image = enhancer.enhance(10)

    compression_image.save(save_path)

    os.remove(low)
    os.remove(high)
