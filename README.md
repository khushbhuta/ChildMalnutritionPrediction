# ChildMalnutritionPrediction

LoP under Prof. Subhrakanta Panda

# Anthrovision Dataset – Setup Guide

This README explains how to download, extract, and organize the **Anthrovision Dataset (IIT Jodhpur)** so it matches the expected project directory structure.

---

## 1. Dataset Download

- Dataset source: **Anthrovision Dataset (IIT Jodhpur)**
- Download link: https://iab-rubric.org/resources/healthcare-datasets/anthrovision-dataset

**Steps:**

1. Open the link above.
2. Scroll to the **bottom of the page**.
3. Click **"Click here to download"**.

---

## 2. Extracting the Dataset

- The downloaded file will be a **`.rar` archive**.
- Extract the `.rar file **in the same directory** where it is downloaded.
- Use the following passkey when prompted:

Passkey : anthro123

---

## 3. Expected Directory Structure

After successful extraction and setup, your project directory should look like this:

LoP/
│
├── Analytics Engine/
│ └── metadata.csv
│
└── Anthrovision Dataset/
└── fulldataset/
├── frontal1/
├── frontal2/
├── frontal3/
├── frontal4/
├── back/
├── lateralleft/
├── lateralright/
├── selfie/
└── handswide/

---

## 4. Notes

- Ensure that **all image folders** are present inside the `fulldataset/` directory.
- Do **not rename** any folders, as downstream code may rely on these exact names.
- The `metadata.csv` file should be placed inside the `Analytics Engine/` directory.

---

You are now ready to use the Anthrovision Dataset for analysis or model development.
