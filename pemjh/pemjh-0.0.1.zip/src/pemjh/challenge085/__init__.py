""" Challenge085 """


def num_rects(height, width):
    """ Number of rectangles that fit """
    count = 0
    for rectangle_height in xrange(1, height + 1):
        for rectangle_width in xrange(1, width + 1):
            num_across = width - rectangle_width + 1
            num_down = height - rectangle_height + 1
            count += num_across * num_down

    return count


def challenge085():
    """ challenge085 """
    width = 1
    target = 2000000
    closest = target  # ie 0
    area = 0
    while True:
        # Get rectangles for width 1
        rectangles = num_rects(1, width)
        # If greater than 2 million and further away than closest
        if rectangles > target and abs(target - rectangles) > closest:
            # Will never improve
            break
        else:
            # use triangle numbers to find the closest to 2000000
            triangle = 0
            height = 1
            while True:
                triangle += height

                # Get difference
                area_rectangles = rectangles * triangle
                difference = abs(target - area_rectangles)

                if difference < closest:
                    closest = difference
                    area = width * height

                if area_rectangles > target:
                    break  # Cannot improve

                height += 1

        width += 1

    return area
