"""Download Fashion-MNIST and save immutable raw NumPy archives."""

from pathlib import Path

import numpy as np
from tensorflow import keras


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def main() -> None:
    """Download the dataset and persist the original train/test partitions."""
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(RAW_DIR / "train.npz", images=x_train, labels=y_train)
    np.savez_compressed(RAW_DIR / "test.npz", images=x_test, labels=y_test)

    print(f"Saved {len(x_train):,} training samples to {RAW_DIR / 'train.npz'}")
    print(f"Saved {len(x_test):,} test samples to {RAW_DIR / 'test.npz'}")


if __name__ == "__main__":
    main()
