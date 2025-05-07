from PIL import Image, UnidentifiedImageError
import torch

def load_image(image_path):
    """
    Loads an image from disk and ensures it's in RGB format.
    Handles errors gracefully.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        print(f"[INFO] Loaded image: {image_path}")
        return image
    except FileNotFoundError:
        print(f"[ERROR] File not found: {image_path}")
    except UnidentifiedImageError:
        print(f"[ERROR] Cannot identify image file: {image_path}")
    except Exception as e:
        print(f"[ERROR] Unexpected error loading image: {e}")
    return None

def preprocess_image(image, processor):
    """
    Preprocesses a PIL image using the Hugging Face processor.
    Handles resizing, normalization, and conversion to tensor.
    Returns a torch tensor ready for model input.
    """
    if image is None:
        print("[ERROR] No image to preprocess.")
        return None
    # The processor handles all required steps for ViT
    inputs = processor(images=image, return_tensors="pt")
    print("[INFO] Image preprocessed (resized, normalized, tensorized).")
    return inputs["pixel_values"]  # shape: [1, 3, 224, 224]

# (Optional) Data augmentation function
def augment_image(image):
    """
    Applies simple augmentations (e.g., horizontal flip).
    Extend as needed for more robust pipelines.
    """
    if image is None:
        return None
    # Example: random horizontal flip
    import random
    if random.random() > 0.5:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        print("[INFO] Applied horizontal flip augmentation.")
    return image


from transformers import ViTImageProcessor

# Initialize processor (reuse from your model code)
processor = ViTImageProcessor.from_pretrained("Akshay0706/Plant-Village-1-Epochs-Model")

# Load and preprocess an image


image_path = "test/test_leaf.JPG"
image = load_image(image_path)
image = augment_image(image)  # Optional
tensor = preprocess_image(image, processor)

if tensor is not None:
    print(f"[INFO] Preprocessed tensor shape: {tensor.shape}")