# Assignment 5 – CO5
## Data Acquisition, Cleaning, Analysis and AI Applications

**Course:** Python Programming – CSA08  
**Course code:** CSA0803  
**Student:** Deepika Gopu  
**Register number:** 1911260133

This repository contains a runnable Python project organized by task, a small synthetic air-quality dataset, requirements, and the assignment report.

## Repository structure

```text
CSA08_Assignment5/
├── data/
│   └── air_quality_sample.csv
├── tasks/
│   ├── task1_data_cleaning/
│   │   └── cleaning.py
│   ├── task2_analysis/
│   │   └── analysis.py
│   ├── task3_adversarial_tests/
│   │   └── adversarial_tests.py
│   └── task4_ai_applications/
│       └── ai_applications.py
├── evidence/
│   └── README.md
├── report/
│   └── Deepika_Gopu_Assignment5.pdf
├── assignment5_complete.py
├── requirements.txt
└── README.md
```

## Setup

Python 3.10 or later is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the complete demonstration

From the repository root:

```bash
python assignment5_complete.py
```

The script reads `data/air_quality_sample.csv`, validates and cleans rows, writes a SQLite database to `output/air_quality.db`, generates four charts in `output/charts/`, runs adversarial-input checks, demonstrates sentiment scoring and extractive summarisation, and prints benchmark/profile information.

## Run individual task files

```bash
python tasks/task1_data_cleaning/cleaning.py
python tasks/task2_analysis/analysis.py
python tasks/task3_adversarial_tests/adversarial_tests.py
python tasks/task4_ai_applications/ai_applications.py
```

The task scripts are standalone teaching demonstrations. The main integrated entry point is `assignment5_complete.py`.

## Dataset and interpretation

`data/air_quality_sample.csv` is a small **synthetic** teaching dataset. It includes valid and deliberately invalid PM2.5 values to demonstrate missing-value, range, and parsing checks. The charts and benchmark data are illustrative, not measured city pollution data.

The report's benchmark numbers and screenshots are reported in the supplied assignment PDF. They should not be represented as fresh measurements from your computer. Run the project locally and capture your own terminal/chart evidence if your instructor requires machine-specific execution screenshots.

## Notes

- Invalid rows are rejected with a reason rather than silently changed.
- Fahrenheit temperatures are converted to Celsius for Guindy and Velachery in the demonstration.
- SQL statements use parameter placeholders (`?`) for user-supplied values.
- The PM2.5 upper bound of 999 is only a demonstration threshold, not a universal sensor limit.
- The assignment PDF notes that some adversarial cases (such as duplicate keys, malformed quoting, and non-numeric PM2.5) need additional local test evidence before claiming full test coverage.
