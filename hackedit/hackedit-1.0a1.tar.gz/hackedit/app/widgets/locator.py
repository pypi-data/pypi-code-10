import re
from difflib import SequenceMatcher

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.api import DelayJobRunner, TextHelper, utils
from pyqode.core.share import Definition

from hackedit.api import editor, project, widgets
from hackedit.app.forms import locator_ui
from hackedit.app.widgets.html_delegate import HTMLDelegate


class LocatorWidget(QtWidgets.QFrame):
    """
    Popup widget that let the user quickly locate a file in a project.

    The user can also locate a symbol in the current editor with the ``@``
    operator or a symbol in the whole project with the ``#`` operator.

    The ``:`` operator can be used to specify the line number to go to.

    Note that all those operators are exclusive, you cannot mix
    ``@`` with ``:`` or with ``#``.
    """
    activated = QtCore.pyqtSignal(str, int)
    cancelled = QtCore.pyqtSignal()

    GOTO_LINE_PATTERN = re.compile(r'^.*:.*')
    GOTO_SYMBOL_PATTERN = re.compile('^@.*')
    GOTO_SYMBOL_IN_PROJ_PATTERN = re.compile('^!.*')

    MODE_GOTO_ANYTHING = 0
    MODE_GOTO_SYMBOL = 1
    MODE_GOTO_SYMBOL_IN_PROJECT = 2
    MODE_GOTO_LINE = 3

    def __init__(self, window=None):
        super().__init__()
        self.icon_provider = widgets.FileIconProvider()
        self._runner = DelayJobRunner(delay=100)
        self._window = window
        self.ui = locator_ui.Ui_Frame()
        self.ui.setupUi(self)
        self.ui.lineEdit.textChanged.connect(self.request_search)
        self.ui.lineEdit.prompt_text = 'Type to locate...'
        self.ui.lineEdit.installEventFilter(self)
        self.ui.treeWidget.installEventFilter(self)
        self.ui.treeWidget.setItemDelegate(HTMLDelegate())
        self.setWindowFlags(QtCore.Qt.Popup)
        self.ui.lineEdit.setFocus(True)
        self.ui.bt_close.clicked.connect(self.hide)
        self.ui.bt_infos.clicked.connect(self._show_help)
        self.mode = self.MODE_GOTO_ANYTHING
        self.ui.treeWidget.currentItemChanged.connect(
            self._on_current_item_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self._activate)

    def showEvent(self, ev):
        self._activated = False
        self.ui.lineEdit.clear()
        if self.mode == self.MODE_GOTO_ANYTHING:
            self.search_files()
        elif self.mode == self.MODE_GOTO_SYMBOL:
            self.ui.lineEdit.setText('@')
            self.search_symbol()
        elif self.mode == self.MODE_GOTO_SYMBOL_IN_PROJECT:
            self.ui.lineEdit.setText('!')
            self.search_symbol_in_project()
        elif self.mode == self.MODE_GOTO_LINE:
            self.ui.lineEdit.setText(':')
            self.ui.treeWidget.hide()
            self.adjustSize()
        self.ui.lineEdit.setFocus()
        super().showEvent(ev)

    def closeEvent(self, ev):
        if not self._activated:
            self.cancelled.emit()
        super().closeEvent(ev)

    def eventFilter(self, obj, ev):
        if obj == self.ui.lineEdit and ev.type() == QtCore.QEvent.KeyPress:
            if ev.key() == QtCore.Qt.Key_Down:
                next_item = self.ui.treeWidget.itemBelow(
                    self.ui.treeWidget.currentItem())
                if next_item is None:
                    next_item = self.ui.treeWidget.topLevelItem(0)
                self.ui.treeWidget.setCurrentItem(next_item)
                return True
            elif ev.key() == QtCore.Qt.Key_Up:
                next_item = self.ui.treeWidget.itemAbove(
                    self.ui.treeWidget.currentItem())
                if next_item is None:
                    next_item = self.ui.treeWidget.topLevelItem(
                        self.ui.treeWidget.topLevelItemCount() - 1)
                self.ui.treeWidget.setCurrentItem(next_item)
                return True
            elif ev.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                self._activate()
                return True
            if ev.key() in [QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab]:
                # tab should not have any effect
                return True
        elif obj == self.ui.treeWidget and ev.type() == QtCore.QEvent.KeyPress:
            if ev.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                self._activate()
                return True
        return super().eventFilter(obj, ev)

    def _activate(self, *_):
        if self.ui.treeWidget.isVisible():
            data = self.ui.treeWidget.currentItem().data(
                0, QtCore.Qt.UserRole)
        else:
            data = self._window.current_tab.file.path
        if isinstance(data, str):
            text = self.ui.lineEdit.text()
            if self.GOTO_LINE_PATTERN.match(text):
                line = self._get_requested_line_nbr()
            else:
                line = -1
            self.activated.emit(data, line)
        elif isinstance(data, tuple):
            path, line = data
            self.activated.emit(path, line)
        elif isinstance(data, Definition):
            self.activated.emit(
                data.file_path, data.line + 1)
        self._activated = True
        self.close()

    def request_search(self):
        self._runner.request_job(self._search)

    def _search(self):
        text = self.ui.lineEdit.text()
        # check the source to use for search (symbols or files).
        if self.GOTO_SYMBOL_PATTERN.match(text):
            if self.GOTO_LINE_PATTERN.match(text):
                self.ui.treeWidget.hide()
                self.adjustSize()
            else:
                self.search_symbol()
        elif self.GOTO_SYMBOL_IN_PROJ_PATTERN.match(text):
            if self.GOTO_LINE_PATTERN.match(text):
                self.ui.treeWidget.hide()
                self.adjustSize()
            else:
                self.search_symbol_in_project()
        else:
            if not text.startswith(':'):
                self.search_files()
            else:
                # will be used to goto line in the current editor.
                self.ui.treeWidget.hide()
                self.adjustSize()
                e = editor.get_current_editor()
                try:
                    TextHelper(e).goto_line(self._get_requested_line_nbr() - 1)
                except ValueError:
                    pass

    @staticmethod
    def flatten(results, level=1):
        """
        Flattens the document structure tree as a simple sequential list.
        """
        ret_val = []
        for de in results:
            ret_val.append(de)
            for sub_d in de.children:
                nd = Definition(
                    sub_d.name, sub_d.line, sub_d.column, sub_d.icon,
                    file_path=sub_d.file_path)
                ret_val += LocatorWidget.flatten(sub_d.children, level+1)
                ret_val.append(nd)
        return ret_val

    def search_symbol(self):
        search_term = self._get_search_term()
        try:
            outline_mode = editor.get_current_editor().modes.get('OutlineMode')
        except (KeyError, AttributeError):
            self.ui.treeWidget.clear()
        else:
            definitions = self.flatten(outline_mode.definitions)
            results = get_search_scores(
                search_term,
                [(d, d.name.split('(')[0].strip()) for d in definitions],
                True, '<b>{}</b>', True, True)

            # display
            self.ui.treeWidget.clear()
            first_item = None
            for original, d, enriched, _ in results:
                text = '%s<br><i>%s:%d</i>' % (enriched, d.file_path, d.line)
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, text)
                item.setIcon(0, self.icon_provider.icon(d.file_path))
                item.setData(0, QtCore.Qt.UserRole, d)
                if first_item is None:
                    first_item = item
                self.ui.treeWidget.addTopLevelItem(item)
            if self.ui.treeWidget.topLevelItemCount():
                self.ui.treeWidget.show()
                self.ui.treeWidget.setCurrentItem(first_item)
            else:
                self.ui.treeWidget.hide()
            self.adjustSize()

    def search_symbol_in_project(self):
        search_term = self._get_search_term()
        symbols = project.get_project_symbols(project.get_root_project())
        definitions = self.flatten(symbols)
        results = get_search_scores(
            search_term,
            [(d, d.name.split('(')[0].strip()) for d in definitions],
            True, '<b>{}</b>', True, True)

        # display
        self.ui.treeWidget.clear()
        first_item = None
        for original, d, enriched, _ in results:
            text = '%s<br><i>%s:%d</i>' % (enriched, d.file_path, d.line)
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, text)
            item.setIcon(0, self.icon_provider.icon(d.file_path))
            item.setData(0, QtCore.Qt.UserRole, d)
            if first_item is None:
                first_item = item
            self.ui.treeWidget.addTopLevelItem(item)
        if self.ui.treeWidget.topLevelItemCount():
            self.ui.treeWidget.show()
            self.ui.treeWidget.setCurrentItem(first_item)
        else:
            self.ui.treeWidget.hide()
        self.adjustSize()

    def get_definition_icon(self, icon):
        if isinstance(icon, list):
            icon = tuple(icon)
        return self._get_definition_icon(icon)

    @utils.memoized
    def _get_definition_icon(self, icon):
        if isinstance(icon, tuple):
            icon = QtGui.QIcon.fromTheme(
                icon[0], QtGui.QIcon(icon[1]))
        elif isinstance(icon, str):
            if QtGui.QIcon.hasThemeIcon(icon):
                icon = QtGui.QIcon.fromTheme(icon)
            else:
                icon = QtGui.QIcon(icon)
        return icon

    def search_files(self):
        project_files = project.get_project_files()
        search_term = self._get_search_term()
        results = get_search_scores(
            search_term,
            [(p, QtCore.QFileInfo(p).fileName()) for p in project_files],
            True, '<b>{}</b>', True, bool(search_term))

        # display
        self.ui.treeWidget.clear()
        first_item = None
        for original, path, enriched, _ in results:
            text = '%s<br><i>%s</i>' % (enriched, path)
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, text)
            item.setIcon(0, self.icon_provider.icon(path))
            item.setData(0, QtCore.Qt.UserRole, path)
            if first_item is None:
                first_item = item
            self.ui.treeWidget.addTopLevelItem(item)
        if self.ui.treeWidget.topLevelItemCount():
            self.ui.treeWidget.show()
            self.ui.treeWidget.setCurrentItem(first_item)
        else:
            self.ui.treeWidget.hide()
        self.adjustSize()

    def _get_search_term(self):
        text = self.ui.lineEdit.text()
        if text.startswith('@'):
            text = text[1:]
        elif text.startswith('!'):
            text = text[1:]
        if self.GOTO_LINE_PATTERN.match(text):
            text = text.split(':')[0]
        return text.strip()

    def _get_requested_line_nbr(self):
        text = self.ui.lineEdit.text()
        try:
            return int(text.split(':')[1])
        except (IndexError, ValueError):
            return -1

    def _show_help(self):
        help_text = '''<p>Use <i>Goto</i> to navigate your project’s files
swiftly.</p>

<p>Use the <i>arrow keys</i> to navigate into the list and press <i>ENTER</i>
to open the selected entry. Press <i>ESCAPE</i> to close the popup window.<p>

<p><i>Goto</i> accepts several operators:

<ul>
    <li> <b>@</b> to locate a symbol in the current editor.</li>
    <li> <b>!</b> to locate a symbol in the opened project(s).</li>
    <li> <b>:</b> to specify the line number to go to.</li>
</ul>

</p>
'''
        QtWidgets.QMessageBox.information(
            self, 'Goto: help', help_text)
        self.show()

    def _on_current_item_changed(self, item):
        text = self.ui.lineEdit.text()
        if item and self.GOTO_SYMBOL_PATTERN.match(text):
            data = item.data(0, QtCore.Qt.UserRole)
            TextHelper(editor.get_current_editor()).goto_line(data.line)


# The following 3 functions have been taken from SpyderIDE.
NOT_FOUND_SCORE = -1
NO_SCORE = 0


@utils.memoized
def get_search_regex(query, ignore_case=True):
    """Returns a compiled regex pattern to search for query letters in order.
    Parameters
    ----------
    query : str
        String to search in another string (in order of character occurence).
    ignore_case : True
        Optional value perform a case insensitive search (True by default).
    Returns
    -------
    pattern : SRE_Pattern
    Notes
    -----
    This function adds '.*' between the query characters and compiles the
    resulting regular expression.
    """
    query = _clean_query(query)
    regex_text = [char for char in query if char != ' ']
    regex_text = [(char + '.*') if char != '\\' else char for char in query]
    regex_text = ''.join(regex_text)
    regex = '({0})'.format(regex_text)

    if ignore_case:
        pattern = re.compile(regex, re.IGNORECASE)
    else:
        pattern = re.compile(regex)

    return pattern


def get_search_score(query, choice, ignore_case, apply_regex, template):
    """Returns a tuple with the enriched text (if a template is provided) and
    a score for the match.
    Parameters
    ----------
    query : str
        String with letters to search in choice (in order of appearance).
    choice : str
        Sentence/words in which to search for the 'query' letters.
    ignore_case : bool, optional
        Optional value perform a case insensitive search (True by default).
    apply_regex : bool, optional
        Optional value (True by default) to perform a regex search. Useful
        when this function is called directly.
    template : str, optional
        Optional template string to surround letters found in choices. This is
        useful when using a rich text editor ('{}' by default).
        Examples: '<b>{}</b>', '<code>{}</code>', '<i>{}</i>'
    Returns
    -------
    results : tuple
        Tuples where the first item is the text (enriched if a template was
        used) and the second item is a search score.
    Notes
    -----
    The score is given according the following precedence (high to low):
    - Letters in one word and no spaces with exact match.
      Example: 'up' in 'up stroke'
    - Letters in one word and no spaces with partial match.
      Example: 'up' in 'upstream stroke'
    - Letters in one word but with skip letters.
      Example: 'cls' in 'close up'
    - Letters in two or more words
      Example: 'cls' in 'car lost'
    """
    original_choice = choice
    result = (original_choice, original_choice, NOT_FOUND_SCORE)

    # Handle empty string case
    if not query:
        return result

    if ignore_case:
        query = query.lower()
        choice = choice.lower()

    if apply_regex:
        pattern = get_search_regex(query, ignore_case=ignore_case)
        r = re.search(pattern, choice)
        if r is None:
            return result
    else:
        sep = u'-'  # Matches will be replaced by this character
        let = u'x'  # Nonmatches (except spaed) will be replaced by this
        score = 0

        exact_words = [query == word for word in choice.split(u' ')]
        partial_words = [query in word for word in choice.split(u' ')]

        if any(exact_words) or any(partial_words):
            pos_start = choice.find(query)
            pos_end = pos_start + len(query)
            score += pos_start
            text = choice.replace(query, sep*len(query), 1)

            enriched_text = original_choice[:pos_start] +\
                template.format(original_choice[pos_start:pos_end]) +\
                original_choice[pos_end:]

        if any(exact_words):
            # Check if the query words exists in a word with exact match
            score += 1
        elif any(partial_words):
            # Check if the query words exists in a word with partial match
            score += 100
        else:
            # Check letter by letter
            text = [l for l in original_choice]
            if ignore_case:
                temp_text = [l.lower() for l in original_choice]
            else:
                temp_text = text[:]

            # Give points to start of string
            try:
                score += temp_text.index(query[0])
            except ValueError:
                score -= 1

            # Find the query letters and replace them by `sep`, also apply
            # template as needed for enricching the letters in the text
            enriched_text = text[:]
            for char in query:
                if char != u'' and char in temp_text:
                    index = temp_text.index(char)
                    enriched_text[index] = template.format(text[index])
                    text[index] = sep
                    temp_text = [u' ']*(index + 1) + temp_text[index+1:]

        enriched_text = u''.join(enriched_text)

        patterns_text = []
        for i, char in enumerate(text):
            if char != u' ' and char != sep:
                new_char = let
            else:
                new_char = char
            patterns_text.append(new_char)
        patterns_text = u''.join(patterns_text)
        for i in reversed(range(1, len(query) + 1)):
            score += (len(query) - patterns_text.count(sep*i))*100000

        temp = patterns_text.split(sep)
        while u'' in temp:
            temp.remove(u'')
        if not patterns_text.startswith(sep):
            temp = temp[1:]
        if not patterns_text.endswith(sep):
            temp = temp[:-1]

        for pat in temp:
            score += pat.count(u' ')*10000
            score += pat.count(let)*100

    return original_choice, enriched_text, score


@utils.memoized
def _clean_query(query):
    """
    Cleans the query before it is transformed to an SRE_Pattern.

    Cleaning means removing the white spaces and removing any regex operator
    (*, ?, +, .).
    """
    query = query.replace(' ', '')
    return re.escape(query)


def get_search_scores(query, choices, ignore_case, template, valid_only, sort):
    """Search for query inside choices and return a list of tuples.
    Returns a list of tuples of text with the enriched text (if a template is
    provided) and a score for the match. Lower scores imply a better match.
    Parameters
    ----------
    query : str
        String with letters to search in each choice (in order of appearance).
    choices : list of tuple (user_data, name)
        List of sentences/words in which to search for the 'query' letters.
        User data is any data you would like to associate with the name to
        check (e.g. definition object for a symbol,...)
    ignore_case : bool, optional
        Optional value perform a case insensitive search (True by default).
    template : str, optional
        Optional template string to surround letters found in choices. This is
        useful when using a rich text editor ('{}' by default).
        Examples: '<b>{}</b>', '<code>{}</code>', '<i>{}</i>'
    Returns
    -------
    results : list of tuples
        List of tuples:
            - original_text
            - enriched_text (= original text if not match were found)
            - user_data
            - score

        Lower scores means better match.

    Note
    ----

    We (the hackedit team) changed the implementation a bit to be more fault
    tolerant (user might make some typos and the results should ignore those
    typos).
    """
    # First remove spaces from query

    # Make sure user did not insert a repeating symbol

    results = []

    for user_data, choice in choices:
        to_remove = 0
        if query:
            for i in reversed(range(len(query))):
                my_query = query[:i + 1]
                r = re.search(get_search_regex(my_query, ignore_case), choice)
                if my_query and r:
                    original_choice, enriched_text, score = get_search_score(
                        query, choice, ignore_case, False, template)
                    result = original_choice, user_data, enriched_text, \
                        score - to_remove
                    break
                else:
                    if my_query and not r:
                        result = (choice, user_data, choice, NOT_FOUND_SCORE)
                    else:
                        result = (choice, user_data, choice, NO_SCORE)
                to_remove -= 10  # not exact match (typos)
        else:
            result = (choice, user_data, choice, NO_SCORE)

        if valid_only:
            if result[-1] != NOT_FOUND_SCORE:
                results.append(result)
        else:
            results.append(result)

    if sort:
        results = sorted(results, key=lambda row: row[-1])

    return results
