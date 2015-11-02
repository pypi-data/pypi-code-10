"""
Copyright (c) 2014, Jan Brohl <janbrohl@t-online.de>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from simpletal.simpleTALES import Context
from simpletal.simpleTALUtils import TemplateCache
import sys
if sys.version_info<(3,): #python3 or python2?
    from StringIO import StringIO
    from collections import Mapping
else:
    from io import StringIO
    from collections.abc import Mapping
from os.path import join, isfile, abspath, exists, isdir
from os import listdir


__version__ = "0.4.0"
_tc = TemplateCache()


class TemplatePath(Mapping):
    """
    Directory containing templates as a Mapping (like dict)
    """

    def __init__(self, path):
        self._path = abspath(path)

    def __getitem__(self, name):
        ap = abspath(join(self._path, name))
        if not (self._nameOK(name) and ap.startswith(self._path)):
            raise KeyError(name)
        fn = self._getFN(ap)
        if fn is None:
            if exists(ap):
                return TemplatePath(ap)
            raise KeyError(name)
        return self._getTPL(fn)

    def __len__(self):
        out = 0
        for fn in listdir(self.__path):
            fp = join(self._path, fn)
            if self._nameOK(fn) and (self._getFN(fp) or isdir(fp)):
                out += 1
        return out

    def _getFN(self, fp):
        for e in self._extensions:
            if isfile(fp + e):
                return fp + e
        return None

    def _nameOK(self, name):
        return not (name.startswith("_") or name.startswith("."))

    def __iter__(self):
        for fn in listdir(self._path):
            fp = join(self._path, fn)
            if self._nameOK(fn) and (self._getFN(fp) or isdir(fp)):
                yield fn

class XMLTemplatePath(TemplatePath):
    _extensions = (".xml", ".xhtml", ".XML", ".XHTML")

    def _getTPL(self, fn):
        return _tc.getXMLTemplate(fn)


class HTMLTemplatePath(TemplatePath):
    _extensions = (".html", ".htm", ".xhtml", ".HTML", ".HTM", ".XHTML")
    _encoding = "utf-8-sig"

    def __init__(self, path, encoding="default"):
        TemplatePath.__init__(self, path)
        if encoding != "default":
            self._encoding = encoding

    def _getTPL(self, fn):
        return _tc.getTemplate(fn, self._encoding)


def makeXMLRoot(path):
    return XMLTemplatePath(path)

def makeHTMLRoot(path):
    return HTMLTemplatePath(path)


class TALView(object):
    """
    Can be used as a decorator like
    @TALView("templatename") #no extension
    def somefunc(n):
        return dict(a=n,b=n*n,c=n**n)
    """
    templateRoot = makeHTMLRoot("templates") #default setting - change by subclassing
    moreGlobals = {}

    def __init__(self, templateName, moreGlobals = {}):
        self.templateName = templateName
        self.moreGlobals = moreGlobals

    def __call__(self, func, moreGlobals = {}):
        """
        Wrap func so the template gets rendered with options returned by func when called
        """
        return (lambda *args, **kwargs:self.render(func(*args, **kwargs), moreGlobals))

    def render(self, options = {}, moreGlobals = {}):
        """
        Render template with given options (and globals)
        """
        tpl = self.templateRoot[self.templateName] #use most recent version of template
        ctx = Context(options)
        ctx.addGlobal("container", self.templateRoot)
        d=dict(self.__class__.moreGlobals)
        d.update(self.moreGlobals)
        d.update(moreGlobals)
        for k, v in d.items():
            ctx.addGlobal(k, v)
        f=StringIO()
        tpl.expand(ctx, f, outputEncoding = "utf-8")
        return f.getvalue()

