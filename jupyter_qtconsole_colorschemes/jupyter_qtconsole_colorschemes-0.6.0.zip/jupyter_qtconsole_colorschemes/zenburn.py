"""
A Pygments_ style based on the dark background variant of Zenburn_. Originally
from https://github.com/litzomatic/MyVim

.. _Pygments: http://pygments.org/
.. _Zenburn: http://kippura.org/zenburnpage/
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

class ZenburnStyle(Style):
    """
    This style mimics the Zenburn color scheme.
    """

    #background_color = "#1f1f1f" #high contrast
    #background_color = "#3f3f3f"
    background_color = "#393939"
    highlight_color = "#838383"
    #highlight_color = "#2f2f2f"
    #highlight_color = "#dcdccc"

    styles = {
        # No corresponding class for the following:
        Text: "#dcdccc", # class:  ''
        Whitespace: "#000000",
        #Error: "#80d4aa bg:#2f2f2f",
        Error: "#e37170 bg:#3d3535",
        Other: "#000000",
        
        Comment: "italic #7f9f7f",
        #Comment.Multiline
        #Comment.Preproc
        #Comment.Single
        #Comment.Special

        Keyword: "bold #f0dfaf",
        Keyword.Constant: "#dca3a3",
        Keyword.Declaration: "#000000",
        Keyword.Namespace: "bold #dfaf8f",
        #Keyword.Pseudo
        #Keyword.Reserved
        #Keyword.Type

        Operator: "#f0efd0",
        #Operator.Word

        Punctuation: "#8f8f8f",

        Name: "#dcdccc",
        Name.Attribute: "#000000",
        Name.Builtin: "#efef8f",
        Name.Builtin.Pseudo: "#efef8f",
        Name.Class: "#efef8f",
        Name.Constant: "#000000",
        Name.Decorator: "#000000",
        Name.Entity: "#000000",
        Name.Exception: "bold #c3bf9f",
        Name.Function: "#efef8f",
        Name.Property: "#000000",
        Name.Label: "#000000",
        Name.Namespace: "#8fbede",
        #Name.Other
        #Name.Tag
        #Name.Variable
        Name.Variable.Class: "#efef8f",
        #Name.Variable.Global
        #Name.Variable.Instance

        Number: "#8cd0d3",
        #Number.Float
        #Number.Hex
        #Number.Integer
        #Number.Integer.Long
        #Number.Oct

        Literal: "#000000",
        Literal.Date: "#000000",

        String: "#cc9393",
        #String.Backtick
        #String.Char
        #String.Doc
        #String.Double
        #String.Escape
        #String.Heredoc
        #String.Interpol
        #String.Other
        #String.Regex
        #String.Single
        #String.Symbol

        Generic: "#dcdccc",
        #Generic.Deleted
        #Generic.Emph
        #Generic.Error
        #Generic.Heading
        #Generic.Inserted
        #Generic.Output
        #Generic.Prompt
        #Generic.Strong
        #Generic.Subheading
        #Generic.Traceback
    }
