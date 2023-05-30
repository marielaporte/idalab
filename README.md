# Idalab Data Engineer Case-Study

This README provides all technical information you need to complete this case study.

## ICUZen 

ICUZen was developed in collaboration with the physicians from the hospital.
It is implemented with only one dependency namely `numpy`.
ICUZen has two methods `predict` and `predict_proba`. 
`predict` returns a boolean stating if an alarm should be thrown under the given threshold and sensitivity.
`predict_proba` returns the score before the classification threshold was applied.

The model's predict methods take the same vital signs as arguments. 
For more details please read the methods docstrings.

You can simply import and use the model if your python environment has numpy installed.
