from copy import deepcopy

from wagtail.wagtailcore import blocks

from streamfield_tools.blocks import (
    MultiRenditionStructBlock,
    Rendition,
    RenditionAwareLazyLoadImageChooserBlock,
    RenditionAwareListBlock,
    RenditionAwareStructBlock
)

stacks_image_form_blocks = [
    (
        'image',
        RenditionAwareLazyLoadImageChooserBlock(
            icon='image',
            abel='Image'
        )
    ),
    ('overline', blocks.TextBlock(required=False)),
    ('title', blocks.TextBlock(required=False)),
    ('additional_content', blocks.RichTextBlock(required=False))
]


stacks_image_block = MultiRenditionStructBlock(
    deepcopy(stacks_image_form_blocks),
    core_renditions=(
        Rendition(
            short_name='full_width',
            verbose_name="Full Width Image",
            description="An image that spans the full width of it's "
                        "containing div.",
            path_to_template='wagtail_stacks_image/single/'
                             'full_width.html',
            image_rendition='fill-1600x901'
        ),
        Rendition(
            short_name='image_left_content_right',
            verbose_name="Image Left, Content Right",
            description="Display an image on the left with it's accompanying "
                        "content on the right. NOTE: This rendition should "
                        "only be used if the 'Optional Content' field is "
                        "filled out.",
            path_to_template='wagtail_stacks_image/single/'
                             'image_left_content_right.html',
            image_rendition='fill-800x450'
        ),
        Rendition(
            short_name='image_right_content_left',
            verbose_name="Image Right, Content Left",
            description="Display an image on the right with it's accompanying "
                        "content on the left. NOTE: This rendition should "
                        "only be used if the 'Optional Content' field is "
                        "filled out.",
            path_to_template='wagtail_stacks_image/single/'
                             'image_right_content_left.html',
            image_rendition='fill-800x450'
        )
    ),
    addl_renditions_settings_key='stacks_image_block',
    label='Image',
    icon='image'
)


stacks_imagelist_block = MultiRenditionStructBlock(
    [
        ('title', blocks.TextBlock(required=False)),
        (
            'list', RenditionAwareListBlock(
                RenditionAwareStructBlock(
                    deepcopy(stacks_image_form_blocks),
                    template='wagtail_stacks_image/list/'
                             'list-item.html',
                    template_carousel='wagtail_stacks_image/list/'
                                      'list-item-carousel.html'
                ),
                label='Images'
            ),
        )
    ],
    [
        Rendition(
            short_name='1up',
            verbose_name="Image List 1-Up",
            description="A list of images displayed in grid with one image "
                        "in each row.",
            path_to_template='wagtail_stacks_image/list/1up.html',
            image_rendition='fill-1600x901'
        ),
        Rendition(
            short_name='2up',
            verbose_name="Image List 2-Up",
            description="A list of images displayed in grid with two "
                        "in each row.",
            path_to_template='wagtail_stacks_image/list/2up.html',
            image_rendition='fill-800x450'
        ),
        Rendition(
            short_name='3up',
            verbose_name="Image List 3-Up",
            description="A list of images displayed in grid with three "
                        "in each row.",
            path_to_template='wagtail_stacks_image/list/3up.html',
            image_rendition='fill-700x394'
        ),
        Rendition(
            short_name='carousel',
            verbose_name="Image Carousel",
            description="A list of images displayed in a javascript-powered "
                        "carousel.",
            path_to_template='wagtail_stacks_image/list/carousel.html',
            image_rendition='max-1600x901'
        )
    ],
    addl_renditions_settings_key='stacks_imagelist_block',
    label='Image List/Gallery',
    icon='image'
)
