"""Normalize Fashion-MNIST and create reproducible train/validation splits."""

from pathlib import Path

import numpy as np
import yaml
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


def load_params() -> dict:
    """Load preprocessing parameters from the project configuration."""
    with (ROOT / "params.yaml").open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)["preprocess"]


def normalize(images: np.ndarray) -> np.ndarray:
    """Scale uint8 pixels to float32 values in the interval [0, 1]."""
    return images.astype(np.float32) / 255.0


def main() -> None:
    """Transform raw arrays and save train, validation, and test archives."""
    params = load_params()
    raw_train = np.load(RAW_DIR / "train.npz")
    raw_test = np.load(RAW_DIR / "test.npz")

    x_train, x_val, y_train, y_val = train_test_split(
        normalize(raw_train["images"]),
        raw_train["labels"],
        test_size=params["test_size"],
        random_state=params["seed"],
        stratify=raw_train["labels"],
    )
    x_test = normalize(raw_test["images"])
    y_test = raw_test["labels"]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(PROCESSED_DIR / "train.npz", images=x_train, labels=y_train)
    np.savez_compressed(PROCESSED_DIR / "val.npz", images=x_val, labels=y_val)
    np.savez_compressed(PROCESSED_DIR / "test.npz", images=x_test, labels=y_test)

    print(
        "Saved processed splits: "
        f"train={len(x_train):,}, validation={len(x_val):,}, test={len(x_test):,}"
    )


if __name__ == "__main__":
    main()
