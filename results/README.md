# Results

This folder contains experiment results, model outputs, and evaluation metrics from the Child Malnutrition Prediction project.

## Contents

This directory is used to store:

- **Model Predictions**: Output files from trained models
- **Evaluation Metrics**: Performance metrics (accuracy, precision, recall, F1-score, etc.)
- **Visualizations**: Plots, charts, and graphs generated during analysis
- **Experiment Logs**: Records of different experimental runs and their parameters

## Usage

When running experiments or training models, save the output files in this directory with descriptive names that include:
- Model name
- Date/timestamp
- Key parameters or configuration details

Example naming convention:
- `xgboost_predictions_2025-12-18.csv`
- `multiview_model_metrics_v2.json`
- `height_gender_regression_plot.png`

## Note

This folder is tracked in git to maintain the project structure. Add large result files to `.gitignore` if they exceed GitHub's file size limits.
