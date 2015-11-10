import random   # One of Python's many standard modules

import bosses
import dogs

humanBeings = [                                  # Start a so called list comprehension
    random.choice (                              # Pick a random class
        (bosses.NatureLover, bosses.CouchPotato) # out of this tuple
    ) ()                                         # and call its constructor to instantiate an object
    for index in range (10)                      # repeatedly, while letting index run from 0 to 9
]                                                # End the list comprehension, it will hold 10 objects

# Let them all walk a new dog with an random sound
for humanBeing in humanBeings:  # Repeat the following for every humanBeing in the list
    humanBeing.walk (           # Call implementation of walk method for that type of humanBeing
        dogs.Dog (              # Construct a dog as parameter to the walk method
            random.choice (     # Pick a random sound
                ('Wraff', 'Wooff', 'Howl', 'Kaii', 'Shreek') # fom this tuple of sounds
            )
        )
    )