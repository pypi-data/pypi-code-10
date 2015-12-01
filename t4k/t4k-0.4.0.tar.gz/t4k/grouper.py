import math

def flatten(iterable, recurse=False, depth=0):
	'''
	flattens an iterable of iterables into a simple list.  E.g.
	turns a list of list of elements into a simple list of elements.

	<recurse> will attempt to flatten the elements within the inner 
	iterable too, and will continue so long as the elements found are 
	iterable.  However, recurse will treat strings as atomic, even though
	they are iterable.
	'''

	flat_list = []
	for element in iterable:

		# If the element is not iterable, just add it to the flat list
		try:
			iter(element)
		except:
			flat_list.append(element)
			continue
		else:

			# If the element is a string, treat it as not iterable
			if isinstance(element, basestring):
				flat_list.append(element)

			# If the element is iterable and <recurse> is True, recurse
			elif recurse:
				flat_list.extend(flatten(element, recurse))

			# If the element is iterable but <recurse> is False, extend
			else:
				flat_list.extend(element)

	return flat_list



def group(iterable, num_chunks):
	'''
	Breaks <iterable> into <num_chunks> chunks (lists) of approximately 
	equal size (chunks will differ by at most one item when <num_chunks> 
	doesn't evenly divide len(<iterable>)).
	'''

	# Coerce the sequence into a list
	iterable = list(iterable)

	# Figure out the chunksize
	num_items = len(iterable)
	chunk_size = num_items / float(num_chunks)

	# Allocate approximately chunksize elements to each chunk, rounded off.
	chunks = []
	for i in range(num_chunks):
		start_index = int(math.ceil(i * chunk_size))
		end_index = int(math.ceil((i+1) * chunk_size))
		chunks.append(iterable[start_index:end_index])

	return chunks


def chunk(iterable, chunk_size):
	'''
	Returns a list of lists of items from iterable, where the internal 
	lists are each approximately of size chunk_size (except the last one,
	which is smaller if chunk_size doesn't evenly divide len(iterable)
	'''

	iterator = iter(iterable)
	chunks = []
	this_chunk = []
	still_has_items = True
	while still_has_items:
		try:
			this_chunk.append(iterator.next())
		except StopIteration:
			still_has_items = False

		if len(this_chunk) == chunk_size:
			chunks.append(this_chunk)
			this_chunk = []

		elif not still_has_items and len(this_chunk) > 0:
			chunks.append(this_chunk)

	return chunks



