import sys
from pipeline.trainer import Trainer
from pipeline.predictor import Predictor
import numpy as np

print("Starting test executable...")
print(f"Python version: {sys.version}")

try:
    # Test trainer
    print("\nTesting Trainer...")
    trainer = Trainer()
    print("Trainer initialized successfully")
    
    # Test predictor
    print("\nTesting Predictor...")
    predictor = Predictor()
    print("Predictor initialized successfully")
    
    print("\nAll tests passed!")
    
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)
