# plant_health_service.py

from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch

class PlantHealthService:
    def __init__(self, model_name="Akshay0706/Plant-Village-1-Epochs-Model", device=None):
        """
        Initializes the model and processor.
        Loads to GPU if available and requested.
        """
        print("[INFO] Initializing PlantHealthService...")
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = ViTForImageClassification.from_pretrained(model_name).to(self.device)
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        print(f"[INFO] Model loaded to device: {self.device}")

        # Disease-to-care-recommendation mapping
        # This dictionary maps disease class labels to care recommendations.
        # Extend this mapping as needed for your use case.
        self.care_recommendations = {
            "Tomato_healthy": "No disease detected. Maintain regular care.",
            "Tomato__Tomato_mosaic_virus": "Remove infected plants. Disinfect tools. Use resistant varieties.",
            "Tomato__Tomato_YellowLeaf__Curl_Virus": "Control whiteflies. Remove infected plants. Use resistant varieties.",
            "Tomato__Target_Spot": "Remove infected leaves. Apply fungicides. Rotate crops.",
            "Tomato_Spider_mites_Two_spotted_spider_mite": "Spray with water to remove mites. Use miticides if needed.",
            "Tomato_Septoria_leaf_spot": "Remove infected leaves. Avoid overhead watering. Apply fungicides.",
            "Tomato_Leaf_Mold": "Increase air circulation. Remove affected leaves. Apply fungicides.",
            "Tomato_Late_blight": "Remove and destroy infected plants. Use resistant varieties. Apply fungicides.",
            "Tomato_Early_blight": "Remove affected leaves. Avoid overhead watering. Rotate crops.",
            "Tomato_Bacterial_spot": "Remove infected plants. Use copper-based sprays. Rotate crops.",
            "Potato___healthy": "No disease detected. Maintain regular care.",
            "Potato___Late_blight": "Remove and destroy infected plants. Use certified seed. Apply fungicides.",
            "Potato___Early_blight": "Remove infected leaves. Rotate crops. Apply fungicides as needed.",
            "Pepper__bell___healthy": "No disease detected. Maintain regular care.",
            "Pepper__bell___Bacterial_spot": "Use copper-based fungicides. Remove infected plants. Rotate crops.",
        }
        # Define what is considered a 'healthy' class (can be a set for fast lookup)
        self.healthy_labels = {label for label in self.care_recommendations if 'healthy' in label.lower()}
        self.default_disease_message = "No specific care recommendation available. Consult an expert or extension service."
        self.healthy_message = "Plant appears healthy. Continue regular care and monitoring."

    def predict(self, image):
        """
        Accepts a PIL image, preprocesses, runs inference, and returns structured results
        including disease class, confidence, and care recommendation.
        """
        # Preprocess
        print("[DEBUG] Preprocessing image...")
        inputs = self.processor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"].to(self.device)
        # Inference
        print("[DEBUG] Running model inference...")
        with torch.no_grad():
            outputs = self.model(pixel_values)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            confidence, predicted_class_idx = torch.max(probs, dim=-1)
            predicted_class_idx = predicted_class_idx.item()
            confidence = confidence.item()
            label = self.model.config.id2label.get(predicted_class_idx, str(predicted_class_idx))
        print(f"[DEBUG] Predicted class: {label} (index {predicted_class_idx}), confidence: {confidence:.4f}")

        # Determine care recommendation
        if label in self.healthy_labels:
            care = self.healthy_message
        elif label in self.care_recommendations:
            care = self.care_recommendations[label]
        else:
            care = self.default_disease_message
        print(f"[DEBUG] Care recommendation: {care}")

        # Structure result
        result = {
            "predicted_class_index": predicted_class_idx,
            "predicted_label": label,
            "confidence": confidence,
            "care_recommendation": care
        }
        print(f"[INFO] Prediction result: {result}")
        return result

    def predict_from_path(self, image_path):
        """
        Loads an image from a file path and runs prediction.
        """
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            print(f"[ERROR] Could not load image: {e}")
            return None
        return self.predict(image)

# Usage example
if __name__ == '__main__':
    # Example usage of PlantHealthService
    service = PlantHealthService()
    # Replace 'test_leaf.JPG' with your image file
    result = service.predict_from_path('test/test_leaf.JPG')
    print("\nFinal result:")
    print(result)
    # To extend care recommendations, add more entries to self.care_recommendations