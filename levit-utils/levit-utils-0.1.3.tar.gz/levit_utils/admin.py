class ImagePreviewAdminMixin(object):

  class Media:
    css = {'all': ('adminsortable/css/sortable.css',)}
    js = (
      'adminsortable/js/plugins/admincompat.js',
      'adminsortable/js/libs/jquery.ui.core-1.10.3.js',
      'adminsortable/js/libs/jquery.ui.widget-1.10.3.js',
      'adminsortable/js/libs/jquery.ui.mouse-1.10.3.js',
      'adminsortable/js/libs/jquery.ui.sortable-1.10.3.js',
      'js/preview.js',
    )


class SortableImagePreviewAdminMixin(object):

  class Media:
    css = {'all': ('adminsortable/css/sortable.css',)}
    js = (
      'adminsortable/js/plugins/admincompat.js',
      'adminsortable/js/libs/jquery.ui.core-1.10.3.js',
      'adminsortable/js/libs/jquery.ui.widget-1.10.3.js',
      'adminsortable/js/libs/jquery.ui.mouse-1.10.3.js',
      'adminsortable/js/libs/jquery.ui.sortable-1.10.3.js',
      'js/preview.js',
    )
