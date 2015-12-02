""" Challenge101 """


def challenge101():
    """ challenge101 """
    highestPower = 10

    # Get correct sequence
    sequence = [1 - i + i**2 - i**3 + i**4 - i**5 + i**6 - i**7 + i**8 -
                i**9 + i**10 for i in xrange(1, highestPower + 2)]

    incorrect = 0

    # Loop through powers to work out, start at 0 up to highestPower
    for power in xrange(highestPower + 1):
        # Create a sequence using the values
        # in the sequence up to power to extrapolate from

        workedSequence = list()

        for x in xrange(1, highestPower + 2):
            y = 0
            for index, value in enumerate(sequence[:power + 1]):
                # Work out the numerator and denomintaor for this value
                numerator = value
                denominator = 1
                if power != 0:
                    for diff in xrange(1, power + 2):
                        if diff != (index + 1):
                            numerator *= (x - diff)
                            denominator *= ((index + 1) - diff)

                y += numerator / denominator

            workedSequence.append(y)

        # Get first value that differs from sequence
        for correct, potential in zip(sequence, workedSequence):
            if correct != potential:
                incorrect += potential
                break

    return incorrect
