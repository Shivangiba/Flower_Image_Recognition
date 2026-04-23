# run_eval.py — Quick evaluation script
from src.evaluate import (
    load_best_model,
    evaluate_model,
    print_classification_report,
    plot_confusion_matrix
)
from src.dataset import get_dataloaders

print("Loading best saved model...")
model = load_best_model()

print("Loading test set...")
_, _, test_loader = get_dataloaders()

print("Running evaluation...")
preds, labels = evaluate_model(model, test_loader)

print("Generating report...")
print_classification_report(preds, labels)

print("Generating confusion matrix...")
plot_confusion_matrix(preds, labels)