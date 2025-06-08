import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pipeline.predictor import Predictor
from pipeline.ensemble_trainer import EnsembleTrainer
import os
from datetime import datetime
from utils.logger import Logger

class EnhancedFraudDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Credit Card Fraud Detector")
        self.root.geometry("1200x800")
        
        self.logger = Logger('gui').get_logger()
        self.predictor = None
        self.model = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(self.main_frame, text="Enhanced Credit Card Fraud Detector", 
                         font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        ttk.Label(self.main_frame, text="Select Transaction File:").grid(row=1, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.file_path, width=50).grid(row=1, column=1)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_file).grid(row=1, column=2)
        
        # Prediction controls
        ttk.Button(self.main_frame, text="Detect Fraud", command=self.detect_fraud).grid(
            row=2, column=0, columnspan=3, pady=10)
        
        # Threshold slider
        ttk.Label(self.main_frame, text="Prediction Threshold:").grid(row=3, column=0, sticky=tk.W)
        self.threshold = tk.DoubleVar(value=0.5)
        ttk.Scale(self.main_frame, from_=0.1, to=0.9, variable=self.threshold, 
                 orient=tk.HORIZONTAL, length=300).grid(row=3, column=1, columnspan=2)
        
        # Results display
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="5")
        self.results_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Create tabs for different views
        self.tab_control = ttk.Notebook(self.results_frame)
        
        # Summary tab
        self.summary_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.summary_tab, text='Summary')
        
        # Detailed results tab
        self.detailed_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.detailed_tab, text='Detailed Results')
        
        # Visualizations tab
        self.visualization_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.visualization_tab, text='Visualizations')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Create visualization canvas
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_tab)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.status_var).grid(
            row=5, column=0, columnspan=3, pady=10)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Transaction File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            self.status_var.set(f"Selected file: {os.path.basename(file_path)}")
        
    def detect_fraud(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a transaction file first")
            return
            
        try:
            if not self.model:
                self.model = EnsembleTrainer.load()
            
            # Load and predict data
            df = pd.read_csv(file_path)
            X = df.drop(['Class'], axis=1, errors='ignore')
            
            # Get predictions
            y_pred = self.model.predict(X, threshold=self.threshold.get())
            y_proba = self.model.predict_proba(X)
            
            # Update summary tab
            self.update_summary(df, y_pred, y_proba)
            
            # Update detailed results
            self.update_detailed_results(df, y_pred, y_proba)
            
            # Update visualizations
            self.update_visualizations(y_pred, y_proba)
            
            messagebox.showinfo("Success", "Fraud detection completed!")
            
        except Exception as e:
            self.logger.error(f"Error during fraud detection: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def update_summary(self, df, y_pred, y_proba):
        """Update the summary tab with key metrics"""
        fraud_count = y_pred.sum()
        total_count = len(y_pred)
        fraud_rate = fraud_count / total_count * 100
        
        summary = f"Total Transactions: {total_count}\n"
        summary += f"Suspected Fraud: {fraud_count}\n"
        summary += f"Fraud Rate: {fraud_rate:.2f}%\n"
        summary += f"Threshold: {self.threshold.get():.2f}\n"
        
        ttk.Label(self.summary_tab, text=summary, justify=tk.LEFT).pack(pady=10)
        
    def update_detailed_results(self, df, y_pred, y_proba):
        """Update the detailed results tab"""
        results = df.copy()
        results['Prediction'] = y_pred
        results['Probability'] = y_proba
        
        # Sort by probability of fraud
        results = results.sort_values('Probability', ascending=False)
        
        # Create text widget for detailed results
        text_widget = scrolledtext.ScrolledText(self.detailed_tab, width=100, height=20)
        text_widget.pack(pady=10)
        
        # Display top suspicious transactions
        for idx, row in results.head(10).iterrows():
            text_widget.insert(tk.END, f"Transaction ID: {idx}\n")
            text_widget.insert(tk.END, f"Amount: ${row['Amount']:.2f}\n")
            text_widget.insert(tk.END, f"Time: {row['Time']}\n")
            text_widget.insert(tk.END, f"Probability of Fraud: {row['Probability']:.4f}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n\n")
        
    def update_visualizations(self, y_pred, y_proba):
        """Update the visualization tab"""
        self.ax.clear()
        
        # Distribution of fraud probabilities
        self.ax.hist(y_proba[y_pred == 0], bins=20, alpha=0.5, label='Non-Fraud')
        self.ax.hist(y_proba[y_pred == 1], bins=20, alpha=0.5, label='Fraud')
        
        self.ax.set_title('Fraud Probability Distribution')
        self.ax.set_xlabel('Probability of Fraud')
        self.ax.set_ylabel('Number of Transactions')
        self.ax.legend()
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = EnhancedFraudDetectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
