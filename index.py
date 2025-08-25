import os
import cv2
import requests
import json
from PIL import Image
import numpy as np
from pathlib import Path

class AdultContentDetector:
    def __init__(self):
        # You'll need to get API keys for these services
        self.moderatecontent_api_key = "YOUR_MODERATECONTENT_API_KEY"
        self.sightengine_api_user = "YOUR_SIGHTENGINE_USER"
        self.sightengine_api_secret = "YOUR_SIGHTENGINE_SECRET"
        
    def check_with_moderatecontent(self, image_path):
        """
        Check image using ModerateContent API
        """
        try:
            url = "https://api.moderatecontent.com/moderate/"
            
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                data = {'key': self.moderatecontent_api_key}
                
                response = requests.post(url, files=files, data=data)
                result = response.json()
                
                if response.status_code == 200:
                    # Check if adult content is detected
                    adult_score = result.get('predictions', {}).get('adult', 0)
                    return adult_score > 0.5  # Threshold for adult content
                    
        except Exception as e:
            print(f"Error with ModerateContent API: {e}")
            return False
            
    def check_with_sightengine(self, image_path):
        """
        Check image using Sightengine API
        """
        try:
            url = "https://api.sightengine.com/1.0/check.json"
            
            with open(image_path, 'rb') as image_file:
                files = {'media': image_file}
                data = {
                    'models': 'nudity-2.0',
                    'api_user': self.sightengine_api_user,
                    'api_secret': self.sightengine_api_secret
                }
                
                response = requests.post(url, files=files, data=data)
                result = response.json()
                
                if response.status_code == 200:
                    # Check nudity scores
                    nudity = result.get('nudity', {})
                    adult_score = nudity.get('sexual_activity', 0) + nudity.get('sexual_display', 0)
                    return adult_score > 0.5
                    
        except Exception as e:
            print(f"Error with Sightengine API: {e}")
            return False
    
    def basic_skin_detection(self, image_path):
        """
        Basic skin tone detection as a fallback method
        This is not reliable for adult content detection but can be used as a basic filter
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return False
                
            # Convert to HSV color space
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define range for skin color in HSV
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask for skin pixels
            skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Calculate percentage of skin pixels
            skin_pixels = cv2.countNonZero(skin_mask)
            total_pixels = image.shape[0] * image.shape[1]
            skin_percentage = skin_pixels / total_pixels
            
            # If more than 30% skin, flag for review
            return skin_percentage > 0.3
            
        except Exception as e:
            print(f"Error in skin detection: {e}")
            return False
    
    def is_valid_image(self, image_path):
        """
        Check if the file is a valid image
        """
        try:
            valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
            file_ext = Path(image_path).suffix.lower()
            
            if file_ext not in valid_extensions:
                return False
                
            # Try to open with PIL
            with Image.open(image_path) as img:
                img.verify()
            return True
            
        except Exception:
            return False
    
    def safe_delete_file(self, file_path):
        """
        Safely delete a file with confirmation
        """
        try:
            if os.path.exists(file_path):
                # Move to trash/recycle bin instead of permanent deletion
                # This is safer for accidental deletions
                
                # For Windows
                if os.name == 'nt':
                    try:
                        import winshell
                        winshell.delete_file(file_path)
                        return True
                    except ImportError:
                        pass
                
                # For macOS/Linux - move to .Trash folder
                trash_dir = os.path.expanduser('~/.Trash')
                if not os.path.exists(trash_dir):
                    trash_dir = os.path.expanduser('~/.local/share/Trash/files')
                    os.makedirs(trash_dir, exist_ok=True)
                
                if os.path.exists(trash_dir):
                    import shutil
                    filename = os.path.basename(file_path)
                    trash_path = os.path.join(trash_dir, filename)
                    shutil.move(file_path, trash_path)
                    return True
                else:
                    # Fallback: rename file with .deleted extension
                    deleted_path = file_path + '.deleted'
                    os.rename(file_path, deleted_path)
                    return True
                    
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
            
        return False
    
    def process_image(self, image_path, use_api=True):
        """
        Main function to process an image
        """
        print(f"Processing image: {image_path}")
        
        # Check if file exists and is a valid image
        if not os.path.exists(image_path):
            print("Error: File does not exist!")
            return False
            
        if not self.is_valid_image(image_path):
            print("Error: Invalid image file!")
            return False
        
        is_adult_content = False
        detection_methods = []
        
        # Try API-based detection first (more accurate)
        if use_api:
            if self.moderatecontent_api_key != "YOUR_MODERATECONTENT_API_KEY":
                moderate_result = self.check_with_moderatecontent(image_path)
                if moderate_result:
                    is_adult_content = True
                    detection_methods.append("ModerateContent API")
            
            if self.sightengine_api_user != "YOUR_SIGHTENGINE_USER":
                sightengine_result = self.check_with_sightengine(image_path)
                if sightengine_result:
                    is_adult_content = True
                    detection_methods.append("Sightengine API")
        
        # Fallback to basic detection if no API keys configured
        if not detection_methods:
            print("No API keys configured. Using basic skin detection (not reliable)...")
            basic_result = self.basic_skin_detection(image_path)
            if basic_result:
                is_adult_content = True
                detection_methods.append("Basic skin detection (unreliable)")
        
        # Results
        if is_adult_content:
            print(f"⚠️  Adult content detected using: {', '.join(detection_methods)}")
            
            # Ask for confirmation before deletion
            response = input("Do you want to delete this image? (y/N): ").lower().strip()
            
            if response in ['y', 'yes']:
                if self.safe_delete_file(image_path):
                    print("✅ Image moved to trash successfully!")
                else:
                    print("❌ Failed to delete image!")
            else:
                print("Image kept (not deleted)")
                
        else:
            print("✅ No adult content detected. Image is safe.")
            
        return is_adult_content

def main():
    detector = AdultContentDetector()
    
    print("Adult Content Image Detector")
    print("=" * 40)
    print("Note: For better accuracy, configure API keys in the code:")
    print("1. ModerateContent API: https://moderatecontent.com/")
    print("2. Sightengine API: https://sightengine.com/")
    print()
    
    while True:
        image_path = input("Enter image path (or 'quit' to exit): ").strip()
        
        if image_path.lower() in ['quit', 'exit', 'q']:
            break
            
        if image_path.startswith('"') and image_path.endswith('"'):
            image_path = image_path[1:-1]  # Remove quotes
            
        detector.process_image(image_path)
        print("-" * 40)

if __name__ == "__main__":
    # Required packages installation command:
    # pip install opencv-python pillow requests numpy pathlib
    
    # Optional for Windows trash functionality:
    # pip install winshell
    
    main()
