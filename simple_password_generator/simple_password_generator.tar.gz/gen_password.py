#!/usr/bin/python
# ~*~ coding: utf8 ~*~
# ~*~ pep - 8 ~*~
#####################


import random
import argparse


class PasswordChooser(object):

    """Very simple passwords generator class."""

    def __init__(self, length):
        # get the wanted length.
        self.length = length
        # build list of uppers + lowers letterd
        from string import ascii_lowercase, ascii_uppercase
        self.letters = list(ascii_lowercase) + list(ascii_uppercase)
        # shuffle it.
        random.shuffle(self.letters)

    def _number_generate(self):
        """generate random integer between 1 to 9. """
        return random.randint(1, 9)

    def generate_password(self):
        """Generate random password. """

        # Initial needed variables:
        ready = 0
        potential_password = list()
        # run till we reach the length of the wanted password.
        while ready != self.length:
            # if the list is empty (it dose at the first enter)
            if not potential_password:
                # fill the first letter uppercased.
                letter = random.choice(self.letters)
                potential_password.append(letter.upper())
            # if not the first time.
            else:
                # random a number: if even number:
                if self._number_generate() % 2 == 0:
                    # load letter (upper or lower.)
                    potential_password.append(random.choice(self.letters))
                # if odd number
                else:
                    # load number.
                    potential_password.append(self._number_generate())
            # raise the ready and continue.
            ready += 1

        # finish the while, `concate` the list to be apropriate string.
        password = ''.join(map(str, potential_password))

        # section 2: avoiding all letters to be upper (all lower is unreachable)
        letters = list()
        # fetching all the letters.
        for c in password:
            if not c.isdigit():
                letters.append(c)
        # if the list of the letters size is in the len of list of upper letter:
        # all the letters are upper.
        if len([c for c in letters if c.istitle()]) == len(letters):
            # catch the 1st letter and lower it.
            for index, c in enumerate(potential_password):
                if isinstance(c, str) and index != 0:
                    potential_password[index] = c.lower()
                    break
            # re join the list and send the ready password.
            password = ''.join(map(str, potential_password))
            return password
        else:
            return password


if __name__ == '__main__':
    # Parse Args CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", type=int, required=True,
                        help="requested password length")
    user_input = parser.parse_args()
    if user_input.length < 8 and user_input.length > 5:
        print '\033[91m [[ We recommended to use atleast password with length of 8 ]] \033[0m'
    elif user_input.length <= 5:
        raise Exception('\033[91m Password length is too short. \033[0m')

    ps = PasswordChooser(user_input.length)
    password = ps.generate_password()
    print """======= Generated Password =======
             \033[92m {password} \033[0m
          """.format(password=password)
    print "=================================="
