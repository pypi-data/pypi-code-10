from unittest import TestCase

import markdown
from mdx_picture import PictureExtension


class MdxPictureBlockParsingTest(TestCase):
    def testImgOrder(self):
        """Test mixed order of the img block and source blocks inside \
        the picture"""
        mixed_img_order_mdx = """
Hello World my Babald

[picture]
    [64em]: high-res.jpg
    ![This picture loads on non-supporting browsers.]\
(image.jpg "The image title")
    [37.5em]: med-res.jpg
    [0em]: low-res.jpg
[/picture]

One more time
"""
        mixed_img_order_html = """<p>Hello World my Babald</p>\n\
<picture><source media="(min-width: 64em)" src="high-res.jpg"></source>\
<source media="(min-width: 37.5em)" src="med-res.jpg"></source>\
<source media="(min-width: 0em)" src="low-res.jpg"></source>\
<img alt="This picture loads on non-supporting browsers." src="image.jpg" \
title="The image title" /></picture><p>One more time</p>"""

        self.assertEqual(mixed_img_order_html,
                         markdown.markdown(mixed_img_order_mdx,
                         extensions=[PictureExtension()]))
