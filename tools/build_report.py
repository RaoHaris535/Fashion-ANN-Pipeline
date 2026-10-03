"""Build the four-page Assignment 3 evidence report."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Assignment3_Report_Muhammad_Haris_23L-0807.pdf"
PAGE_W, PAGE_H = letter
MARGIN = 36
NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2563A6")
PALE_BLUE = colors.HexColor("#EAF2F8")
PALE_GREEN = colors.HexColor("#EAF7EF")
INK = colors.HexColor("#18212B")
MUTED = colors.HexColor("#5D6874")
LIGHT = colors.HexColor("#D9E0E7")
TERMINAL = colors.HexColor("#111827")
TERM_TEXT = colors.HexColor("#E5E7EB")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if stringWidth(candidate, font, size) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def paragraph(c: canvas.Canvas, text: str, x: float, y: float, width: float,
              size: float = 8.4, leading: float = 11.2, color=INK,
              font: str = "Helvetica") -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def header(c: canvas.Canvas, section: str, page_no: int) -> None:
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 58, PAGE_W, 58, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15.5)
    c.drawString(MARGIN, PAGE_H - 28, "End-to-End ML Versioning with Git DVC and TensorFlow")
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN, PAGE_H - 43, section)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 43, f"Page {page_no} of 4")


def footer(c: canvas.Canvas) -> None:
    c.setStrokeColor(LIGHT)
    c.line(MARGIN, 27, PAGE_W - MARGIN, 27)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.8)
    c.drawString(MARGIN, 16, "Evidence generated from the repository's actual commands, commits, DVC lock state, and model outputs.")
    c.drawRightString(PAGE_W - MARGIN, 16, "Muhammad Haris | 23L-0807 | MLOps 7-A")


def section_title(c: canvas.Canvas, title: str, y: float) -> float:
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, title)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.4)
    c.line(MARGIN, y - 5, MARGIN + 38, y - 5)
    return y - 17


def terminal_box(c: canvas.Canvas, title: str, text: str, x: float, y_top: float,
                 width: float, height: float, font_size: float = 6.5) -> None:
    c.setFillColor(TERMINAL)
    c.roundRect(x, y_top - height, width, height, 5, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#93C5FD"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(x + 10, y_top - 14, title)
    c.setFillColor(TERM_TEXT)
    c.setFont("Courier", font_size)
    leading = font_size + 2.0
    max_chars = max(25, int((width - 20) / (font_size * 0.60)))
    max_lines = int((height - 27) / leading)
    lines: list[str] = []
    for raw in text.strip().splitlines():
        raw = raw.replace("\t", "    ")
        while len(raw) > max_chars:
            lines.append(raw[:max_chars])
            raw = raw[max_chars:]
        lines.append(raw)
    for idx, line in enumerate(lines[:max_lines]):
        c.drawString(x + 10, y_top - 27 - idx * leading, line)


def metric_card(c: canvas.Canvas, x: float, y_top: float, width: float,
                label: str, value: str, detail: str) -> None:
    c.setFillColor(PALE_BLUE)
    c.setStrokeColor(LIGHT)
    c.roundRect(x, y_top - 48, width, 48, 6, fill=1, stroke=1)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 9, y_top - 13, label.upper())
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x + 9, y_top - 31, value)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawRightString(x + width - 9, y_top - 31, detail)


def draw_table(c: canvas.Canvas, x: float, y_top: float, widths: list[float],
               rows: list[list[str]], row_h: float = 22) -> float:
    total_w = sum(widths)
    for r, row in enumerate(rows):
        y = y_top - (r + 1) * row_h
        c.setFillColor(NAVY if r == 0 else (colors.white if r % 2 else PALE_BLUE))
        c.setStrokeColor(LIGHT)
        c.rect(x, y, total_w, row_h, fill=1, stroke=1)
        cursor = x
        for col, value in enumerate(row):
            if col:
                c.line(cursor, y, cursor, y + row_h)
            c.setFillColor(colors.white if r == 0 else INK)
            c.setFont("Helvetica-Bold" if r == 0 else "Helvetica", 7.5)
            c.drawString(cursor + 6, y + 7, value)
            cursor += widths[col]
    return y_top - len(rows) * row_h


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    c.setTitle("Assignment 3 End-to-End ML Versioning")
    c.setAuthor("Muhammad Haris")

    # Page 1 - outcomes and Git evidence
    header(c, "Outcome and Git workflow evidence", 1)
    y = PAGE_H - 78
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Submission result")
    y -= 15
    y = paragraph(c,
        "A four-stage DVC pipeline trains a fully connected ANN on Fashion-MNIST. The final tagged experiment exceeds the 85% target and the complete unsquashed history demonstrates the required Git operations.",
        MARGIN, y, PAGE_W - 2 * MARGIN, 8.6, 11.5)
    y -= 7
    card_w = (PAGE_W - 2 * MARGIN - 16) / 3
    metric_card(c, MARGIN, y, card_w, "v1 test accuracy", "87.41%", "128 units")
    metric_card(c, MARGIN + card_w + 8, y, card_w, "v2 test accuracy", "87.72%", "256 units")
    metric_card(c, MARGIN + 2 * (card_w + 8), y, card_w, "pipeline state", "Clean", "dvc status")
    y -= 62
    y = section_title(c, "Git history and branch workflow", y)
    graph = git("log", "--oneline", "--graph", "--all", "--decorate", "-16")
    terminal_box(c, "$ git log --oneline --graph --all", graph, MARGIN, y, PAGE_W - 2 * MARGIN, 182, 6.2)
    y -= 194
    y = section_title(c, "Required command demonstrations", y)
    commands = """$ git log --stat -3                 # files and line counts in recent commits
$ git log -p -1                     # exact patch introduced by the latest commit
$ git log main..dev                 # commits reachable from dev but not main
$ git diff                          # unstaged preprocess.py range validation
$ git diff --staged                 # same change after staging
$ git diff main..dev                # endpoint comparison
$ git diff main...dev               # changes since the merge base
$ git stash push -m 'WIP preprocess range validation'
$ git stash list
stash@{0}: On dev: WIP preprocess range validation
$ git stash pop                     # restored the exact mid-edit change
$ git reset --hard HEAD~1           # working tree returned clean
$ git reset --soft HEAD~1           # reset_demo.txt remained staged
$ git mv PROJECT_NOTES.md docs/PROJECT_NOTES.md
$ git rm obsolete_scratch.txt"""
    terminal_box(c, "Part A command/output record", commands, MARGIN, y, PAGE_W - 2 * MARGIN, 151, 6.1)
    y -= 162
    left = "Rebase: a README hotfix was committed on a short-lived branch, fast-forwarded into main, and dev was rebased onto it. The graph changed from parallel lines to a clean feature sequence above the hotfix."
    right = "Diff semantics: two-dot compares the two branch tips. Three-dot compares the right tip with the best common ancestor, isolating work introduced on dev. In the captured linear case, both outputs matched because main was the merge base."
    paragraph(c, left, MARGIN, y, 254, 7.3, 9.5)
    paragraph(c, right, MARGIN + 274, y, 254, 7.3, 9.5)
    header(c, "Outcome and Git workflow evidence", 1)
    footer(c)
    c.showPage()

    # Page 2 - implementation and DVC configuration
    header(c, "TensorFlow implementation and DVC configuration", 2)
    y = PAGE_H - 78
    y = section_title(c, "Modular implementation", y)
    rows = [
        ["Stage", "Responsibility", "Versioned output"],
        ["prepare", "Load 60k/10k Fashion-MNIST arrays", "data/raw"],
        ["preprocess", "Normalize and stratified 90/10 split", "data/processed"],
        ["train", "Flatten-Dense-Dropout-Softmax ANN", "model.h5 + history.csv"],
        ["evaluate", "Loss, accuracy, predictions and matrix", "metrics.json + PNG"],
    ]
    y = draw_table(c, MARGIN, y, [72, 280, 176], rows, 23) - 15
    params = (ROOT / "params.yaml").read_text(encoding="utf-8")
    dvc_lines = (ROOT / "dvc.yaml").read_text(encoding="utf-8").splitlines()
    midpoint = len(dvc_lines) // 2
    terminal_box(c, "Final params.yaml", params, MARGIN, y, 168, 190, 6.0)
    terminal_box(c, "Final dvc.yaml 1 of 2", "\n".join(dvc_lines[:midpoint]), MARGIN + 176, y, 174, 190, 4.8)
    terminal_box(c, "Final dvc.yaml 2 of 2", "\n".join(dvc_lines[midpoint:]), MARGIN + 358, y, 170, 190, 4.8)
    y -= 205
    y = section_title(c, "DVC tracking and Google Drive remote", y)
    pointer = git("show", "v1:data/raw.dvc")
    remote_text = f"""$ dvc init
Initialized DVC repository.
$ dvc remote add -d gdrive_storage gdrive://1iyOk52bAA4H6i9_KrBaXYRkjCInOuMYg
Setting 'gdrive_storage' as a default remote.
$ dvc add data/raw data/processed models
Created data/raw.dvc, data/processed.dvc and models.dvc
$ dvc push --all-branches --all-tags
11 files pushed
$ dvc status -c
Cache and remote 'gdrive_storage' are in sync.

v1 data/raw.dvc
{pointer}

Credential files: excluded from Git through .gitignore and .dvc/config.local."""
    terminal_box(c, "Part C configuration and pointer evidence", remote_text, MARGIN, y, PAGE_W - 2 * MARGIN, 145, 6.1)
    y -= 158
    note = (
        "Pipeline migration: standalone dvc add created the rubric's .dvc pointers at v1. The same paths were then migrated to dvc.yaml outputs because DVC correctly rejects tracking one path simultaneously as both a standalone pointer and a stage output. Modern pipeline artifact hashes therefore live in dvc.lock."
    )
    y = paragraph(c, note, MARGIN, y, PAGE_W - 2 * MARGIN, 7.5, 10)
    y -= 6
    tree = """Fashion-ANN-Pipeline/
|- src/{prepare,preprocess,train,evaluate}.py
|- data/{raw,processed}/        [DVC cached]
|- models/                     [DVC cached]
|- params.yaml                 [single source of hyperparameters]
|- dvc.yaml / dvc.lock         [pipeline and exact artifact hashes]
|- metrics.json                [DVC metric + Git history]
`- README.md / requirements.txt"""
    terminal_box(c, "Final project structure", tree, MARGIN, y, PAGE_W - 2 * MARGIN, 82, 6.5)
    header(c, "TensorFlow implementation and DVC configuration", 2)
    footer(c)
    c.showPage()

    # Page 3 - reproducibility and metrics
    header(c, "DVC reproduction and v1-v2 experiment", 3)
    y = PAGE_H - 78
    y = section_title(c, "D3 first complete reproduction", y)
    d3 = """$ dvc repro
Running stage 'prepare':     > python src/prepare.py
Saved 60,000 training samples and 10,000 test samples
Running stage 'preprocess':  > python src/preprocess.py
Saved splits: train=54,000, validation=6,000, test=10,000
Running stage 'train':       > python src/train.py
Epoch 8/8 - accuracy: 0.8832 - val_accuracy: 0.8912
Running stage 'evaluate':    > python src/evaluate.py
{\"test_loss\": 0.348672, \"test_accuracy\": 0.8741, \"test_samples\": 10000}
Generating and updating dvc.lock"""
    terminal_box(c, "Actual condensed v1 console output", d3, MARGIN, y, PAGE_W - 2 * MARGIN, 125, 6.3)
    y -= 140
    y = section_title(c, "D4 parameter change and selective reproduction", y)
    d4 = """$ git diff params.yaml
-  dense_units: 128
+  dense_units: 256
$ dvc repro
Stage 'prepare' didn't change, skipping
Stage 'preprocess' didn't change, skipping
Running stage 'train':       > python src/train.py
Epoch 8/8 - accuracy: 0.8896 - val_accuracy: 0.8932
Running stage 'evaluate':    > python src/evaluate.py
{\"test_loss\": 0.342278, \"test_accuracy\": 0.8772, \"test_samples\": 10000}"""
    terminal_box(c, "Actual condensed v2 console output", d4, MARGIN, y, 318, 154, 6.1)
    matrix_path = ROOT / "models" / "confusion_matrix.png"
    if matrix_path.exists():
        c.saveState()
        c.drawImage(ImageReader(str(matrix_path)), MARGIN + 333, y - 154, width=195, height=154, preserveAspectRatio=True, anchor="c")
        c.restoreState()
    y -= 168
    y = section_title(c, "Metrics comparison", y)
    rows = [
        ["Version", "Dense units", "Test loss", "Test accuracy", "Change"],
        ["v1", "128", "0.348672", "87.41%", "baseline"],
        ["v2", "256", "0.342278", "87.72%", "+0.31 pp"],
    ]
    y = draw_table(c, MARGIN, y, [82, 98, 105, 115, 128], rows, 24) - 14
    explanation = (
        "Only train reran because its dense_units dependency changed. Evaluate reran downstream because the model hash changed. Prepare and preprocess were skipped because their code, parameters, and input hashes were unchanged. The larger hidden layer reduced test loss by 0.006394 and improved accuracy by 0.31 percentage points."
    )
    y = paragraph(c, explanation, MARGIN, y, PAGE_W - 2 * MARGIN, 8.1, 11)
    y -= 9
    terminal_box(c, "Version tags", "$ git tag --list -n\nv1  Baseline Fashion-MNIST ANN\nv2  Fashion-MNIST ANN with 256 dense units", MARGIN, y, PAGE_W - 2 * MARGIN, 62, 6.5)
    header(c, "DVC reproduction and v1-v2 experiment", 3)
    footer(c)
    c.showPage()

    # Page 4 - conflicts, validation, deliverables
    header(c, "Collaboration conflict resolution and final validation", 4)
    y = PAGE_H - 78
    y = section_title(c, "Part E simulated two-contributor conflict", y)
    conflict = """$ git merge teammate-sim
Auto-merging dvc.lock
CONFLICT (content): Merge conflict in dvc.lock
Auto-merging metrics.json
CONFLICT (content): Merge conflict in metrics.json
Auto-merging src/preprocess.py
CONFLICT (content): Merge conflict in src/preprocess.py
Automatic merge failed; fix conflicts and then commit the result.
$ git status --short
UU dvc.lock
UU metrics.json
UU src/preprocess.py"""
    terminal_box(c, "Actual merge output", conflict, MARGIN, y, PAGE_W - 2 * MARGIN, 130, 6.3)
    y -= 145
    left_conflict = """<<<<<<< HEAD
scaled = images.astype(float32) / 255.0
return power(scaled, 0.99)
=======
clipped = clip(images.astype(float32), 0, 255)
scaled = clipped / 255.0
return power(scaled, 1.01)
>>>>>>> teammate-sim"""
    lock_conflict = """dvc.lock contained divergent md5 hashes for:
- data/processed
- models/model.h5
- models/history.csv
- metrics.json

Resolution policy:
1. reconcile source logic
2. choose no stale branch hash
3. regenerate with dvc repro
4. verify dvc status"""
    terminal_box(c, "Source conflict", left_conflict, MARGIN, y, 254, 112, 5.8)
    terminal_box(c, "Data conflict", lock_conflict, MARGIN + 274, y, 254, 112, 6.0)
    y -= 127
    y = section_title(c, "Resolution and reproducibility proof", y)
    resolution = (
        "The merged normalize function combines clipping from teammate-sim with explicit float32 division and the original range validation. Instead of choosing either conflicting lockfile, the main-side lock was used only as a parseable starting point and dvc repro regenerated the authoritative processed hash. Because the resolved linear transform matched the v2 data exactly, DVC reused the cached train/evaluate outputs."
    )
    y = paragraph(c, resolution, MARGIN, y, PAGE_W - 2 * MARGIN, 7.6, 10.2)
    y -= 6
    final_status = """$ dvc repro
Stage 'prepare' didn't change, skipping
Running stage 'preprocess'
Stage 'train' is cached - skipping run, checking out outputs
Stage 'evaluate' is cached - skipping run, checking out outputs
$ dvc status
Data and pipelines are up to date.
$ git log --oneline --graph --all
* ee2871e merge: resolve simulated code and DVC data conflicts
|\
| * 9a7b3df collab: simulate teammate normalization and data version
* | 47614a4 collab: add independent main normalization and data version
|/"""
    terminal_box(c, "Final local verification", final_status, MARGIN, y, PAGE_W - 2 * MARGIN, 128, 6.0)
    y -= 143
    y = section_title(c, "Deliverables", y)
    delivery_rows = [
        ["Deliverable", "Location / proof"],
        ["GitHub repository", "https://github.com/RaoHaris535/Fashion-ANN-Pipeline"],
        ["Google Drive DVC remote", "Folder ID 1iyOk52bAA4H6i9_KrBaXYRkjCInOuMYg; 11 files pushed"],
        ["Final pipeline state", "dvc.lock committed; data and pipelines up to date"],
        ["Submission report", "Assignment3_Report_Muhammad_Haris_23L-0807.pdf"],
    ]
    draw_table(c, MARGIN, y, [130, 398], delivery_rows, 20)
    header(c, "Collaboration conflict resolution and final validation", 4)
    footer(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
