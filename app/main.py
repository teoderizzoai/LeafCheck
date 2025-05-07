import streamlit as st
import boto3
from config import validate_config, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_BUCKET_NAME

def test_aws_connection():
    """Test AWS S3 connection by listing buckets"""
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        buckets = s3.list_buckets()
        return True, f"Successfully connected to AWS. Found {len(buckets['Buckets'])} buckets."
    except Exception as e:
        return False, f"Failed to connect to AWS: {str(e)}"

def main():
    st.title("LeafCheck - Environment Test")
    
    # Test configuration
    try:
        validate_config()
        st.success("✅ Configuration validation passed")
    except ValueError as e:
        st.error(f"❌ Configuration error: {str(e)}")
        return

    # Test AWS connection
    st.subheader("Testing AWS Connection")
    success, message = test_aws_connection()
    if success:
        st.success(message)
    else:
        st.error(message)

    # Display environment info
    st.subheader("Environment Information")
    st.write("- Python packages installed successfully")
    st.write("- Application structure initialized")
    st.write(f"- Using AWS Region: {AWS_REGION}")
    st.write(f"- Target S3 Bucket: {AWS_BUCKET_NAME}")

if __name__ == "__main__":
    main()