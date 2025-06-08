# Offline Payment Fraud Detection System

A comprehensive, offline system for detecting fraudulent credit card transactions using machine learning.

## Features

- 🚀 Advanced Machine Learning Model with Hyperparameter Tuning
- 📊 Handles Imbalanced Datasets using SMOTE
- 🤖 Feature Importance Visualization
- 📈 Batch and Real-time Prediction
- 📱 User-friendly GUI Interface
- 📦 Fully Offline Executable
- 📊 Detailed Performance Metrics
- 📈 Feature Importance Analysis

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the package:
   ```bash
   pip install .
   ```

## Usage

### Training the Model

1. Place your transaction dataset (CSV format) in the `data/` directory
2. Run the main script:
   ```bash
   python main.py
   ```
   This will:
   - Perform hyperparameter tuning
   - Train the model
   - Generate feature importance visualization
   - Save the trained model

### Using the GUI

1. Run the GUI:
   ```bash
   python gui/fraud_detector_gui.py
   ```
   The GUI allows you to:
   - Load transaction files
   - Detect fraud in real-time
   - View detailed results
   - See feature importance

### Making Predictions via Command Line

1. Place new transaction data in CSV format in the desired location
2. Use the predictor:
   ```python
   from pipeline.predictor import Predictor
   
   predictor = Predictor()
   predictor.predict("path/to/new_transactions.csv")
   ```

## Project Structure

```
fraud_detector/
├── main.py                      # Entry point
├── config.py                    # Constants and paths
├── data/                        # Input dataset directory
├── models/                      # Trained model directory
├── outputs/                     # Output directory
├── pipeline/                    # Core processing modules
│   ├── data_loader.py          # Load dataset
│   ├── preprocessor.py         # Preprocess and scale
│   ├── trainer.py              # Train the model
│   ├── evaluator.py            # Evaluate model
│   └── predictor.py            # Make predictions
├── gui/                         # GUI interface
│   └── fraud_detector_gui.py   # Main GUI application
├── setup.py                     # Package configuration
└── README.md                   # Documentation
```

## Requirements

- Python 3.10+
- scikit-learn
- imbalanced-learn
- joblib
- pandas
- numpy
- matplotlib
- seaborn
- xgboost
- tkinter

## Building the Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile main.py
   ```
   This will create an executable in the `dist` directory.

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- Kaggle Credit Card Fraud Detection Dataset
- scikit-learn
- imbalanced-learn
- pandas
- numpy
