# goldchen
Python Version 3.8.5 64bit 

libraries to install beforehand:
skikit-image    Version 0.17.2
opencv-python   Version 4.5.2.52
scikit-learn    Version 0.24.1

commands to install the above libraries:
pip install skikit-image
pip install opencv-python
pip install scikit-learn


Command format:  Main.py n samples scale
n is an integer that represents the height and width of grid in cell count
samples is the number of samples for the trainind data, recommended to not be more than 250
scale is the exponential scale for the costs

Command with values used for our results:
Main.py 10 100 4

Note: Since the training data is randomly generated, the numerical results obtained cannot be reproduced, but the general trends will remain
regardless of how the randomization takes place.
