# app/model.py

import os
import cv2
import dlib
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PREDICTOR_PATH = os.getenv("PREDICTOR_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")

# Load Dlib models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)
face_rec_model = dlib.face_recognition_model_v1(MODEL_PATH)


def create_mask(image, detections):
    """Create a precise mask overlay for detected regions only"""
    # Create an empty mask with the same dimensions as the input image
    mask = np.zeros_like(image)

    # Iterate through detections and create segmented regions
    for d in detections:
        # Extract the coordinates of the detected region
        x, y, w, h = d.left(), d.top(), d.width(), d.height()

        # Create a precise mask for the detected region
        region = mask[y:y + h, x:x + w]  # Focus only on the detected region
        region[:, :] = (255, 0, 0)  # Apply a red mask to the detected region

    # Overlay the mask on the original image
    overlay = cv2.addWeighted(image, 0.7, mask, 0.3, 0)

    return overlay


def process_image(image_path):
    """Process the image and generate defect mask"""
    try:
        # Read input image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces/defects
        detections = detector(gray)

        if len(detections) == 0:
            print("No defects detected.")
            return None

        # Generate overlay mask
        mask = create_mask(image, detections)

        # Save the mask
        mask_filename = f"{os.path.basename(image_path).split('.')[0]}_mask.png"
        mask_path = os.path.join(os.getenv("MASKS_FOLDER"), mask_filename)
        cv2.imwrite(mask_path, mask)

        return mask_path

    except Exception as e:
        print(f"Error processing image: {e}")
        return None