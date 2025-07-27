import os

class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/predict")
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {'csv'}

    @staticmethod
    def is_allowed_file(filename):  
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS  
    @staticmethod
    def create_upload_folder():
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)  # Create the upload folder if it doesn't exist
Config.create_upload_folder()  # Ensure the upload folder is created at startup
