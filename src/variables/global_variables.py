# Path
WORKSPACE = ""
DATA_DIR = WORKSPACE + "dataset/"
MODELS_DIR = WORKSPACE + "models/"
LBFH_MODELS_DIR = WORKSPACE + "models/LBFH/"
MODELS_DATA_DIR = LBFH_MODELS_DIR + "data/"
HAARSCASCADE_MODELS_DIR = MODELS_DIR + "haarscascade/"

# Variables
nb_img = 0
photoTook = 0
tips = False
record = False
frameWidth = 640
frameHeight = 480
spaceBetweenFrame = False
nb_frameBeforeNextPhoto = 5
cascade = HAARSCASCADE_MODELS_DIR + "haarcascade_frontalface_alt2.xml"

# Create folder with dataset's name given by user

# Models
modelName = "custom_LBFHFaceRecognizer_model.yml"
dataModelName = "data_custom_LBFHFaceRecognizer_model.pickle"

id_image=0
frameWidth = 640
frameHeight = 480
userColorGranted = (0, 255, 0)
userColorUnknown = (0, 0, 255)
userColorInfo = (255, 255, 255)
threshold_confidence_index = 100
