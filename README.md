# Fashion ANN Pipeline

An end-to-end Fashion-MNIST classification project using a fully connected TensorFlow artificial neural network, Git, DVC, and Google Drive. The final pipeline reaches 87.72% test accuracy and reproduces preparation, preprocessing, training, and evaluation with one command.

## Pipeline

| Stage | Command | Main output |
| --- | --- | --- |
| prepare | `python src/prepare.py` | `data/raw/` |
| preprocess | `python src/preprocess.py` | `data/processed/` |
| train | `python src/train.py` | `models/model.h5`, `models/history.csv` |
| evaluate | `python src/evaluate.py` | `metrics.json`, confusion matrix |

The model is the required ANN architecture: `Flatten -> Dense(ReLU) -> Dropout -> Dense(10, Softmax)`. All preprocessing and training settings come from `params.yaml`.

## Setup and reproduction

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
dvc pull
dvc repro
dvc metrics show
```

The configured remote is the assignment's Google Drive folder. If Google's shared DVC OAuth client is blocked for an account, configure a private desktop OAuth client as described in the official DVC Google Drive instructions; keep the client secret and generated user credential file in local DVC configuration only.

## Experiment results

| Version | Dense units | Test loss | Test accuracy |
| --- | ---: | ---: | ---: |
| v1 | 128 | 0.348672 | 87.41% |
| v2 | 256 | 0.342278 | 87.72% |

Increasing the hidden layer from 128 to 256 units improved test accuracy by 0.31 percentage points. DVC skipped `prepare` and `preprocess` because neither their dependencies nor parameters changed; only `train` and its dependent `evaluate` stage reran.

## Version-control demonstrations

The unsquashed history includes feature commits on `dev`, a `main` hotfix followed by a rebase, stash/pop recovery, soft and hard reset demonstrations, tracked moves/removals, v1/v2 tags, and a two-branch collaboration simulation. The collaboration merge records both a source conflict in `src/preprocess.py` and divergent artifact hashes in `dvc.lock`; the final resolution regenerates authoritative processed data and leaves `dvc status` clean.
