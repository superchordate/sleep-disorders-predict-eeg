**pytorch\a-process-edf-testtrain.py**
Converts EDF files into parquet files that can be read into the model.
* Selects observations to be in train, validation, and holdout sets.
* Creates data splits. Turn this feature off by splitting to 1 dataset.
* Idea: split into distinct segments instead of randomly sampling the beginning of each split.
* Keeps splits of observations together so a split from holdout doesn't get used in training, for example.

**pytorch\b-data-loader.py**
Data loaders for the model training to use.

**pytorch\c-model.py**
Model training including defining neural network layers.
* Uses validation data to check generalization, bias/variance.

**pytorch\d-‌holdout-test-rollup.py**
Roll up predictions on splits into a prediction for observations in the holdout set.