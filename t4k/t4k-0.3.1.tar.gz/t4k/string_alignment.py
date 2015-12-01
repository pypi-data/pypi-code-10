import t4k

def string_distance(s1, s2):
	sa = StringAligner()
	return sa.string_distance(s1, s2)

def string_align(s1, s2):
	sa = StringAligner()
	distance, path = sa.string_alignment(s1, s2)
	return distance, path

def string_align_masks(s1, s2):
	sa = StringAligner()
	mask1, mask2 = sa.get_string_alignment_masks(s1, s2)
	return 

def string_align_path(s1, s2):
	sa = StringAligner()
	return sa.get_string_alignment_path(s1, s2)


class StringAligner(object):

	UP = 1
	LEFT = 2
	DIAG = 3

	DELETE = 'd'
	INSERT = 'i'
	MATCH = 'm'
	SUBSTITUTE = 's'

	def string_alignment(self, name1, name2):
		distance = [
			[None for j in range(len(name2)+1)] for i in range(len(name1)+1)
		]
		path = [
			[None for j in range(len(name2)+1)] for i in range(len(name1)+1)
		]

		for i in range(len(name1) + 1):
			for j in range(len(name2) + 1):

				# The word boundary matches
				if i == 0 and j == 0:
					distance[i][j] = 0
					path[i][j] = self.DIAG
					continue

				# match character i and j
				match_dist = None
				if i > 0 and j > 0:
					if name1[i-1] == name2[j-1]:
						match_dist = distance[i-1][j-1]

					# substitute character i by char j
					else:
						match_dist = distance[i-1][j-1] + 2

				# Delete one char from name1
				del_dist = None
				if i > 0:
					del_dist = distance[i-1][j] + 1

				# Insert one char from name2
				insert_dist = None
				if j > 0:
					insert_dist = distance[i][j-1] + 1

				distance[i][j] = t4k.safe_min(
					match_dist, del_dist, insert_dist)

				if t4k.safe_lte(match_dist, del_dist):
					if t4k.safe_lte(match_dist, insert_dist):
						path[i][j] = self.DIAG
					else:
						path[i][j] = self.LEFT

				elif t4k.safe_lte(del_dist, insert_dist):
					path[i][j] = self.UP

				else:
					path[i][j] = self.LEFT

		return distance, path



	def string_distance(self, name1, name2):
		distance, path = self.string_alignment(name1, name2)
		return distance[-1][-1]



	def get_string_alignment_masks(self, name1, name2):
		distance, path = self.string_alignment(name1, name2)

		alignment1 = [None for p in range(len(name1))]
		alignment2 = [None for q in range(len(name2))]
		i = len(name1)
		j = len(name2)
		while i > 0 or j > 0:
			if path[i][j] == self.UP:
				i -= 1
				alignment1[i] = 0
				continue

			if path[i][j] == self.LEFT:
				j -= 1
				alignment2[j] = 0
				continue

			if path[i][j] == self.DIAG:
				i -= 1
				j -= 1
				if distance[i][j] == distance[i+1][j+1]:
					alignment1[i] = 1
					alignment2[j] = 1
				else:
					alignment1[i] = 0
					alignment2[j] = 0

		return alignment1, alignment2


	def get_string_alignment_path(self, name1, name2):
		distance, path = self.string_alignment(name1, name2)

		linear_path = []
		i = len(name1)
		j = len(name2)
		while i > 0 or j > 0:
			if path[i][j] == self.UP:
				i -= 1
				linear_path.append(self.DELETE)
				continue

			if path[i][j] == self.LEFT:
				j -= 1
				linear_path.append(self.INSERT)
				continue

			if path[i][j] == self.DIAG:
				i -= 1
				j -= 1
				if distance[i][j] == distance[i+1][j+1]:
					linear_path.append(self.MATCH)
				else:
					linear_path.append(self.SUBSTITUTE)

		linear_path.reverse()
		return linear_path


	def display_string_alignment(self, name1, name2):
		alignment1, alignment2 = self.get_string_alignment_masks(
			name1, name2
		)

		i = 0
		j = 0
		display1 = []
		display2 = []
		display = []
		while i < len(name1) or j < len(name2):

			if i >= len(name1):
				display1.append('-')
				display2.append(name2[j])
				display.append(' ')
				j += 1
				continue

			if j >= len(name2):
				display1.append(name1[i])
				display2.append('-')
				display.append(' ')
				i += 1
				continue

			if alignment1[i]:
				if alignment2[j]:
					display1.append(name1[i])
					display2.append(name2[j])
					display.append('|')
					i += 1
					j += 1

				else:
					display1.append('-')
					display2.append(name2[j])
					display.append(' ')
					j += 1

			else:
				if alignment2[j]:
					display1.append(name1[i])
					display2.append('-')
					display.append(' ')
					i += 1

				else:
					display1.append(name1[i])
					display2.append(name2[j])
					display.append(' ')
					i += 1
					j += 1

		return '\n'.join([
			''.join(display1),
			''.join(display),
			''.join(display2)
		])

