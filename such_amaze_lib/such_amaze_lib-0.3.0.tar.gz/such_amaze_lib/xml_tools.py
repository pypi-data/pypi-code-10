"""
    Various XML parser en file generator
"""
from xml.etree import ElementTree
from xml.dom import minidom


class XMLToolsError(Exception):
    pass


def prettify_xml(src_filename, dst_filename):
    """
        Prettify an xml file

    :param src_filename: the source file name
    :param dst_filename: the destination file name
    """
    xml = minidom.parse(src_filename)
    pretty_xml_as_string = xml.toprettyxml()
    f = open(dst_filename, 'w')
    f.write(pretty_xml_as_string)
    f.close()


def get_xml_item(label, xml_file):
    """
        Find text text corresponding to the item label

    :param label: the item label to look for
    :param xml_file: the file to browse
    :return: str
    """
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    for i in root.findall(label):
        return i.text


def gen_xml_file(dest_file, items):
    r"""
        Create an xml file according to the dictionary given

    :param dest_file: the xml_file name
        :Example:

        >>> items = {'root': 'data',
        ... 'data':
        ...     {'port': 'COM10',
        ...     'conf_files':
        ...         {'paths': 'conf_path.xml',
        ...         'exe': 'win.exe'},
        ...     'timeout': 10}}
        >>> gen_xml_file('test.xml', items)
        >>> with open('test.xml') as f:
        ...     for line in f:
        ...         line
        ...
        '<?xml version="1.0" ?>\n'
        '<data>\n'
        '\t<conf_files>\n'
        '\t\t<paths>conf_path.xml</paths>\n'
        '\t\t<exe>win.exe</exe>\n'
        '\t</conf_files>\n'
        '\t<port>COM10</port>\n'
        '\t<timeout>10</timeout>\n'
        '</data>\n'

    :return: the file abs path
    """
    try:
        root = ElementTree.Element(items['root'])
        data = items['data']
    except Exception as e:
        raise XMLToolsError('{}: Bad argument format: {}'.format(e, items))

    def tree_build(values, parent):
        for key, value in values.items():
            if isinstance(value, dict):
                tree_build(value, ElementTree.SubElement(parent, key))
            else:
                ElementTree.SubElement(parent, key).text = str(value)

    tree_build(data, root)

    tree = ElementTree.ElementTree(root)
    tree.write(dest_file)
    prettify_xml(dest_file, dest_file)
