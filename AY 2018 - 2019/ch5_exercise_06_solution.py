#!/usr/bin/python3
# -*- coding: utf-8 -*-


'''
@author: Pieter
Pieter.Huycke@UGent.be

- - - - - - - - - - - - 

Stuck using a function?
No idea about the arguments that should be defined?

Type:
help(function_name)
to let Python help you!
'''


import matplotlib.pyplot          as     plt
import numpy                      as     np
from   sklearn.metrics            import accuracy_score
from   sklearn.model_selection    import train_test_split
from   sklearn.neural_network     import MLPClassifier
from   sklearn                    import datasets


#%%
'''
* GENERAL EXPLANATION *

In this code, we are going to train a simple Stroop model
You are going to implement this yourself.
However, as we are aware that the learning curve might be a bit steep, we will
provide some hints to get you started.

The paradigm of a Stroop task is simple:
A participant sits in front of a computerscreen, and sees a sequence of English
colorwords (in written format). A cue presented prior to the word tells the 
participant to what dimension one should respond. Two response dimensions are 
available: the word itself, and the color of the word.
If the color of the word and the written format match (e.g. RED written in a 
red color), then a congruency effect will occur. Alternatively, if color and 
word do not match (e.g. GREEN written in red), participants become slower.

To keep things simple, we will only look at two words and two colors.
You can imagine this as a Stroop task where participants see the words 'GREEN'
and 'RED', written in the colors green and red.
The cue that indicates to which dimension the subjects have to respond is also
binary: a subject should either react to the word itself, or to the color.

In other words, we have three dimensions that can take two different values:
    - color of the word
    - written form
    - cue that represents the relevant dimension
Given this, we know that we will need 6 input units (three dimensions with each
two possible values).
By doing so, we can represent every possible input that our participant might
see.

How many output units do we need?
Know that we have two response dimensions: "It's green" and "It's red"
What the participant thinks is often measured by key presses (e.g. press right
if the answer is 'green').
We actually only need one output unit: this is enough to represent 
every possible outcome
Why? To show you that every binary representation can be represented by a single
unit that can two values
In other words: our model could also be created with three input units and a single
output unit
We made it more intuitive though by "smearing out" the inputs, now we can see 
which units are active, and which are not active, and what this represents

For convenience, we will fix the cue units: this means that the participants 
always have to respond to the same stimulus dimension.
Fixing the cue unit is the same as me saying to the participant 'you should
only respond to the color of the shown word.'
'''



'''
* TWO RELEVANT STIMULUS DIMENSIONS *

In the following, we will create data for a model where the participant has to
switch tasks. 
In other words, the first two units will have different activation patterns
(while they were fixed previously).
Try to use Delta learning to configure a correct set of weights.
See whether this works out.
If not, use backpropagation to configure a set of weights which can solve the 
problem.
'''

# 'focus on color'
red_red_color     = [0, 1, 0, 1, 0, 1] # Answer should be: 'red'
green_green_color = [0, 1, 1, 0, 1, 0] # Answer should be: 'green'
red_green_color   = [0, 1, 0, 1, 1, 0] # Answer should be: 'red'
green_red_color   = [0, 1, 1, 0, 0, 1] # Answer should be: 'green'

# 'focus on the word'
red_red_word      = [1, 0, 0, 1, 0, 1] # Answer should be: 'red'
green_green_word  = [1, 0, 1, 0, 1, 0] # Answer should be: 'green'
red_green_word    = [1, 0, 0, 1, 1, 0] # Answer should be: 'green'
green_red_word    = [1, 0, 1, 0, 0, 1] # Answer should be: 'red'

response_1, response_2, response_3, response_4 =  [1], [-1],  [1], [-1]
response_5, response_6, response_7, response_8 =  [1], [-1], [-1],  [1]

# Bundle them together
all_possible_inputs  = np.array([red_red_color, green_green_color, red_green_color, green_red_color,
                                 red_red_word,  green_green_word,  red_green_word,  green_red_word])
all_possible_outputs = np.array([response_1, response_2, response_3, response_4, 
                                 response_5, response_6, response_7, response_8])

# Amount of possible inputs
length_inputs = len(all_possible_inputs)
    
# Repeat every possible input pattern 50 times
inputted_patterns    = np.tile(all_possible_inputs,  (length_inputs * 50, 1))
outputs              = np.ravel(np.tile(all_possible_outputs, (length_inputs * 50, 1)))

# The strings associated with our possible outcomes
# Here, only two labels are possible ('red', and 'green')
class_names = ['Red', 'Green']

n_hid = 50 # number of iterations across hidden layer size
accuracy_vector = np.zeros(n_hid)

'''
* TWO RELEVANT STIMULUS DIMENSIONS *
* BACKPROPAGATION *

Train the model that incorporated different tasks
Now, implemented an extra hidden layer with 4 units, and use backpropagation
to alter the weight matrix
'''

np.set_printoptions(precision=2)
# import the Iris flower dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

for hid_loop in range(n_hid):
    # split data in training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y)

    mlp = MLPClassifier(hidden_layer_sizes=(hid_loop+1,), 
                    max_iter=100,
                    solver='sgd', 
                    verbose=0, 
                    random_state=2020,
                    learning_rate_init=.1, 
                    activation='logistic')

    # fit  classifier to the training data
    mlp.fit(X_train, y_train)

    y_pred = mlp.predict(X_test)
    accuracy_vector[hid_loop] = accuracy_score(y_test, y_pred)
    
plt.plot(range(n_hid), accuracy_vector)    