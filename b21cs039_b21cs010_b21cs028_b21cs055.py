# -*- coding: utf-8 -*-
"""B21CS039_B21CS010_B21CS028_B21CS055.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gf4MfZEirmu9zANwu96SjitjyGuG0kJ6

## CODE 1
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained face detectors (Haar cascades)
face_cascade_frontal = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')
face_cascade_profile = cv2.CascadeClassifier('/content/haarcascade_profileface.xml')

def detect_faces(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading image: {image_path}")
        return None, None
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces using Haar cascade
    faces_frontal = face_cascade_frontal.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)
    # Detect profile faces using Haar cascade
    faces_profile = face_cascade_profile.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=3)

    # Combine the detected faces
    detected_faces = []
    for (x1, y1, w1, h1) in faces_frontal:
        frontal_region = gray_img[y1:y1+h1, x1:x1+w1]
        found_overlap = False
        for (x2, y2, w2, h2) in faces_profile:
            if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                found_overlap = True
                break
        if not found_overlap:
            detected_faces.append((x1, y1, w1, h1))

    for (x, y, w, h) in faces_profile:
        detected_faces.append((x, y, w, h))

    detected_faces = np.array(detected_faces)

    if len(detected_faces) == 0:
        print(f"No faces detected in image: {image_path}")
        return img, []  # Return original image and empty faces list for non-face images
    else:
        print(f"{image_path}: {len(detected_faces)} face(s) detected")
        return img, detected_faces

# Path to the directory containing the images
images_dir = "/content/images"

# Process each image in the directory
for image_name in os.listdir(images_dir):
    image_path = os.path.join(images_dir, image_name)
    # Detect faces in the image
    result_img, detected_faces = detect_faces(image_path)
    if result_img is not None:
        # Display the result image with rectangles drawn around the detected faces
        plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        if len(detected_faces) > 0:
            for i, (x, y, w, h) in enumerate(detected_faces, start=1):
                plt.text(x, y - 10, f"Face {i}", color='red', fontsize=10)
                plt.gca().add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2))
            plt.title(f"Detected faces in {image_name}")
        else:
            plt.title(f"No faces detected in {image_name}")
        plt.show()

"""## CODE 2 -- original---grayscale -- detector"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained face detectors (Haar cascades)
face_cascade_frontal = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')
face_cascade_profile = cv2.CascadeClassifier('/content/haarcascade_profileface.xml')

def detect_faces(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading image: {image_path}")
        return None, None
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces using Haar cascade
    faces_frontal = face_cascade_frontal.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)
    # Detect profile faces using Haar cascade
    faces_profile = face_cascade_profile.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=3)

    # Combine the detected faces
    detected_faces = []
    for (x1, y1, w1, h1) in faces_frontal:
        frontal_region = gray_img[y1:y1+h1, x1:x1+w1]
        found_overlap = False
        for (x2, y2, w2, h2) in faces_profile:
            if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                found_overlap = True
                break
        if not found_overlap:
            detected_faces.append((x1, y1, w1, h1))

    for (x, y, w, h) in faces_profile:
        detected_faces.append((x, y, w, h))

    detected_faces = np.array(detected_faces)

    if len(detected_faces) == 0:
        print(f"No faces detected in image: {image_path}")
        return img, []  # Return original image and empty faces list for non-face images
    else:
        print(f"{image_path}: {len(detected_faces)} face(s) detected")
        return img, detected_faces

# Path to the directory containing the images
images_dir = "/content/images"

# Process each image in the directory
for image_name in os.listdir(images_dir):
    image_path = os.path.join(images_dir, image_name)
    # Detect faces in the image
    result_img, detected_faces = detect_faces(image_path)
    if result_img is not None:
        # Display the original image
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')
        plt.axis('off')

        if len(detected_faces) > 0:
            # Display the grayscale image
            plt.subplot(1, 3, 2)
            plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2GRAY), cmap='gray')
            plt.title('Grayscale Image')
            plt.axis('off')

            # Highlight the detected faces with different colors
            colored_img = result_img.copy()
            for i, (x, y, w, h) in enumerate(detected_faces, start=1):
                # Different colors for frontal and profile faces
                if w/h > 1.2:  # Aspect ratio threshold for profile faces
                    color = (255, 0, 0)  # Blue for profile faces
                    face_type = 'Profile'
                else:
                    color = (0, 0, 255)  # Red for frontal faces
                    face_type = 'Frontal'
                cv2.rectangle(colored_img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(colored_img, f"{face_type} {i}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            plt.subplot(1, 3, 3)
            plt.imshow(cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB))
            plt.title('Detected Faces')
            plt.axis('off')
        else:
            plt.subplot(1, 3, 3)
            plt.text(0.5, 0.5, 'No faces detected', horizontalalignment='center', verticalalignment='center')
            plt.axis('off')

        plt.suptitle(f"Image: {image_name}")
        plt.show()

"""##CODE 3 -- individual faces"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained face detectors (Haar cascades)
face_cascade_frontal = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')
face_cascade_profile = cv2.CascadeClassifier('/content/haarcascade_profileface.xml')

def detect_faces(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading image: {image_path}")
        return None, None
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces using Haar cascade
    faces_frontal = face_cascade_frontal.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)
    # Detect profile faces using Haar cascade
    faces_profile = face_cascade_profile.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=3)

    # Combine the detected faces
    detected_faces = []
    for (x1, y1, w1, h1) in faces_frontal:
        frontal_region = gray_img[y1:y1+h1, x1:x1+w1]
        found_overlap = False
        for (x2, y2, w2, h2) in faces_profile:
            if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                found_overlap = True
                break
        if not found_overlap:
            detected_faces.append((x1, y1, w1, h1))

    for (x, y, w, h) in faces_profile:
        detected_faces.append((x, y, w, h))

    detected_faces = np.array(detected_faces)

    if len(detected_faces) == 0:
        print(f"No faces detected in image: {image_path}")
        return img, []  # Return original image and empty faces list for non-face images
    else:
        print(f"{image_path}: {len(detected_faces)} face(s) detected")
        return img, detected_faces

# Path to the directory containing the images
images_dir = "/content/images"

# Process each image in the directory
for image_name in os.listdir(images_dir):
    image_path = os.path.join(images_dir, image_name)
    # Detect faces in the image
    result_img, detected_faces = detect_faces(image_path)
    if result_img is not None:
        # Display the original image
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')
        plt.axis('off')

        if len(detected_faces) > 0:
            # Display the grayscale image
            plt.subplot(1, 3, 2)
            plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2GRAY), cmap='gray')
            plt.title('Grayscale Image')
            plt.axis('off')

            # Display individual detected faces
            plt.subplot(2, 3, 4)
            for i, (x, y, w, h) in enumerate(detected_faces, start=1):
                face_img = result_img[y:y+h, x:x+w]
                plt.imshow(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
                plt.title(f"Face {i}")
                plt.axis('off')
                plt.show()

            # Display side-by-side comparison of original image and detected faces
            plt.subplot(1, 3, 3)
            colored_img = result_img.copy()
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(colored_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            plt.imshow(cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB))
            plt.title('Detected Faces')
            plt.axis('off')
        else:
            plt.subplot(1, 3, 3)
            plt.text(0.5, 0.5, 'No faces detected', horizontalalignment='center', verticalalignment='center')
            plt.axis('off')

        plt.suptitle(f"Image: {image_name}")
        plt.show()

"""##CODE 4 : AGE AND GENDER"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained face detectors (Haar cascades)
face_cascade_frontal = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')
face_cascade_profile = cv2.CascadeClassifier('/content/haarcascade_profileface.xml')

# Age and gender estimation functions
def estimate_age(face):
    # Use a heuristic based on the apparent size of the face in the image
    # You may need to adjust these thresholds based on your specific use case
    face_area = face[2] * face[3]
    if face_area < 2000:
        return "Child"
    elif 2000 <= face_area < 6000:
        return "Young Adult"
    else:
        return "Adult"

def estimate_gender(face):
    # Use a heuristic based on the aspect ratio of the face bounding box
    # You may need to adjust this threshold based on your specific use case
    aspect_ratio = face[2] / face[3]
    if aspect_ratio > 1.1:
        return "Male"
    else:
        return "Female"

def detect_faces(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading image: {image_path}")
        return None, None
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces using Haar cascade
    faces_frontal = face_cascade_frontal.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)
    # Detect profile faces using Haar cascade
    faces_profile = face_cascade_profile.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

    # Combine the detected faces
    detected_faces = []
    for (x1, y1, w1, h1) in faces_frontal:
        frontal_region = gray_img[y1:y1+h1, x1:x1+w1]
        found_overlap = False
        for (x2, y2, w2, h2) in faces_profile:
            if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                found_overlap = True
                break
        if not found_overlap:
            detected_faces.append((x1, y1, w1, h1))

    for (x, y, w, h) in faces_profile:
        detected_faces.append((x, y, w, h))

    detected_faces = np.array(detected_faces)

    if len(detected_faces) == 0:
        print(f"No faces detected in image: {image_path}")
        return img, []  # Return original image and empty faces list for non-face images
    else:
        print(f"{image_path}: {len(detected_faces)} face(s) detected")
        return img, detected_faces

# Path to the directory containing the images
images_dir = "/content/images"

# Process each image in the directory
for image_name in os.listdir(images_dir):
    image_path = os.path.join(images_dir, image_name)
    # Detect faces in the image
    result_img, detected_faces = detect_faces(image_path)
    if result_img is not None:
        # Display the result image with rectangles drawn around the detected faces
        plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        if len(detected_faces) > 0:
            age_gender_info = []  # Accumulate age and gender information for all faces
            for i, (x, y, w, h) in enumerate(detected_faces, start=1):
                age = estimate_age((x, y, w, h))
                gender = estimate_gender((x, y, w, h))
                age_gender_info.append((f"Face {i}", age, gender))  # Store age and gender information
                plt.text(x, y - 10, f"Face {i}", color='red', fontsize=10)
                plt.gca().add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2))
            # Display age and gender information collectively at the bottom of the output
            plt.title(f"Detected faces in {image_name}")
            plt.show()
            for info in age_gender_info:
                print(f"{info[0]} - Age: {info[1]}, Gender: {info[2]}")
        else:
            print(f"No faces detected in {image_name}")

"""##CODE 5 : Input is a video , and output is detecting faces of each frame"""

import cv2
from google.colab.patches import cv2_imshow

# Path to your video file
video_path = '/content/sample.mp4'

cap = cv2.VideoCapture(video_path)
cascade_classifier = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')

if not cap.isOpened():
    print("Error: Unable to open the video file.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = cascade_classifier.detectMultiScale(gray_frame)
        if len(detections) > 0:
            for (x, y, w, h) in detections:
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2_imshow(frame)  # Use cv2_imshow() instead of cv2.imshow()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

"""##CODE 6 : input is group of videos and output is detecting faces in a output folder"""

import os
import cv2

# Function to process a single video
def process_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    cascade_classifier = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')

    if not cap.isOpened():
        print(f"Error: Unable to open the video file {input_video_path}.")
        return

    # Get the video frame properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = cascade_classifier.detectMultiScale(gray_frame)
        # Draw rectangles around detected faces
        for (x, y, w, h) in detections:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Write the frame to the output video
        out.write(frame)

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Output video saved successfully: {output_video_path}")

# Function to process all videos in a folder
def process_videos_in_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(('.mp4', '.avi', '.mov')):
            input_video_path = os.path.join(input_folder, file_name)
            output_video_path = os.path.join(output_folder, file_name)
            print(f"Processing video: {input_video_path}")
            process_video(input_video_path, output_video_path)

# Input and output folder paths
input_folder = '/content/videos'
output_folder = '/content/output_videos'

# Process videos in the input folder
process_videos_in_folder(input_folder, output_folder)

"""##CODE 7: Face recognition with a unknown face"""

import cv2
import matplotlib.pyplot as plt

def recognize_face_in_group(known_face_path, group_image_path):
    # Load the known face image
    known_face_image = cv2.imread(known_face_path, cv2.IMREAD_GRAYSCALE)

    # Load the group image
    group_image = cv2.imread(group_image_path)
    gray_group_image = cv2.cvtColor(group_image, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('/content/haarcascade_frontalface_default.xml')

    # Detect faces in the known face image
    known_faces = face_cascade.detectMultiScale(known_face_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Detect faces in the group image
    group_faces = face_cascade.detectMultiScale(gray_group_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Define a threshold for face similarity
    threshold = 0.6

    # Flag to indicate if a match is found
    match_found = False

    # Compare the known face with each face in the group image
    for (x, y, w, h) in group_faces:
        # Extract the region of interest (ROI) from the group image
        roi = gray_group_image[y:y+h, x:x+w]

        # Resize the known face image to match the size of the ROI
        known_face_resized = cv2.resize(known_face_image, (w, h))

        # Calculate histogram of the known face and ROI
        hist_known = cv2.calcHist([known_face_resized], [0], None, [256], [0,256])
        hist_roi = cv2.calcHist([roi], [0], None, [256], [0,256])

        # Calculate correlation coefficient between histograms
        correlation = cv2.compareHist(hist_known, hist_roi, cv2.HISTCMP_CORREL)

        # Check if the correlation coefficient is above the threshold
        if correlation > threshold:
            # Draw a rectangle around the matched face in the group image
            cv2.rectangle(group_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            match_found = True
            break  # Stop after the first match

    # Display the group image with matplotlib
    plt.imshow(cv2.cvtColor(group_image, cv2.COLOR_BGR2RGB))
    if match_found:
        plt.title('Group Image with Matched Face')
    else:
        plt.title('Group Image (No Match)')
    plt.axis('off')
    plt.show()

    return match_found

# Test the function with paths to the known face image and the group image
known_face_path = '/content/individual.JPG'
group_image_path = '/content/images/face_img.JPG'
if recognize_face_in_group(known_face_path, group_image_path):
    print("A matching face is found in the group image.")
else:
    print("No matching face is found in the group image.")

# Test the function with paths to the known face image and the group image
known_face_path = '/content/individual.JPG'
group_image_path = '/content/images/group_ppl.JPG'
if recognize_face_in_group(known_face_path, group_image_path):
    print("A matching face is found in the group image.")
else:
    print("No matching face is found in the group image.")

"""##CODE 8"""

import os
import cv2
import numpy as np
# import face_recognition

# Function to load images, resize, and extract names
def load_images_and_names(folder_path, target_size=(100, 100)):
    images = []
    names = []

    for filename in os.listdir(folder_path):
        name, ext = os.path.splitext(filename)
        if ext in ['.jpg', '.jpeg', '.png']:
            img = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_GRAYSCALE)  # Load image as grayscale
            img_resized = cv2.resize(img, target_size)  # Resize image to target size
            images.append(img_resized)
            names.append(name)

    return images, names

# Function to recognize faces
def recognize_faces(known_images, known_names, unknown_image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_recognizer = cv2.face.FisherFaceRecognizer_create()

    # Convert known_names to unique integers for labels
    label_ids = {name: idx for idx, name in enumerate(set(known_names))}
    labels = [label_ids[name] for name in known_names]
    face_recognizer.train(known_images, np.array(labels))  # Convert labels to numpy array

    # Detect faces in unknown image
    faces = face_cascade.detectMultiScale(unknown_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Normalize confidence values to range [0, 100]
    def normalize_confidence(confidence):
        return 100 - confidence / 100

    # Predict label and confidence for each face in the unknown image
    for (x, y, w, h) in faces:
        roi_gray = unknown_image[y:y+h, x:x+w]
        roi_gray_resized = cv2.resize(roi_gray, (100, 100))  # Resize detected face to match training size
        label, confidence = face_recognizer.predict(roi_gray_resized)
        print("Predicted Label:", label)
        print("Predicted Confidence:", confidence)

        # Normalize confidence value
        confidence_normalized = normalize_confidence(confidence)
        print("Normalized Confidence:", confidence_normalized)

        # Map predicted label to corresponding name
        if confidence_normalized > 50:  # Set threshold for recognition
            recognized_name = [name for name, idx in label_ids.items() if idx == label][0]
        else:
            recognized_name = "Unknown"

        print("Recognized face:", recognized_name)

# Paths to known and unknown images
known_folder_path = "/content/known_person"
unknown_folder_path = "/content/unknown_person"

# Load known faces and names
known_images, known_names = load_images_and_names(known_folder_path)

# Load unknown image
unknown_image_path = os.path.join(unknown_folder_path, "unknown.jpeg")
unknown_image = cv2.imread(unknown_image_path, cv2.IMREAD_GRAYSCALE)  # Load image as grayscale

# Recognize faces in unknown image
recognize_faces(known_images, known_names, unknown_image)