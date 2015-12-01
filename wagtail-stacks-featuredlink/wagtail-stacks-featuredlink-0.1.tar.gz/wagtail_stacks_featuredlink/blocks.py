from copy import deepcopy

from wagtail.wagtailcore.blocks import (
    BooleanBlock,
    TextBlock,
    RichTextBlock,
    StructBlock,
    PageChooserBlock,
    URLBlock,
    CharBlock
)

from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from streamfield_tools.blocks import (
    Rendition,
    MultiRenditionStructBlock,
    RenditionAwareStructBlock,
    RenditionAwareLazyLoadImageChooserBlock,
    RenditionAwareListBlock
)

anchor_tag_help_text = (
    "Anchor tags should be all lowercase, without special characters and with "
    "dashes instead of spaces (i.e. 'recipes-section' not 'Recipes Section')."
)

stacks_featuredlink_anchor_tag = CharBlock(
    icon='link',
    template='wagtail_stacks_featuredlink/anchor-tag.html',
    label='Anchor Tag',
    help_text=anchor_tag_help_text
)


class MultiSourceLinkBlock(StructBlock):

    class Meta:
        template = None

    def __init__(self, **kwargs):
        super(MultiSourceLinkBlock, self).__init__(
            local_blocks=[
                ('page', PageChooserBlock(required=False)),
                ('document', DocumentChooserBlock(required=False)),
                ('url', URLBlock(required=False, label='External Link')),
                (
                    'anchor_tag',
                    CharBlock(
                        required=False,
                        label='Anchor Tag',
                        help_text=(
                            "Anchor tags should be all lowercase, without "
                            "special characters and with dashes instead of "
                            "spaces (i.e. 'recipes-section' not 'Recipes "
                            "Section')."
                        )
                    )
                )
            ],
            **kwargs
        )

    def render_basic(self, value):
        if value.get('page'):
            url = value.get('page').url
        elif value.get('document'):
            url = value.get('document').url
        elif value.get('url'):
            url = value.get('url')
        else:
            url = ''
        if value.get('anchor_tag'):
            url = '{url}#{anchor_tag}'.format(
                url=url,
                anchor_tag=value.get('anchor_tag')
            )
        return url

stacks_featured_link_form_blocks = [
    ('image', RenditionAwareLazyLoadImageChooserBlock(required=False)),
    (
        'link', MultiSourceLinkBlock(
            help_text=(
                'Enter a URL or select either a page or a document to '
                'build this link to.'
            )
        )
    ),
    ('overline', TextBlock(required=False)),
    ('title', TextBlock()),
    ('additional_content', RichTextBlock(required=False))
]

stacks_featuredlink_button = StructBlock(
    [
        (
            'link', MultiSourceLinkBlock(
                help_text=(
                    'Enter a URL or select either a page or a document to '
                    'build this link to.'
                ),
                required=True
            )
        ),
        ('link_text', TextBlock()),
        (
            'new_window',
            BooleanBlock(
                label='Open In New Window',
                default=False,
                required=False,
                help_text="Check this box if you'd like for this button to "
                          "load this link in a new browser window."
            )
        ),
        (
            'addl_classes',
            TextBlock(
                label='Additional Classes',
                required=False,
                help_text="Enter any additional classes you'd like to add "
                          "to this button (to enable custom styling)."
            )
        )
    ],
    icon='link',
    label='Button Link',
    template='wagtail_stacks_featuredlink/button.html'
)

stacks_featuredlinklist_block = MultiRenditionStructBlock(
    [
        ('title', TextBlock(required=False)),
        ('links', RenditionAwareListBlock(
            RenditionAwareStructBlock(
                deepcopy(stacks_featured_link_form_blocks),
                template='wagtail_stacks_featuredlink/list/'
                         'list-item.html'
            )
        ))
    ],
    core_renditions=(
        Rendition(
            short_name='1up',
            verbose_name="Featured Link List 1-Up",
            description="A list of featured link modules displayed in grid "
                        "with one featured link in each row.",
            path_to_template='wagtail_stacks_featuredlink/list/1up.html',
            image_rendition='fill-1600x901'
        ),
        Rendition(
            short_name='2up',
            verbose_name="Featured Link List 2-Up",
            description="A list of featured link modules displayed in grid "
                        "with two featured links in each row.",
            path_to_template='wagtail_stacks_featuredlink/list/2up.html',
            image_rendition='fill-800x450'
        ),
        Rendition(
            short_name='3up',
            verbose_name="Featured Link List 3-Up",
            description="A list of featured link modules displayed in grid "
                        "with three featured links in each row.",
            path_to_template='wagtail_stacks_featuredlink/list/3up.html',
            image_rendition='fill-700x394'
        ),
    ),
    addl_renditions_settings_key='stacks_featuredlinklist_block',
    label='Featured Link List',
    icon='link'
)
