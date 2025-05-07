# Plant Health Detection & Care Recommendation System

## 🌱 Project Idea & Motivation
This project aims to help gardeners, farmers, and researchers quickly diagnose plant health issues from leaf photos using state-of-the-art AI. By leveraging deep learning and the PlantVillage dataset, the system can identify common diseases in tomatoes, potatoes, and peppers, and provide actionable care recommendations. The goal is to make plant disease detection accessible, fast, and easy to use for everyone.

## 🚀 What Has Been Implemented
- **Development Environment & Infrastructure:**
  - Python environment with all dependencies (PyTorch, Hugging Face Transformers, Pillow, etc.)
  - Project structure for scalable development
- **Database Setup:**
  - PostgreSQL schema for storing user data and image analysis history (future extension)
- **Model Integration:**
  - Integrated a Vision Transformer (ViT) model from Hugging Face, trained on PlantVillage
  - Model can classify images into disease/healthy classes for tomato, potato, and pepper
- **Image Upload & Preprocessing:**
  - Handles JPEG/PNG images, resizes and normalizes for the model
  - Error handling for corrupted or invalid images
- **Plant Health Classification Service:**
  - Service class wraps model and preprocessing
  - Returns disease class, confidence, and care recommendation for each image
- **Care Recommendations:**
  - Maps each disease class to actionable advice (e.g., remove infected leaves, apply fungicide)
- **Taskmaster Workflow:**
  - Project managed with Taskmaster for clear, iterative task breakdown and progress tracking
- **Testing:**
  - Scripts for running predictions on sample images
  - Metadata and class mapping files for reproducibility

## 🛠️ What I'm Working On Now
- **Refining the Plant Health Classification Service:**
  - Ensuring robust mapping between model output and care recommendations
  - Improving error handling and user feedback
- **Preparing for API/Frontend Integration:**
  - Laying groundwork for a web or mobile interface (future step)
- **Expanding Care Recommendations:**
  - Adding more detailed, expert-verified advice for each disease class
- **Documentation & Usability:**
  - Making the codebase easy to understand and extend for new contributors

## 🧑‍💻 How to Run the Model
1. **Install dependencies:**
   ```bash
   pip install torch torchvision transformers pillow
   ```
2. **Download the PlantVillage dataset** (see data/plantvillage/ for structure)
3. **Run a prediction:**
   ```bash
   python app/plant_health_service.py
   ```
   - Edit the image path in the script to test your own images
4. **Output:**
   - The script prints the predicted class, confidence, and care recommendation

## 📁 Project Structure
```
app/
  plant_health_service.py   # Main service class for prediction and care advice
  ...
data/
  plantvillage/            # PlantVillage dataset (not tracked in git)
tasks/                     # Taskmaster task files (not tracked in git)
scripts/                   # Utility scripts, PRD, complexity reports
README.md                  # This file
.gitignore                 # Ignore rules for data, models, logs, etc.
```

## 🤝 How to Extend or Contribute
- **Add new disease classes:**
  - Update the `care_recommendations` dictionary in `plant_health_service.py`
- **Improve care advice:**
  - Edit or expand the recommendations for each class
- **Add new features:**
  - Batch prediction, API endpoints, frontend integration, etc.
- **Follow the Taskmaster workflow:**
  - Check `tasks/tasks.json` for current and upcoming tasks
- **Open issues or pull requests:**
  - Contributions and suggestions are welcome!

## 📚 References
- [PlantVillage Dataset (Kaggle)](https://www.kaggle.com/datasets/emmarex/plantdisease)
- [Hugging Face Model: Akshay0706/Plant-Village-1-Epochs-Model](https://huggingface.co/Akshay0706/Plant-Village-1-Epochs-Model)
- [Taskmaster Project Management](https://github.com/task-master-ai)

---
*This project is a work in progress. For questions or suggestions, please open an issue or contact the maintainer.*
