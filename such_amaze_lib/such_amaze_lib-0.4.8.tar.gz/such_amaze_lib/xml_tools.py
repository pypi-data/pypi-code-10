# coding=utf-8
"""
    Various XML parser en file generator
"""
import copy
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


def gen_xml_file(dst_file, in_dict, space_replace='_'):
    r"""
        Create an xml file according to the dictionary given
        It replace dict key string spaces with space_replace parameter

    :param dst_file: the xml_file name
    :param in_dict: input dictionary
    :param space_replace: the space replacement string

        :Example:

        >>> items = {'port': 'COM10',
        ...          'conf files':
        ...              {'paths': 'conf_path.xml',
        ...              'exe': 'win.exe'},
        ...          'timeout': 10,
        ...          'merchant': [{'merchant id': 123, 'url': 'www.hello.com'},
        ...                       {'id': 321, 'url': 'www.world.com', 'token': 0}]}
        ... 
        >>> gen_xml_file('test.xml', items)
        >>> with open('test.xml') as f:
        ...     for line in f:
        ...         line
        ... 
        '<?xml version="1.0" ?>\n'
        '<data>\n'
        ...
        '</data>\n'

    :return: the file abs path
        """
    in_dict = copy.deepcopy(in_dict)
    try:
        root = ElementTree.Element('data')
    except Exception as e:
        raise XMLToolsError('{}: Bad argument format: {}'.format(e, in_dict))

    def tree_build(values, parent):
        for key, value in values.items():
            key = key.replace(' ', space_replace)
            if isinstance(value, dict):
                tree_build(value, ElementTree.SubElement(parent, key))
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                for item in value:
                    for item_key, item_value in item.items():
                        if ' ' in item_key:
                            old_key = item_key
                            item_key = item_key.replace(' ', space_replace)
                            item.__delitem__(old_key)
                        item[item_key] = str(item_value)
                    ElementTree.SubElement(parent, key, **item)
            else:
                try:
                    ElementTree.SubElement(parent, key).text = str(value).decode("ascii")
                except UnicodeDecodeError:
                    ElementTree.SubElement(parent, key).text = repr(value)

    tree_build(in_dict, root)

    tree = ElementTree.ElementTree(root)
    tree.write(dst_file)
    prettify_xml(dst_file, dst_file)
