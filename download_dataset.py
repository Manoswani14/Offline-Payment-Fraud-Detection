import os
import kaggle

# Create .kaggle directory if it doesn't exist
os.makedirs(os.path.expanduser('~/.kaggle'), exist_ok=True)

# Download the credit card fraud detection dataset
print("Downloading Credit Card Fraud Detection dataset...")
!kaggle datasets download -d mlg-ulb/creditcardfraud -p data/ --unzip

print("\nDataset downloaded successfully!")
