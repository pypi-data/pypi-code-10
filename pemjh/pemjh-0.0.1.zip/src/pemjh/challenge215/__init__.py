""" Challenge215 """


def buildRowOptions(start, end):
    options = list()
    if (end - start == 2):
        # Only a 2 can fit
        options.append([])
    elif (end - start == 3):
        # only a 3 can fit
        options.append([])
    elif (end - start == 4):
        # only two 2s can fit
        options.append([start + 2])
    elif (end - start == 5):
        # only 2 and 3 or 3 and 2 can fit
        options.append([start + 2])
        options.append([start + 3])
    else:
        # 2 next
        for remainder in buildRowOptions(start + 2, end):
            options.append([start + 2] + remainder)
        # 3 next
        for remainder in buildRowOptions(start + 3, end):
            options.append([start + 3] + remainder)
    return options


def runningCrack(row1, row2):
    for crack in row1:
        if crack in row2:
            return True
    return False


def W(startRow, depth, data, known=dict()):
    key = (startRow, depth,)

    if key not in known:
        num = 0
        if depth == 2:
            num = len(data[startRow])
        else:
            for subRow in data[startRow]:
                num += W(subRow, depth - 1, data)

        known[key] = num

    return known[key]


def challenge215():
    """ challenge215 """
    # Get possible rows
    wallWidth = 32
    wallHeight = 10

    rowLinks = dict()
    rows = buildRowOptions(0, wallWidth)
    rows = [tuple(row) for row in rows]
    for row in rows:
        linked = list(subRow for subRow in rows
                      if not runningCrack(row, subRow))
        if len(linked) > 0:
            rowLinks[row] = linked

    return sum(W(row, wallHeight, rowLinks) for row in rows)
