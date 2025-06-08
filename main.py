from pipeline.data_loader import load_data
from pipeline.preprocessor import Preprocessor
from pipeline.trainer import Trainer
from pipeline.evaluator import Evaluator
from typing import Tuple
import pandas as pd
import sys
import os

def main():
    try:
        # Load data
        print("Loading dataset...")
        df = load_data("data/creditcard.csv")
        print(f"Dataset loaded with {len(df)} transactions")

        # Preprocess data
        print("\nPreprocessing data...")
        preprocessor = Preprocessor()
        X, y = preprocessor.fit_transform(df)
        X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
        
        # Train model
        print("\nTraining model...")
        trainer = Trainer()
        trainer.train(X_train, y_train)
        print("Training complete")
        
        # Save model
        trainer.save_model()
        
        # Evaluate model
        print("\nEvaluating model...")
        evaluator = Evaluator()
        metrics = evaluator.evaluate(trainer.model, X_test, y_test)
        
        print("\nModel training and evaluation complete!")
        print("\nModel metrics:")
        for metric, value in metrics.items():
            if isinstance(value, list):
                print(f"{metric}:\n{value}")
            else:
                print(f"{metric}: {value:.4f}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
