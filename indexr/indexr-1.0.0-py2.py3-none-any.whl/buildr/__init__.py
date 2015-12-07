import abc
import os
import shutil
import sys
from collections import deque

import pickle

from indexr.utils import tokenize


def build_index(files, index_path, **kwargs):
    """
    Build an index.

    Optional parameters:
        indexer:        Indexing algorithm. The indexr package already has predefined algorithms in the
                        indexr.buildr.indexing submodule (default: indexr.buildr.indexing.BSB).
        force_rebuild:  Whether or not to rebuild the index.

    :param files:       List of files to include in the index.
    :type  files:       list
    :param index_path:  The path where all index files will be stored.
    :type  index_path:  str
    :param kwargs:      Optional parameters.
    :return             The index.
    """

    # Fetch the indexing algorithm
    indexer = kwargs.get('indexer', None)
    force_rebuild = kwargs.get('force_rebuild', False)
    if indexer is None:
        indexer = SPIMI()
    indexer.initialize(files, index_path)
    if not indexer.index_exists() or force_rebuild:
        indexer.construct()

    return indexer


class Buildr(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        Initialize the Buildr.
        """
        self._index_path = ''
        self._files = []
        self._block_path = ''
        self._index_file = ''

    def initialize(self, files, index_path):
        """
        Initialize the indexer.

        :param files:       List of files to include in the index.
        :type  files:       list
        :param index_path:  The path where all index files will be stored.
        :type  index_path:  str
        """
        self._index_path = index_path
        self._files = files
        self._block_path = os.path.join(self._index_path, '_block')
        self._index_file = os.path.join(self._index_path, 'index')
        if not os.path.exists(self._index_path):
            os.mkdir(self._index_path)

    def index_exists(self):
        """
        Check whether the index file already exists.

        :return: Whether the index file already exists or not.
        :rtype:  bool
        """
        return os.path.exists(self._index_file)

    def get_index_path(self):
        """
        Get the path to the index file.

        :return: Path to the index file.
        :rtype:  str
        """
        return self._index_file

    def get_size(self):
        """
        Get the size of the index.

        :return:    The size of the index (in kB, False if the index was not constructed).
        :rtype:     int|bool
        """
        if not self.index_exists():
            return False
        return os.path.getsize(self.get_index_path()) / 1024

    @abc.abstractmethod
    def construct(self):
        """
        Construct the index and store it in the file expressed in the self._index_file variable.
        """
        return

    @abc.abstractmethod
    def find(self, token, **kwargs):
        """
        Find all files which contain a given token.

        Optional parameters:
            frequencies:     If true, then a dictionary will be returned where the keys are all the files which have
                             at least one occurrence of the token and the values are the frequencies
                             (number of occurrences).
                             If false, then only a list of files will be returned where the elements are the files which
                             have at least one occurrence of the token (default: False).

        :param token:   Token to search for.
        :type  token:   str
        :param kwargs:  Optional parameters.
        :return:        A list (or dictionary) of files which contain the token.
        :rtype:         list|dict
        """
        return


class BSB(Buildr):
    """
    Block sort-based indexing.
    """

    def __init__(self, **kwargs):
        """
        Block sort-based indexing.

        Optional parameters:
            block_size:     The size of the blocks (default: 1024 bytes).

        :param kwargs:      Optional parameters.
        """
        super(BSB, self).__init__()
        self._lines = []
        self._block_num = 0
        self.block_size = kwargs.get('block_size', 1024)
        self.show_progress = kwargs.get('show_progress', False)

    def construct(self):
        """
        Construct the index.
        """
        # Make a subdirectory to store the blocks
        if os.path.exists(self._block_path):
            shutil.rmtree(self._block_path)
        os.mkdir(self._block_path)
        self._lines = []
        self._block_num = 0
        file_num = 0
        for file in self._files:
            file_pointer = open(file)
            buffered_token = ''
            while True:
                block = file_pointer.read(self.block_size + 1)
                if not block:
                    break
                tokens = tokenize(block)

                # Only do something if there are found tokens
                if len(tokens) > 0:
                    # Detect whether the block ends with a token
                    ends_with_token = (tokens[-1][-1] == block[-1])

                    # Detect whether the block start with a token
                    starts_with_token = (tokens[0][0] == block[0])

                    # Check whether the whole block is a token
                    block_is_token = (tokens[0] == block)

                    if block_is_token:
                        # If the full block is a token, then just enlarge the buffer
                        buffered_token += tokens[0]
                    else:
                        # Otherwise, there are at least two tokens in the block
                        block_tokens = []
                        if starts_with_token:
                            block_tokens.append(buffered_token + tokens[0])
                            buffered_token = ''
                            tokens = tokens[1:]
                        else:
                            block_tokens.append(buffered_token)
                            buffered_token = ''
                        if ends_with_token:
                            buffered_token = tokens[-1]
                            tokens = tokens[:-1]
                        for token in tokens:
                            block_tokens.append(token)
                        # Save the block tokens and increase the block number
                        if len(block_tokens) > 0:
                            self._save_block(file_num, block_tokens)
            if len(buffered_token) > 0:
                # If there is some left over token, save it as a block token and increase the block number
                self._save_block(file_num, [buffered_token])

            # Do not forget to close the file
            file_pointer.close()

            # Increase the file identifier
            file_num += 1

            # Display the progres
            if self.show_progress:
                sys.stdout.write("\rIndex construction: " + '{0} / {1}'.format(file_num, len(self._files)))
                sys.stdout.flush()

        # Save the line buffer if there is any left
        self._save_line_buffer()

        # The index construction is done
        if self.show_progress:
            sys.stdout.write("\rIndex construction: done\n")
            sys.stdout.flush()

        # Merge the blocks
        self._merge_blocks()

        # Clean up the temporary block folder
        shutil.rmtree(self._block_path)

    def get_vocab(self, **kwargs):
        files = kwargs.get('files', [])
        files_tester = kwargs.get('files', None)
        if type('') == type(files):
            files = [files]
        tokens = []
        with open(self.get_index_path(), 'r') as file_handle:
            for line in file_handle.readlines():
                line = line.strip()
                indexed_token, docs = line.split(' ')
                if files_tester is None:
                    if indexed_token not in tokens:
                        tokens.append(indexed_token)
                else:
                    docs = docs.split(':')
                    for file in files:
                        if str(self.get_document_id(file)) in docs:
                            tokens.append(indexed_token)
        return tokens

    def get_document_id(self, document):
        index = 0
        for found_document in self._files:
            if document == found_document:
                return index
            index += 1
        return False

    def find(self, token, **kwargs):
        frequencies = kwargs.get('frequencies', False)
        if frequencies:
            result = {}
        else:
            result = []
        with open(self.get_index_path(), 'r') as file:
            for line in file.readlines():
                line = line.strip()
                indexed_token, docs = line.split(' ')
                if token == indexed_token:
                    docs = docs.split(':')
                    index = 0
                    for indexed_file in self._files:
                        if frequencies:
                            for item in docs:
                                if int(item) == index:
                                    if indexed_file not in result:
                                        result[indexed_file] = 0
                                    result[indexed_file] += 1
                        else:
                            for item in docs:
                                if int(item) == index:
                                    if indexed_file not in result:
                                        result.append(indexed_file)
                        index += 1
                    break
        return result

    def _save_block(self, file_num, tokens):
        """
        Save an inverted block.

        :param file_num:     The file index.
        :type  file_num:     int
        :param tokens:       List of tokens to save.
        :type  tokens:       list
        """
        for raw_token in tokens:
            raw_token = raw_token.strip()
            for token in tokenize(raw_token):
                if len(token) > 0:
                    line = token + ' ' + str(file_num) + "\n"
                    self._lines.append(line)
                    if len(line) > self.block_size:
                        self._save_line_buffer()

    def _save_line_buffer(self):
        """
        Save the current line buffer.
        """
        if len(self._lines) == 0:
            return
        file_path = os.path.join(self._block_path, str(self._block_num))
        with open(file_path, 'w') as file_handle:
            for line in self._lines:
                file_handle.write(line)
        self._lines = []
        self._block_num += 1

    @staticmethod
    def _line_merger(path, lines):
        """
        Merge lines into a file such that the file has its lines sorted.

        :param path:        Path to the file.
        :type  path:        str
        :param lines:       Lines to merge.
        :type  lines:       list
        """
        if len(lines) == 0:
            return
        sorted_lines = sorted(lines)
        if os.path.exists('_tmp'):
            os.remove('_tmp')
        if not os.path.exists(path):
            open(path, 'w').close()
        writer = open('_tmp', 'w')
        file = open(path, 'r')
        line_index = 0
        add_line = sorted_lines[line_index]
        done = False
        for line in file.readlines():
            line = line.strip()
            while add_line <= line and not done:
                writer.write(add_line + "\n")
                line_index += 1
                if line_index < len(sorted_lines):
                    add_line = sorted_lines[line_index]
                else:
                    done = True
            writer.write(line + "\n")
        while line_index < len(sorted_lines):
            add_line = sorted_lines[line_index]
            writer.write(add_line + "\n")
            line_index += 1
        file.close()
        writer.close()
        os.remove(path)
        os.rename('_tmp', path)

    def _merge_blocks(self):
        """
        Merge blocks.
        """
        self._tmp_index = os.path.join(self._index_path, '_tmp_index')
        # Loop through all block files
        block_num = 0
        for root_folder, folders, files in os.walk(self._block_path):
            for file in files:
                # Loop through all files
                file_path = os.path.join(root_folder, file)
                pairs = []
                # Find all pairs and place them into main memory
                with open(file_path, 'r') as file_handle:
                    for line in file_handle.readlines():
                        token, file_num = line.split()
                        pairs.append((token, file_num))
                # Sort the pairs
                sorted_pairs = sorted(pairs, key=lambda pair: pair[0])
                lines = []
                for token, doc_id in sorted_pairs:
                    lines.append(token + ' ' + doc_id)
                self._line_merger(self._tmp_index, lines)
                block_num += 1

                # Display the progres
                if self.show_progress:
                    sys.stdout.write("\rBlock merging: " + '{0} / {1}'.format(block_num, len(files)))
                    sys.stdout.flush()

        # Now merge lines
        writer = open(self.get_index_path(), 'w')
        handle = open(self._tmp_index, 'r')
        last_token = None
        is_first_token = True
        for line in handle.readlines():
            line = line.strip()
            token, doc_id = line.split(' ')
            if token != last_token:
                if not is_first_token:
                    writer.write("\n")
                writer.write(token + ' ' + str(doc_id))
            else:
                writer.write(':' + str(doc_id))
            last_token = token
            is_first_token = False
        handle.close()
        writer.close()
        # Remove the temporary index file
        os.remove(self._tmp_index)

        if self.show_progress:
            sys.stdout.write("\rBlock merging: done\n\n")
            sys.stdout.flush()


class SPIMI(Buildr):
    """
    Single-pass In Memory Indexing.
    """

    def __init__(self, **kwargs):
        """
        Single-pass In Memory Indexing.

        Optional parameters:
            show_progress:     Whether or not to show the progress.

        :param kwargs:      Optional parameters.
        """
        super(SPIMI, self).__init__()
        self.show_progress = kwargs.get('show_progress', False)

    def construct(self):
        dictionary = dict()
        postings = dict()
        last_docs = dict()
        files = dict()
        token_id = 0
        num_files = len(self._files)
        # Apply lossless compression by only saving the gaps between document ids (not the document ids themselves)
        for doc_id in range(0, num_files):
            # Loop through all documents
            file = self._files[doc_id]
            files[doc_id] = file
            with open(file, 'r') as handle:
                # Open the file and tokenize
                tokens = tokenize(handle.read())
                for token in tokens:
                    # Update the dictionary and postings
                    if token not in dictionary:
                        dictionary[token] = token_id
                        postings[token_id] = deque([doc_id])
                        last_docs[token_id] = doc_id
                        token_id += 1
                    else:
                        found_token_id = dictionary[token]
                        gap = doc_id - last_docs[found_token_id]
                        postings[found_token_id].append(gap)
                        last_docs[found_token_id] = doc_id
            if self.show_progress:
                sys.stdout.write("\rIndexing: " + '{0} / {1}'.format(doc_id, num_files))
                sys.stdout.flush()
        # The index construction is done
        if self.show_progress:
            sys.stdout.write("\rIndex construction: done\n")
            sys.stdout.flush()
        # Save the index
        index = (postings, dictionary, files)
        pickle.dump(index, open(self.get_index_path(), 'wb'))

    def find(self, token, **kwargs):
        frequencies = kwargs.get('frequencies', False)
        if frequencies:
            result = {}
        else:
            result = []
        (postings, dictionary, files) = pickle.load(open(self.get_index_path(), 'rb'))
        # Check whether the token is in the dictionary
        if token not in dictionary.keys():
            return []
        token_id = dictionary[token]
        token_postings = postings[token_id]
        doc_id = 0
        # Loop through all document gaps
        for doc_gap in token_postings:
            doc_id += doc_gap
            file = files[doc_id]
            if frequencies:
                # Case for frequencies
                if doc_gap == 0 and doc_id > 0:
                    result[file] += 1
                else:
                    result[file] = 1
            else:
                # Case for occurrences
                if doc_gap > 0:
                    result.append(file)
        return result
