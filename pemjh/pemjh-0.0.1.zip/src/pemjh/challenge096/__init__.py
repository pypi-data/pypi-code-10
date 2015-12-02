""" Challenge096 """
from __future__ import with_statement
from os.path import abspath, dirname
import copy


def sortSquareLengths(a, b):
    la = len(a[0])
    lb = len(b[0])
    if la > lb:
        return 1
    elif la == lb:
        return 0
    else:
        return -1


class SGrid:

    __rows = None

    def __init__(self, s):
        # Setup 81 squares
        square = range(1, 10)
        row = [[copy.deepcopy(square), False] for _ in xrange(9)]
        self.__rows = [copy.deepcopy(row) for _ in xrange(9)]

        # Add row and column data...
        # for r in xrange(9):
        #    for c in xrange(9):
        #        self.__rows[r][c].append([r, c])

        # Load in data
        self.__loadData(s)

        self.__solve()

    def __loadData(self, s):
        # 9 rows of input data, read into rows

        # Loop through rows
        for r, row in enumerate(s):
            # Loop through columns
            for c, value in enumerate(row):
                if value != "0":
                    self.__setValue(r, c, int(value))

    def __getBox(self, r, c):
        def getStartIndex(i):
            if i < 3:
                return 0
            elif i < 6:
                return 3
            else:
                return 6

        rowStart = getStartIndex(r)
        for row in xrange(rowStart, rowStart + 3):
            columnStart = getStartIndex(c)
            for column in xrange(columnStart, columnStart + 3):
                yield self.__rows[row][column]

    def __removeValueFromList(self, l, value):
        nRemoved = 0

        for sq in l:
            if value in sq[0]:
                nRemoved += 1
                sq[0].remove(value)

        return nRemoved

    def __setValue(self, r, c, value):
        # Remove value from rest of row r
        self.__removeValueFromList(self.__rows[r], value)

        # Remove value from rest of column c
        self.__removeValueFromList([self.__rows[i][c] for i in xrange(9)],
                                   value)

        # Get the box
        box = list(self.__getBox(r, c))

        # Remove value from rest of box
        self.__removeValueFromList(box, value)

        # Remove all but value from square
        sq = self.__rows[r][c]
        for rem in xrange(1, 10):
            if rem != value and rem in sq[0]:
                sq[0].remove(rem)

        # Set square to the value
        sq[0].append(value)
        sq[1] = True

        return

    def __getAllBlocks(self):
        blocks = []
        blocks.extend(self.__rows)
        blocks.extend([[self.__rows[i][j] for i in xrange(9)]
                       for j in xrange(9)])
        for r in xrange(0, 9, 3):
            for c in xrange(0, 9, 3):
                box = list(self.__getBox(r, c))
                blocks.extend([box])

        return blocks

    def __processCompletedSquares(self):
        changes = False
        # Cycle through the rows and find any single value squares that
        # aren't True
        for r in self.__rows:
            for sq in r:
                if len(sq[0]) == 1 and not sq[1]:
                    self.__setValue(self.__rows.index(r),
                                    r.index(sq),
                                    sq[0][0])
                    changes = True
        return changes

    def __processGroups(self):
        changes = False

        # Loop through each block (row, column, box) and check for sets of
        # numbers that are the same. Remove these numbers from all others in
        # the list
        blocks = self.__getAllBlocks()

        for block in blocks:
            for sq in block:
                # Get each square that is longer than 1
                if len(sq[0]) > 1:
                    # Count qty in the block that are the same
                    identical = [sq2 for sq2 in block if sq[0] == sq2[0]]
                    # If count matches length then remove the values from all
                    # non-matching squares
                    if len(identical) == len(sq[0]):
                        lSq = len(sq[0])
                        # Store values
                        stored = copy.copy(sq[0])

                        # Remove from list
                        for val in stored:
                            nRemoved = self.__removeValueFromList(block, val)
                            if nRemoved != lSq:
                                changes = True

                        # Reinstate in identicals
                        for val in stored:
                            for sq2 in identical:
                                sq2[0].append(val)

        return changes

    def __getLocation(self, sq):
        # Find the containing row
        for r, row in enumerate(self.__rows):
            for c, sq2 in enumerate(row):
                if sq is sq2:
                    return [r, c]

        return None

    def __processOnlyInOneSquare(self):
        changes = False

        # Get the blocks
        blocks = self.__getAllBlocks()

        for block in blocks:
            for i in xrange(1, 10):

                # Get the squares that contain this number
                containers = [sq for sq in block if i in sq[0] and not sq[1]]
                if len(containers) == 1:
                    # Set the value in this square
                    location = self.__getLocation(containers[0])
                    self.__setValue(location[0], location[1], i)
                    changes = True

        return changes

    def __copy(self, source):
        # Loop through the rows
        for sRow, tRow in zip(source.__rows, self.__rows):
            for sSquare, tSquare in zip(sRow, tRow):
                tSquare[0] = sSquare[0]
                tSquare[1] = sSquare[1]

    def __solve(self):
        progressMade = True

        while progressMade:
            progressMade = self.__processCompletedSquares()

            progressMade = progressMade or self.__processGroups()

            progressMade = progressMade or self.__processOnlyInOneSquare()

        if not self.solved():
            # Find square with multiple options
            unsolvedSquares = []
            for r in self.__rows:
                for c in r:
                    if len(c[0]) == 0:
                        return
                    if len(c[0]) > 1:
                        unsolvedSquares.append(c)

            unsolvedSquares.sort(sortSquareLengths)

            for sq in unsolvedSquares:
                loc = self.__getLocation(sq)
                for val in sq[0]:
                    # Create a clone
                    clone = copy.deepcopy(self)
                    # Set value
                    clone.__setValue(loc[0], loc[1], val)
                    if clone.valid():

                        clone.__solve()

                        if clone.solved():

                            # Set self to the same as clone
                            self.__copy(clone)

                            return

    def valid(self):
        for r in self.__rows:
            for sq in r:
                if len(sq[0]) == 0:
                    return False
        return True

    def solved(self):
        for r in self.__rows:
            for sq in r:
                if len(sq[0]) != 1:
                    return False
        return True

    def __int__(self):
        if not self.solved():
            return 0

        return sum(self.__rows[0][i][0][0] * 10**(2 - i) for i in xrange(3))

    def __repr__(self):
        repr = []
        for r in self.__rows:
            row = []
            for sq in r:
                # concat the square
                f1 = "(" if sq[1] else ""
                f2 = ")" if sq[1] else ""

                row.append(f1 + "".join(str(c) for c in sq[0]) + f2)
            repr.append("\t".join(row))
        return "SGrid\n" + "\n".join(repr)


def challenge096():
    """ challenge096 """
    with open("%s/sudoku.txt" % dirname(abspath(__file__))) as f:

        total = 0

        # Read blocks of 10 lines for each puzzle
        for _ in xrange(50):
            # Read header line
            f.readline()
            # Read next 9 lines into a list
            input = [f.readline().strip() for _ in xrange(9)]

            ans = SGrid(input)

            total += int(ans)

        return total
