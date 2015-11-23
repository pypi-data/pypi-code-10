import random

import bosses
import dogs

human_beings = []                # Create an emptpy list
for index in range (10):         # Repeat the following 10 times, index running from 0 to 9
    human_beings.append (        # Append a random human being to the list by
        random.choice ((bosses.NatureLover, bosses.CouchPotato)) () # randomly selecting its class
    )                                                               # and calling its contructor

# Let them all walk a new dog with a random sound
for human_being in human_beings: # Repeat the following for every human being in the list
    human_being.walk (           # Call implementation of walk method for that type of human being
        dogs.Dog (               # Construct a dog as parameter to the walk method
            random.choice (      # Pick a random sound
                ('Wraff', 'Wooff', 'Howl', 'Kaii', 'Shreek') # fom this tuple of sounds
            )
        )
    )