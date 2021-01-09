import os
import cv2
import pickle
import numpy as np

# Directory paths
WORKSPACE = "../"
DATA_DIR = WORKSPACE + "dataset/"
LBFH_MODELS_DIR = WORKSPACE + "models/LBFH/"
MODELS_DATA_DIR = LBFH_MODELS_DIR + "data/"

# Variables
current_id = 0
label_ids = {}
x_train = []
y_labels = []
modelName = "custom_LBFHFaceRecognizer_model.yml"
dataModelName = "data_custom_LBFHFaceRecognizer_model.pickle"

# Create folder if they don't exist yet
try:
    os.mkdir(DATA_DIR)
except:
    pass

try:
    os.mkdir(LBFH_MODELS_DIR)
except:
    pass

try:
    os.mkdir(MODELS_DATA_DIR)
except:
    pass

print("[!] - Processing...")

for root, dirs, files in os.walk(DATA_DIR):
    if len(files):
        label = root.split("/")[-1]

        for file in files:
            # if file.endswith("jpg"):
                path = os.path.join(root, file)
        
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]

                # Resize image to get better accuracy during training & test
                image = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (70, 70))

                # Check if image is superior to a blurry threshold with Laplacian mathematic formula
                sharpness_index = cv2.Laplacian(image, cv2.CV_64F).var()

                if sharpness_index < 150:
                    print(" > [!] - Excluded image: \"" + str(path) + "\" with sharpness index: " + str(sharpness_index))
                else:
                    x_train.append(image)
                    y_labels.append(id_)

with open(MODELS_DATA_DIR + dataModelName, "wb") as f:
    pickle.dump(label_ids, f)

print("\n > [+] - Save data with labels & ids for custom LBFH model in\"" + MODELS_DATA_DIR + dataModelName + "\"")

# Create numpy array with features and labels for training
x_train = np.array(x_train)
y_labels = np.array(y_labels)

# Create custom LBFH Face Recognizer's object
recognizerModel = cv2.face.LBPHFaceRecognizer_create()

# Train custom LBFH Face Recognizer model
recognizerModel.train(x_train, y_labels)

# Save custom LBFH Face Recognizer model
recognizerModel.save(LBFH_MODELS_DIR + modelName)

print(" > [+] - Save custom LBFH model in\"" + LBFH_MODELS_DIR + modelName + "\"")

print("\n[!] - DONE!\n")
