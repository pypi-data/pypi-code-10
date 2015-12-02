"""
This module contains the functions to read BibTeX entries to a :class:`.bibdb.BibDB` object.

.. note:: By default LaTeX codes will be *decode* to a unicode character.

"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'
__revision__  = filter(str.isdigit, "$Revision: 92 $")


# import external package modules
import isbnlib

# import of internal package modules
from ._entry import Entry
from ._bibdb import BibDB
from .dev._parser import parse_data
from .dev._latexenc import latex_to_string
from .dev._doilib import (doi2bibtex, DOIError)


def db_from_string(bibStr, decode=True, method=None):
    """
    Function parsing a BibTeX bibStr containing one or more entries
    and returns a BibTeX database object.

    :param bibStr: input BibTeX string
    :type bibStr: str
    :param decode: LaTeX codes to unicode character
    :type decode: bool
    :param method: keyword for merging method (see :meth:`.BibDB.add_entry`)
    :type method: str
    :return: BibTeX database object
    :rtype: .BibDB
    """

    # decode LaTeX code to unicode characters
    if decode:
        bibStr = latex_to_string(bibStr)

    # parses a bibStr
    listOfDicts = parse_data(bibStr)

    return _db_from_listOfDicts(listOfDicts, method=method)


def db_from_file(filename, decode=True, method=None):
    """
    Function parsing a BibTeX file containing one or more entries
    and returns a BibTeX database object.

    :param filename: input BibTeX file
    :type filename: str
    :param decode: LaTeX codes to unicode character
    :type decode: bool
    :param method: keyword for merging method (see :meth:`.BibDB.add_entry`)
    :type method: str
    :return: BibTeX database object
    :rtype: .BibDB
    """
    # read the file to a string
    dataStr = open(filename, 'r').read().decode('utf8')

    return db_from_string(dataStr, decode=decode, method=method)


def db_from_doi(doiList, decode=True, method=None):
    """
    Function to retrieve BibTeX citation entries by their DOI
    and returns a BibTeX database object.

    :param doiList: list of DOIs as strings
    :type doiList: list
    :param decode: LaTeX codes to unicode character
    :type decode: bool
    :param method: keyword for merging method (see :meth:`.BibDB.add_entry`)
    :type method: str
    :return: BibTeX database object
    :rtype: .BibDB
    """
    dataStr = u''
    for DOI in doiList:
        dataStr += doi2bibtex(DOI) + "\n"

    return db_from_string(dataStr, decode=decode, method=method)


def db_from_isbn(isbnList, method=None):
    """
    Function to retrieve BibTeX citation entries by their ISBN
    and returns a BibTeX database object.

    :param isbnList: list of ISBN numbers as strings
    :type isbnList: list
    :param method: keyword for merging method (see :meth:`.BibDB.add_entry`)
    :type method: str
    :return: BibTeX database object
    :rtype: .BibDB
    """
    listOfDicts = []
    for isbn in isbnList:
        metaDict = _metaData_from_ISBN(isbn)
        if metaDict:
            inputdict = _meta_to_inputdict(metaDict)
            listOfDicts.append(inputdict)

    return _db_from_listOfDicts(listOfDicts, method=method)


def _db_from_listOfDicts(listOfDicts, method=None):
    """
    Creates a database from a list of inputdicts.

    :param listOfDicts: list of inputdicts
    :param method: keyword for merging method (see :meth:`.BibDB.add_entry`)
    :type method: str
    :return:  BibTeX database object
    :rtype: .BibDB
    """
    listOfEntryObj=[]
    for entryDict in listOfDicts:
        entryObj = Entry.get_Instance(entryDict)
        listOfEntryObj.append(entryObj)

    return BibDB(listOfEntryObj, method=method)


def _meta_to_inputdict(metaDict):
    """
    Converts a dictionary as returned by the isbnlib.meta() function to
    a valid inputdict for an entry object.

    :param metaDict: meta data
    :type metaDict: dict
    :return: inputdict
    :rtype: dict
    """
    for key, vakue in metaDict.items():
        new_key = key.lower()
        # key name correction
        if new_key == 'authors':
            new_key = 'author'
        metaDict[new_key] = metaDict.pop(key)
    # set citation-key
    metaDict['ID'] = str(metaDict.get('isbn-13','unknown'))
    # set type to 'Book'
    metaDict['ENTRYTYPE'] = 'book'
    # join author list
    metaDict['author'] = ' and '.join( metaDict['author'] )
    return metaDict


def _metaData_from_ISBN(isbn):
    """
    Returns the meta data for a given ISBN number.
    If the ISBN number is invalid or no meta data is available, it returns *None*.

    :param isbn: ISBN number
    :type isbn: str
    :return: meta data
    :rtype: dict
    """
    try:
        metaDict = isbnlib.meta(isbn=isbn)
    except isbnlib._exceptions.NotValidISBNError as e:
        print e.message
        metaDict = None
    return metaDict