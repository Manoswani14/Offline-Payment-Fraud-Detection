import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pipeline.predictor import Predictor
import pandas as pd
import os

class FraudDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Credit Card Fraud Detector")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = ttk.Label(self.main_frame, text="Credit Card Fraud Detector", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection
        ttk.Label(self.main_frame, text="Select Transaction File:").grid(row=1, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.file_path, width=50).grid(row=1, column=1)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_file).grid(row=1, column=2)
        
        # Prediction button
        ttk.Button(self.main_frame, text="Detect Fraud", command=self.detect_fraud).grid(
            row=2, column=0, columnspan=3, pady=20)
        
        # Results display
        self.results_text = tk.Text(self.main_frame, height=10, width=70)
        self.results_text.grid(row=3, column=0, columnspan=3, pady=20)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Transaction File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
        
    def detect_fraud(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a transaction file first")
            return
            
        try:
            predictor = Predictor()
            predictor.predict(file_path, "outputs/gui_predictions.csv")
            
            # Display results
            df = pd.read_csv("outputs/gui_predictions.csv")
            fraud_count = df[df['Prediction'] == 1].shape[0]
            total_count = df.shape[0]
            fraud_percentage = (fraud_count / total_count) * 100
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Fraud Detection Results:\n\n")
            self.results_text.insert(tk.END, f"Total Transactions: {total_count}\n")
            self.results_text.insert(tk.END, f"Suspected Fraud: {fraud_count}\n")
            self.results_text.insert(tk.END, f"Fraud Rate: {fraud_percentage:.2f}%\n\n")
            
            if fraud_count > 0:
                self.results_text.insert(tk.END, "Top Suspected Fraud Transactions:\n")
                top_frauds = df[df['Prediction'] == 1].head(5)
                for idx, row in top_frauds.iterrows():
                    self.results_text.insert(tk.END, f"\nTransaction Time: {row['Time']}\n")
                    self.results_text.insert(tk.END, f"Amount: ${row['Amount']:.2f}\n")
                    self.results_text.insert(tk.END, "-" * 40 + "\n")
            
            messagebox.showinfo("Success", "Fraud detection completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = FraudDetectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
