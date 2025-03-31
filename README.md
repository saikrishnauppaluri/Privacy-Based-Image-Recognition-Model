# Privacy-Based-Image-Recognition-Model

# Privacy-Based Image Recognition Model

## Overview
This project is a **privacy-focused image recognition system** that ensures user privacy by:
- Capturing only **facial vectors** without retaining the original image.
- Overlays are applied directly to the processed image, ensuring no sensitive data is stored.

The system is designed to provide a **personalized experience** for users by assigning a **unique ID** to each captured or uploaded image. (IN WORKS) 
This ID is used to store associated details such as:
- **Facial Vectors**
- **Emotion**
- **Age**
- **Gender**

Additionally, the project is scalable to include **real-time video processing** and other advanced features.

---

## Features
### Current Features
1. **Privacy-First Design**:
   - Original images are not stored.
   - Only facial vectors are retained for processing and authentication.

2. **Facial Vector-Based Recognition**:
   - Extracts facial vectors using `dlib` and stores them securely.

3. **Unique User ID Assignment**:
   - Each user is assigned a unique ID for personalized experiences.

4. **User Authentication**:
   - Users can log in by uploading a new image, which is matched against stored facial vectors.

5. **Mask Overlay**:
   - Segmented masks are applied to detected regions for visualization.

---

### Future Scalability
1. **Real-Time Video Processing**:
   - Extend the system to process live video streams for real-time recognition and analysis.

2. **Emotion Detection**:
   - Analyze facial expressions to detect emotions in real-time or from uploaded images.

3. **Age and Gender Detection**:
   - Provide additional insights by detecting the age and gender of users.

4. **Synthetic Avatars**:
   - Replace detected faces with synthetic avatars for enhanced privacy and personalization.

5. **Fun Filters**:
   - Add fun filters (e.g., sunglasses, hats) to detected faces for a playful experience.

6. **Secure Data Storage**:
   - Encrypt stored facial vectors and metadata for enhanced security.

---

## How It Works
1. **Registration**:
   - Users upload or capture an image.
   - Facial vectors are extracted, and a unique ID is assigned.
   - Metadata (e.g., filename, emotion, age, gender) is stored securely.

2. **Login**:
   - Users upload or capture an image.
   - Facial vectors are extracted and matched against stored vectors.
   - If a match is found, the user is authenticated, and their details are retrieved.

3. **Privacy**:
   - Original images are never stored.
   - Only facial vectors and metadata are retained.

---

## Installation
### Prerequisites
- Python 3.8+
- FastAPI
- OpenCV
- Dlib
- SQLite (for local database)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/defect_detection_api.git
   cd defect_detection_api