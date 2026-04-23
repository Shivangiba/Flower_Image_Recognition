#  single entry point to run everything

import argparse
import os
import torch
import sys

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.train import train_model
from src.evaluate import (
    load_best_model, 
    evaluate_model, 
    print_classification_report, 
    plot_confusion_matrix, 
    plot_training_history, 
    predict_from_path
)
from src.dataset import get_dataloaders

def main():
    parser = argparse.ArgumentParser(description="Flower Classification with EfficientNet-B0")
    parser.add_argument("--mode", type=str, choices=["train", "eval", "predict"], required=True,
                        help="Mode: train a new model, evaluate existing, or predict an image")
    parser.add_argument("--image", type=str, help="Full path to image file for prediction")
    
    args = parser.parse_args()

    if args.mode == "train":
        print("\nStarting Training Pipeline...")
        history = train_model()
        print("\nGenerating Plots...")
        plot_training_history(history)
        
    elif args.mode == "eval":
        print("\nStarting Evaluation Pipeline...")
        model = load_best_model()
        if model:
            _, _, test_loader = get_dataloaders()
            preds, labels = evaluate_model(model, test_loader)
            print_classification_report(preds, labels)
            plot_confusion_matrix(preds, labels)
            
    elif args.mode == "predict":
        if not args.image:
            print("ERROR: --mode predict requires --image 'path/to/image.jpg'")
            return
            
        print(f"\nStarting Prediction for: {args.image}")
        model = load_best_model()
        if model:
            predict_from_path(args.image, model)

if __name__ == "__main__":
    main()