# Face to BMI Estimation

## Objective
Give a human's face image , identify BMI of the individual.

## Instruction for Running Prediction
1. Specify full prediction image path at `config.py` under `prediction config`.
2. In command line, run `python main.py`.
3. Input `y` for the question prompted.

## Instruction for Training New BMI Model
1. Navigate to `config.py` and update all the required configuration under `training config`.
2. In command line, run `python main.py`.
3. Input `n` for the first question.
4. Input `y` for the second question.

## Project Description
Model used for the project is **Random Forest Generator** from sklearn.
Initial training data contained **217** images from **22** celebrities of different ethnicity, height and weight. Images of the individuals are publicly accessible. BMI of those are calculated from height and weight.
Face image must be used for best result.

## Latest Model
The latest model was trained on November 15, 2020.
```
Model Performance
Average Error: 0.0521
Accuracy = 98.39%.
```
