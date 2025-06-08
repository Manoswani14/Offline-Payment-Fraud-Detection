from pipeline.predictor import Predictor

# Create predictor instance
predictor = Predictor()

# Make prediction on test transaction
predictor.predict("data/test_transaction.csv")
