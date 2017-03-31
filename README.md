# language-detector-python

## Description
### English
Simple language detector with corpus. Implementation with Python. Predicts the language of a specified <code>.txt</code>.
### Spanish
Simple detector de lenguaje con corpus. Implementación con Python. Predice el lenguaje de un documento <code>.txt</code> dado.

## Installation
* <code>sudo apt-get install python3 python3-numpy python3-pip</code>
* <code>pip3 install -r pip-requirements.txt</code>
* <code>python3 download-nltk.py</code>
  * Download tokenizers and Punkt data.
  
## Running
* <code>python3 main.py</code>
* Type target corpus to predict language.

## Preprocessing
Already ready. If you want to change the set of languages for the prediction, you'll have to dive in the code and give a supporting corpus.
* <code>python3 preprocessing.py</code>
* Then rename the target <code>.pkl</code> to <code>data.pkl</code>.
