# Configuration settings for the Fraud Detection System

# File paths
DATA_DIR = "data"
MODEL_DIR = "models"
OUTPUT_DIR = "outputs"

# Model configuration
MODEL_PATH = f"{MODEL_DIR}/model.pkl"
PREDICTION_OUTPUT = f"{OUTPUT_DIR}/predictions.csv"

# Data preprocessing settings
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Model training settings
N_ESTIMATORS = 100
MAX_DEPTH = None
MIN_SAMPLES_SPLIT = 2
MIN_SAMPLES_LEAF = 1

# Feature scaling settings
SCALING_FEATURES = ['Amount', 'Time']
