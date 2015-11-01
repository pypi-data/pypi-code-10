import abc
import os
import re
import shutil
import tempfile
import zipfile

from typing import List, Optional

import lxml.etree


def _etree_to_xml(etree: lxml.etree._ElementTree) -> bytes:
    return lxml.etree.tostring(etree, xml_declaration=True, encoding='UTF-8')


class IOBase(metaclass=abc.ABCMeta):
    def __init__(self, file_path: str, *args, **kwargs) -> None:
        self.original_path = file_path

    @abc.abstractmethod
    def extract(self) -> List[str]:
        """Return list of paragraph.
        """
        ...

    @abc.abstractmethod
    def swap(self, texts: List[str]) -> None:
        ...

    @abc.abstractmethod
    def save(self, dest_file_path: str=None) -> None:
        """
        :param dest_file_path: When this parameter is None, overwrite the original file.
        """
        ...

    def _make_parent_directory(self, file_path: str) -> None:
        """Make directories for the file_path.
        """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)


class TextIO(IOBase):
    def __init__(self, file_path: str, *args, **kwargs) -> None:
        super().__init__(file_path)
        with open(file_path) as f:
            self.text = f.read()

    def extract(self) -> List[str]:
        return [self.text]

    def swap(self, texts: List[str]) -> None:
        self.text = texts[0]

    def save(self, dest_file_path: str=None) -> None:
        actual_dest_file_path = self.original_path if dest_file_path is None else dest_file_path
        self._make_parent_directory(actual_dest_file_path)
        with open(actual_dest_file_path, 'w') as f:
            f.write(self.text)


class OfficeOpenXMLSpreadsheetIO(IOBase):
    """As know as Excel.
    """
    namespaces = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    shared_strings_path = 'xl/sharedStrings.xml'

    def __init__(self, file_path: str, *args, **kwargs) -> None:
        super().__init__(file_path)
        # Read strings file from the orifinal file. OfficeOpenXML file is compressed as zip.
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            with zip_file.open(self.shared_strings_path) as zip_element:
                shared_strings = zip_element.read()  # type: bytes
        self.etree = lxml.etree.fromstring(shared_strings)

    def extract(self) -> List[str]:
        return self.etree.xpath('//ns:t/text()', namespaces=self.namespaces)

    def swap(self, texts: List[str]) -> None:
        for t, new_text in zip(self.etree.xpath('//ns:t', namespaces=self.namespaces), texts):
            if new_text is not None:
                t.text = new_text

    def save(self, dest_file_path: str=None) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp_file_path = f.name

        # Copy zip items because cannot over write zip item.
        with zipfile.ZipFile(self.original_path, 'r') as old_zip:
            with zipfile.ZipFile(tmp_file_path, 'w') as new_zip:
                for info in old_zip.infolist():
                    if info.filename == self.shared_strings_path:
                        continue
                    new_zip.writestr(info, old_zip.read(info.filename))

                new_zip.writestr(self.shared_strings_path, _etree_to_xml(self.etree))

        if dest_file_path is None:
            actual_dest_file_path = self.original_path
        else:
            self._make_parent_directory(dest_file_path)
            shutil.copyfile(self.original_path, dest_file_path)
            actual_dest_file_path = dest_file_path
        os.rename(tmp_file_path, actual_dest_file_path)


class OfficeOpenXMLPresentationIO(IOBase):
    """As know as Power Point.
    """
    namespaces = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    def __init__(self, file_path: str, *args, **kwargs) -> None:
        super().__init__(file_path)
        # Read strings file from the orifinal file. OfficeOpenXML file is compressed as zip.
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            # sorted by slide number
            self.slides = [
                name for number, name in sorted(
                    [
                        # Because slide10 is behind slide2.
                        (int(re.search('\d+', name).group()), name)
                        for name in zip_file.namelist() if name.startswith('ppt/slides/slide')
                    ]
                )
            ]
            self.etrees = []
            for slide in self.slides:
                with zip_file.open(slide) as zip_element:
                    xml = zip_element.read()  # type: bytes
                self.etrees.append(lxml.etree.fromstring(xml))

    def extract(self) -> List[str]:
        texts = []
        for etree in self.etrees:
            texts.extend([
                t.text for t in etree.xpath(
                    '//a:t', namespaces=self.namespaces) if t.text.strip() != ''
            ])
        return texts

    def swap(self, texts: List[str]) -> None:
        def swap(etree, texts: List[str]) -> List[str]:
            for t in etree.xpath('//a:t', namespaces=self.namespaces):
                if t.text.strip() == '':
                    continue
                text = texts.pop()
                if text is None:
                    continue
                t.text = text
            return texts

        # pop is the fastest when access last element of list.
        reversed_texts = list(reversed(texts))
        for etree in self.etrees:
            reversed_texts = swap(etree, reversed_texts)

    def save(self, dest_file_path: str=None) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp_file_path = f.name

        # Copy zip items because cannot over write zip item.
        with zipfile.ZipFile(self.original_path, 'r') as old_zip:
            with zipfile.ZipFile(tmp_file_path, 'w') as new_zip:
                for info in old_zip.infolist():
                    if info.filename in (self.slides):
                        continue
                    new_zip.writestr(info, old_zip.read(info.filename))

                for name, etree in zip(self.slides, self.etrees):
                    new_zip.writestr(name, _etree_to_xml(etree))

        if dest_file_path is None:
            actual_dest_file_path = self.original_path
        else:
            self._make_parent_directory(dest_file_path)
            shutil.copyfile(self.original_path, dest_file_path)
            actual_dest_file_path = dest_file_path
        os.rename(tmp_file_path, actual_dest_file_path)


class XMLIO(IOBase):
    def __init__(self, file_path: str, *args, **kwargs) -> None:
        super().__init__(file_path)
        with open(file_path) as f:
            self.etree = lxml.etree.parse(f)

    def extract(self) -> List[str]:
        def append_if_not_only_whitespace(text: Optional[str], texts: List[str]) -> List[str]:
            if text is not None and text.strip() != '':
                texts.append(text)
            return texts

        def extract(element: lxml.etree._Element, texts: List[str]) -> List[str]:
            texts = append_if_not_only_whitespace(element.text, texts)
            for child_element in element.iterchildren():
                texts = extract(child_element, texts)
            return append_if_not_only_whitespace(element.tail, texts)
        return extract(self.etree.getroot(), [])

    def swap(self, texts: List[str]) -> None:
        def swap_if_valid(
                element: lxml.etree._Element, property: str, texts: List[str]) -> List[str]:
            text = getattr(element, property)
            if text is not None and text.strip() != '':
                new_text = texts.pop()
                if new_text is not None:
                    setattr(element, property, new_text)
            return texts

        def swap(element: lxml.etree._Element, texts: List[str]) -> List[str]:
            texts = swap_if_valid(element, 'text', texts)
            for child_element in element.iterchildren():
                texts = swap(child_element, texts)
            return swap_if_valid(element, 'tail', texts)

        swap(self.etree.getroot(), list(reversed(texts)))

    def save(self, dest_file_path: str=None) -> None:
        if dest_file_path is None:
            actual_dest_file_path = self.original_path
        else:
            self._make_parent_directory(dest_file_path)
            actual_dest_file_path = dest_file_path

        dest_xml = _etree_to_xml(self.etree)
        with open(actual_dest_file_path, 'wb') as f:
            f.write(dest_xml)
