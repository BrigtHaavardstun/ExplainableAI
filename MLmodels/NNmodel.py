class model:
    def __init__(self, boolFunc, labelData, images) -> None:
        self.boolFunc = boolFunc   




"""
Below is testing to get used to generate NNs
"""

from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
print("making regression...")
X, y = make_classification(n_samples=100, random_state=1)
print("test train split")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,random_state=1)
print("trainging")
clf = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)
print("predicting")
print(clf.predict_proba(X_test[:1]))
print(clf.predict(X_test[:5, :]))
print("scoring")
print(clf.score(X_test, y_test))
