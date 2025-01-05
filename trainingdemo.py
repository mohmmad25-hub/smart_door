import cv2
import numpy as np
from PIL import Image
import os

# Initialize the recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Paths for datasets
authorized_path = "datasets/authorized"  # Folder for authorized faces
unauthorized_path = "datasets/unauthorized"  # Folder for unauthorized faces

def getImageID(path, label):
    """
    Get images and IDs from the specified path.
    The label indicates whether the faces are authorized (1) or unauthorized (0).
    """
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for imagePath in imagePaths:
        try:
            # Convert the image to grayscale
            faceImage = Image.open(imagePath).convert('L')
            faceNP = np.array(faceImage)
            # Assign the label (1 for authorized, 0 for unauthorized)
            ids.append(label)
            faces.append(faceNP)
            # Optional: Show the image being trained
            cv2.imshow("Training", faceNP)
            cv2.waitKey(1)
        except Exception as e:
            print(f"Error processing {imagePath}: {e}")
    return ids, faces

# Load and label authorized faces
auth_ids, auth_faces = getImageID(authorized_path, label=1)

# Load and label unauthorized faces
unauth_ids, unauth_faces = getImageID(unauthorized_path, label=0)

# Combine the data
ids = auth_ids + unauth_ids
faces = auth_faces + unauth_faces

# Train the recognizer
recognizer.train(faces, np.array(ids))
recognizer.write("Trainer.yml")
cv2.destroyAllWindows()
print("Training Completed for both Authorized and Unauthorized faces.")
