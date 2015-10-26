"""PytSite Select Widgets.
"""
from datetime import datetime as _datetime
from pytsite import assetman as _assetman, browser as _browser, html as _html, lang as _lang, validation as _validation, \
    hreflang as _hreflang, router as _router
from . import _input, _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Checkbox(_input.Input):
    """Single Checkbox Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._label_disabled = True

    def set_value(self, value, **kwargs):
        """Set value of the widget.
        """
        self._value = bool(value)

    def render(self):
        """Render the widget.
        """
        div = _html.Div(cls='checkbox')
        div.append(_html.Input(type='hidden', name=self._name))
        label = _html.Label(self._label, label_for=self._uid)
        label.append(_html.Input(uid=self._uid, name=self._name, type='checkbox', checked=self._value))
        div.append(label)

        return self._group_wrap(div)


class Select(_input.Input):
    """Select Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._items = kwargs.get('items', [])
        if type(self._items) not in (list, tuple):
            raise TypeError('List or tuple expected.')

    def _get_select_html_em(self) -> _html.Element:
        select = _html.Select(name=self.name, cls='form-control', required=self._required)
        select.append(_html.Option('--- ' + _lang.t('pytsite.widget@select_none_item') + ' ---', value=''))
        for item in self._items:
            option = _html.Option(item[1], value=item[0])
            if item[0] == self._value:
                option.set_attr('selected', True)
            select.append(option)

        return select

    def render(self):
        """Render the widget.
        """
        return self._group_wrap(self._get_select_html_em())


class Select2(Select):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        _browser.include('select2')
        _assetman.add('pytsite.widget@js/select2.js')

        self._theme = kwargs.get('theme', 'bootstrap')
        self._ajax_url = kwargs.get('ajax_url')
        self._ajax_delay = kwargs.get('ajax_delay', 750)
        self._ajax_data_type = kwargs.get('ajax_data_type', 'json')
        self._css += ' widget-select-select2'

    def render(self):
        select = self._get_select_html_em()

        if self._ajax_url:
            select.set_attr('data_theme', self._theme)
            select.set_attr('data_ajax_url', self._ajax_url)
            select.set_attr('data_ajax_delay', self._ajax_delay)
            select.set_attr('data_ajax_data_type', self._ajax_data_type)

        return self._group_wrap(select)


class Checkboxes(Select):
    """Group of Checkboxes Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self.set_value(kwargs.get('value', []))

        if not isinstance(self._value, list):
            raise TypeError("List expected.")

        self._selected_items = kwargs.get('selected_items', self._value)

    def set_value(self, value: list, **kwargs):
        """Set value of the widget.
        """

        if not isinstance(value, list):
            raise TypeError('List expected')

        self._value = value
        self._selected_items = value

    def render(self) -> str:
        """Render the widget.
        """
        div = _html.Div()
        div.append(_html.Input(type='hidden', name=self.uid))
        for item in self._items:
            checked = True if item[0] in self._selected_items else False
            div.append(
                _html.Div(cls='checkbox').append(
                    _html.Label(item[1]).append(
                        _html.Input(type='checkbox', name=self.uid, value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(div)


class Language(Select):
    """Select Language Widget
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._items = kwargs.get('items', [])

        for code in _lang.langs():
            self._items.append((code, _lang.lang_title(code)))


class LanguageNav(_base.Base):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._bootstrap = kwargs.get('bootstrap', True)
        self._dropdown = kwargs.get('dropdown')
        self._css += ' lang-switch'

        if self._bootstrap:
            self._css += ' nav navbar-nav'

    def render(self):
        if len(_lang.langs()) == 1:
            return _html.TagLessElement()

        root_ul = _html.Ul(cls=self._css)
        cur_lang = _lang.get_current()

        if self._dropdown:
            dropdown_root = _html.Li(cls='dropdown')
            toggle_a = _html.A(_lang.lang_title(cur_lang), cls='dropdown-toggle lang-' + cur_lang,
                               data_toggle='dropdown', role='button',
                               aria_haspopup='true', aria_expanded='false', href='#', content_first=True)
            toggle_a.append(_html.Span(cls='caret'))

            dropdown_menu = _html.Ul(cls='dropdown-menu')
            for lng in _lang.langs(True):
                hl = _hreflang.get(lng)
                if hl:
                    dropdown_menu.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=hl))
                    )

            dropdown_root.append(toggle_a).append(dropdown_menu)
            root_ul.append(dropdown_root)
        else:
            for lng in _lang.langs():
                lang_title = _lang.lang_title(lng)
                if lng == cur_lang:
                    root_ul.append(_html.Li(cls='active').append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.current_url(),
                                title=lang_title)))
                elif _hreflang.get(lng):
                    root_ul.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_hreflang.get(lng),
                                title=lang_title)))
                else:
                    root_ul.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.base_url(lang=lng),
                                title=lang_title)))

        return root_ul


class DateTime(_input.Text):
    """Date/Time Select Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        _browser.include('datetimepicker')
        _assetman.add('pytsite.widget@js/datetime.js')

        self._css = self._css.replace('widget-input-text', 'widget-select-datetime')
        self.add_rule(_validation.rule.DateTime())

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if value and isinstance(value, str):
            value = _datetime.strptime(value, '%d.%m.%Y %H:%M')

        return super().set_value(value, **kwargs)

    def get_value(self, **kwargs: dict) -> _datetime:
        """Get value of the widget.
        """
        return super().get_value(**kwargs)

    def render(self) -> str:
        """Render the widget
        """
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self.get_value().strftime('%d.%m.%Y %H:%M'),
            cls=' '.join(('form-control', self._css)),
            required=self._required,
        )

        return self._group_wrap(html_input)
