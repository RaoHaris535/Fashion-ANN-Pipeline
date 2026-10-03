"""Evaluate the trained ANN and produce metrics plus a confusion matrix."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
MODEL_PATH = ROOT / "models" / "model.h5"
METRICS_PATH = ROOT / "metrics.json"
CONFUSION_MATRIX_PATH = ROOT / "models" / "confusion_matrix.png"
CLASS_NAMES = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]


def main() -> None:
    """Evaluate the saved model and persist machine-readable and visual results."""
    test = np.load(PROCESSED_DIR / "test.npz")
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    test_loss, test_accuracy = model.evaluate(
        test["images"], test["labels"], verbose=0
    )
    probabilities = model.predict(test["images"], verbose=0)
    predictions = np.argmax(probabilities, axis=1)
    matrix = confusion_matrix(test["labels"], predictions)

    figure, axis = plt.subplots(figsize=(9, 8))
    display = ConfusionMatrixDisplay(matrix, display_labels=CLASS_NAMES)
    display.plot(ax=axis, cmap="Blues", colorbar=False, xticks_rotation=35)
    axis.set_title("Fashion-MNIST Test Confusion Matrix")
    figure.tight_layout()
    figure.savefig(CONFUSION_MATRIX_PATH, dpi=180)
    plt.close(figure)

    metrics = {
        "test_loss": round(float(test_loss), 6),
        "test_accuracy": round(float(test_accuracy), 6),
        "test_samples": int(len(test["labels"])),
    }
    with METRICS_PATH.open("w", encoding="utf-8") as stream:
        json.dump(metrics, stream, indent=2)
        stream.write("\n")

    print(json.dumps(metrics, indent=2))
    print(f"Saved confusion matrix to {CONFUSION_MATRIX_PATH}")


if __name__ == "__main__":
    main()
