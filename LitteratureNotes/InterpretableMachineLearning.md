##  Notes on Interpretable Machine Learning
### A guid fo rMaking Black Box Models Explainable
#### Author Christoph Molnar
#### 2019-09-21

## citing
Molnar, Christoph. "Interpretable machine learning. A Guide for Making Black Box Models Explainable", 2019. https://christophm.github.io/interpretable-ml-book/.




# Chapter 1: Interpretabiliy
We want to achive global, model-agnositic, post-hoc interpretability.

Global: It says something about the system as a whole system, not individual predictions.
Model-agnositic: Can be used on any ML system, not just e.g. NN

Human-friendly explanations: max 3 reasons; 2 cases in, 1 out. Context e.g. who gets the explinations is important.

## Linear Regression
We can easily interpret the weights to argue how the modle predicts. This is positive as it makes the modle interpretable. If the dataset we have has a lot of features, we could use "lasso" to select a subset of the features s.t. the prediction still are rather good, and fewer features == easier to understand.

