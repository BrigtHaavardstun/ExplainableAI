# ExplainableAI
This projects holds software used to generate teaching sets for the paper "XAI with Machine Teaching when Humans Are (Not) Informed about the Irrelevant Features" by Brigt Arve Toppe H åvardstun, Cèsar Ferri, Jose Hernández-Orallo,
Pekka Parviainen, and Jan Arne Telle. The paper can be found at [http://www.ii.uib.no/~telle/bib/HFHPT.pdf](http://www.ii.uib.no/~telle/bib/HFHPT.pdf).

# A tutorial

 If you follow each step you can choose an boolean function, generate new random training data, train a new Convolutional Neural Network and find the optimal* teaching set for this CNN.

 *Optimal in the sence that the Learner defined in the paper and implemented in this code gets the best score for the given teaching set. A combination of the size of the teaching size, and how well the learners choosen boolean formula fits the AI.

<a id='creating-conda'></a>
## Setting up the correct envoriment
<a id='install-conda'></a>
 Step 1: Install Conda (pip might work also, but tested for conda). See the guide at [this page](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
 
<a id='create-new-conda'></a>
 Step 2: Create a new conda enviorment
```console
foo@bar:ExplainableAI$ conda env create -f environment.yml --name ExplainableAIVenv
```
or if you want to use pip
```console
foo@bar:ExplainableAI$ pip install -r requirements_pip.txt
```
<a id='activate-conda'></a>
 Step 3: Activate the enviorment
```console
foo@bar:ExplainableAI$ conda activate ExplainableAIVenv
```

<a id='activate-the-jupyter-notebook'></a>
## Activate the juptyer notebook

```console
(ExplainableAIVenv) foo@bar:ExplainableAI$ jupyter notebook tutorial.ipynb
```

 Once you mangage to open this file in juptyer notebook we will continue from this notebook.