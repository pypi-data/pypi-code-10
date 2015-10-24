from os.path import join

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from erp.base.directory.models import Person


class MaterialsManager(models.Manager):

    def materials(self):
        return DynamicItem.objects.all()


class Category(models.Model):

    def get_cat_upload_path(self, filename):
        ext = filename.split('.')[-1]
        return join("storage", "cat_%s" % self.slug, 'title.{}'.format(ext))

    title = models.CharField(max_length=20)
    slug = models.SlugField()
    parent = models.ForeignKey('Category', related_name='child_cat', blank=True, null=True)
    pic = models.ImageField(upload_to=get_cat_upload_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('storage-category', kwargs={'slug': self.slug})


class Nomenclature(models.Model):

    KILOGRAM = 'kg'
    GRAMM = 'gm'
    LITER = 'l'
    MILLILITER = 'ml'
    UNIT = 'u'
    UNIT_CHOICES = (
        (UNIT, 'Unit'),
        (KILOGRAM, 'Kilogram'),
        (GRAMM, 'Gram'),
        (LITER, 'Liter'),
        (MILLILITER, 'Milliliter')
    )

    objects = MaterialsManager()

    def get_goods_upload_path(self, filename):
        ext = filename.split('.')[-1]
        return join("storage", "cat_%s" % self.cat.slug, '{}.{}'.format(self.slug, ext))

    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    cat = models.ForeignKey(Category, related_name='nomenclature', null=True, blank=True)
    # rel_cat = models.ManyToManyField(Category, related_name='related_nomenclature', blank=True)
    desc = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to=get_goods_upload_path, blank=True, null=True)
    adopted = models.DateField(auto_now_add=True, editable=False)
    unit = models.CharField(choices=UNIT_CHOICES, max_length=5)

    class Meta:
        verbose_name_plural = "nomenclature"

    # def save(self, *args, **kwargs):
    #
    #     if not self.pic:
    #         self.pic = self.cat.pic
    #     super(Nomenclature, self).save()

    # def get_absolute_url(self):
    #     return reverse('storage-nomenclature', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    @property
    def quantity(self):
        return self.st_items.count() + self.dyn_items.count()

    def available(self):
        if len(self.st_items.all()) > 0:
            return len([i for i in self.st_items.all() if i.is_available])
        elif len(self.dyn_items.all()) > 0:
            return self.dyn_items.aggregate(models.Sum(models.F('quantity')))
        else:
            return 0


class StaticItem(models.Model):

    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    pos = models.ForeignKey(Nomenclature, related_name='st_items')
    desc = models.CharField(max_length=200, null=True, blank=True)
    invent_no = models.CharField(max_length=10, null=True, blank=True, unique=True)
    quantity = models.IntegerField(default=0)

    @property
    def is_available(self):
        if self.shipment_log.count() < self.adoption_log.count():
            return False
        else:
            return True

    def __str__(self):
        return self.desc

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         super(StorageItem, self).save(*args, **kwargs)
    #     if 'quantity' in kwargs:
    #         self.quantity += kwargs['quantity']
    #         super(StorageItem, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('storage-item', kwargs={'pk': self.pk})


class DynamicItem(models.Model):

    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    desc = models.CharField(max_length=200, null=True, blank=True)
    adopted = models.DateField(auto_now_add=True, editable=False)
    quantity = models.FloatField(default=0)

    @property
    def is_available(self):
        if self.shipment_log.count() < self.adoption_log.count():
            return False
        else:
            return True

    def __str__(self):
        return self.desc


class StorageItemShipmentLog(models.Model):

    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label__in': ['dynamic item', 'static item']})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    shipped_to = models.ForeignKey(Person)
    when = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        get_latest_by = 'when'

    def save_from_ajax(self, fields):
        if fields['id'] is not None:
            self.id = fields['id']
            if fields['DELETE']:
                self.delete()
                return
        elif fields['DELETE']:
                return

        self.content_type = fields['content_type']
        self.object_id = fields['object_id']
        self.shipped_to_id = fields['shipped_to_id']
        self.comment = fields['comment']
        self.save()


class StorageItemAdoptionLog(models.Model):

    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label__in': ['dynamic item', 'static item']})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    when = models.DateTimeField(auto_now_add=True, editable=False)
    waybill = models.CharField(max_length=20, null=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        get_latest_by = 'when'

    def save_from_ajax(self, fields):
        if fields['id'] is not None:
            self.id = fields['id']
            if fields['DELETE']:
                self.delete()
                return
        elif fields['DELETE']:
                return

        self.content_type = fields['content_type']
        self.object_id = fields['object_id']
        self.waybill = fields['waybill']
        self.comment = fields['comment']
        self.save()
