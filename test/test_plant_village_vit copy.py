# Step 1: Install dependencies (run this in your terminal, not in Python)
# pip install torch torchvision transformers pillow

from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch
import json

print("[INFO] Starting PlantVillage ViT model test script...")

# Step 2: Load the pre-trained PlantVillage ViT model and its processor from Hugging Face
print("[INFO] Loading model and processor from Hugging Face...")
model_name = "Akshay0706/Plant-Village-1-Epochs-Model"
model = ViTForImageClassification.from_pretrained(model_name)
processor = ViTImageProcessor.from_pretrained(model_name)
print("[INFO] Model and processor loaded successfully.")

# Step 3: Load your test image
image_path = "C:/Users/teode/Documents/CURSOR/LeafCheck/test/test_leaf.JPG"  # Update this if your image is named differently
print(f"[INFO] Loading test image from '{image_path}'...")
try:
    image = Image.open(image_path)
    print("[INFO] Test image loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load image: {e}")
    exit(1)

# Step 4: Preprocess the image for the model
print("[INFO] Preprocessing image (resize, normalize, convert to tensor)...")
inputs = processor(images=image, return_tensors="pt")
print("[INFO] Image preprocessing complete.")

# Step 5: Run inference
print("[INFO] Running inference with the model...")
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_label = model.config.id2label[predicted_class_idx]
print(f"[RESULT] Predicted class index: {predicted_class_idx}")
print(f"[RESULT] Predicted label: {predicted_label}")

# Step 6: Export the class mapping to a JSON file for metadata/reference
print("[INFO] Saving class mapping to 'plant_village_vit_classes.json'...")
with open("plant_village_vit_classes.json", "w") as f:
    json.dump(model.config.id2label, f, indent=2)
print("[INFO] Class mapping saved.")

# Step 7: Create a metadata file describing the model and its requirements
print("[INFO] Saving model metadata to 'plant_village_vit_metadata.json'...")
metadata = {
    "model_name": model_name,
    "architecture": "ViT-base-patch16-224-in21k",
    "framework": "PyTorch",
    "input_size": [224, 224, 3],
    "preprocessing": "Resize to 224x224, normalize as per ImageNet",
    "output_classes_file": "plant_village_vit_classes.json",
    "license": "Apache-2.0",
    "source": "https://huggingface.co/Akshay0706/Plant-Village-1-Epochs-Model"
}
with open("plant_village_vit_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
print("[INFO] Metadata saved.")

print("[INFO] Script completed successfully.")