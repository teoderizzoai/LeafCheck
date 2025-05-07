import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'eu-north-1')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'leafcheck-uploads')

# Database Configuration
DB_NAME = os.getenv('DB_NAME', 'leafcheck')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Application Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
MODEL_PATH = os.getenv('MODEL_PATH', 'models/plant_health_model.pth')

# Validate required configuration
def validate_config():
    """Validate that all required configuration variables are set."""
    required_vars = [
        ('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID),
        ('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY),
        ('DB_PASSWORD', DB_PASSWORD),
    ]
    
    missing_vars = [var_name for var_name, var_value in required_vars if not var_value]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please create a .env file based on .env.example and fill in the required values."
        )

# Database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 