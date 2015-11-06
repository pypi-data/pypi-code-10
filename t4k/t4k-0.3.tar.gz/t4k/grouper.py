import math

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



