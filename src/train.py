"""Train a configurable fully connected neural network on Fashion-MNIST."""

import csv
import os
from pathlib import Path

import numpy as np
import tensorflow as tf
import yaml


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
MODEL_DIR = ROOT / "models"


def load_params() -> dict:
    """Load model and optimization settings from params.yaml."""
    with (ROOT / "params.yaml").open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)["train"]


def build_model(params: dict) -> tf.keras.Model:
    """Construct the assignment's required Flatten-Dense-Dropout ANN."""
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(28, 28)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(params["dense_units"], activation="relu"),
            tf.keras.layers.Dropout(params["dropout_rate"]),
            tf.keras.layers.Dense(10, activation="softmax"),
        ],
        name="fashion_ann",
    )
    optimizer = tf.keras.optimizers.Adam(learning_rate=params["learning_rate"])
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def save_history(history: dict, destination: Path) -> None:
    """Write one CSV row per epoch without requiring a notebook."""
    columns = ["epoch", *history.keys()]
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for epoch in range(len(history["loss"])):
            writer.writerow(
                {"epoch": epoch + 1, **{key: values[epoch] for key, values in history.items()}}
            )


def main() -> None:
    """Load processed arrays, fit the ANN, and save its model and history."""
    params = load_params()
    seed = params["seed"]
    os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
    np.random.seed(seed)
    tf.keras.utils.set_random_seed(seed)

    train = np.load(PROCESSED_DIR / "train.npz")
    validation = np.load(PROCESSED_DIR / "val.npz")
    model = build_model(params)
    history = model.fit(
        train["images"],
        train["labels"],
        validation_data=(validation["images"], validation["labels"]),
        epochs=params["epochs"],
        batch_size=params["batch_size"],
        verbose=2,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(MODEL_DIR / "model.h5")
    save_history(history.history, MODEL_DIR / "history.csv")
    print(f"Saved trained model and history under {MODEL_DIR}")


if __name__ == "__main__":
    main()
