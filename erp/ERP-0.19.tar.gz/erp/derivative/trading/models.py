from os.path import join, basename
from django.db import models
from gm2m import GM2MField
from erp.base.storage.models import Nomenclature, StaticItem, DynamicItem
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image


class Category(models.Model):

    def get_cat_upload_path(self, filename):
        ext = filename.split('.')[-1]
        return join("trading", "cat_%s" % self.slug, 'title.{}'.format(ext))

    title = models.CharField(max_length=20)
    slug = models.SlugField()
    parent = models.ForeignKey('Category', related_name='child_cat', blank=True, null=True)
    pic = models.ImageField(upload_to=get_cat_upload_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class ProductGallery(models.Model):

    def get_gallery_upload_path(self, filename):
        name = filename.split('.')[0]
        ext = filename.split('.')[-1]
        return join("trading", "%s" % self.product.cat.slug, "%s" % self.product.slug, '{}.{}'.format(name, ext))

    product = models.ForeignKey('Product', blank=True, null=True, related_name='gallery')
    image = models.ImageField(upload_to=get_gallery_upload_path, blank=True, null=True)


class Product(models.Model):
    def get_products_upload_path(self, filename):
        ext = filename.split('.')[-1]
        return join("trading", "%s" % self.cat.slug, "%s" % self.slug, '{}.{}'.format('logo', ext))

    title = models.CharField(max_length=50)
    slug = models.SlugField()
    desc = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=get_products_upload_path)
    cat = models.ForeignKey('Category', blank=True, null=True)
    rel_cat = models.ManyToManyField(Category, related_name='additional_products', blank=True)
    items = models.ManyToManyField(DynamicItem, through='ProductAssoc', related_query_name='parent')

    def save(self, size=(200, 200)):
        if not self.logo:
            return
        super(Product, self).save()
        pw = self.logo.width
        ph = self.logo.height
        nw = size[0]
        nh = size[1]

        # only do this if the image needs resizing
        if (pw, ph) != (nw, nh):
            filename = str(self.logo.path)
            image = Image.open(filename)
            pr = float(pw) / float(ph)
            nr = float(nw) / float(nh)

            if pr > nr:
                # photo aspect is wider than destination ratio
                tw = int(round(nh * pr))
                image = image.resize((tw, nh), Image.ANTIALIAS)
                l = int(round(( tw - nw ) / 2.0))
                image = image.crop((l, 0, l + nw, nh))
            elif pr < nr:
                # photo aspect is taller than destination ratio
                th = int(round(nw / pr))
                image = image.resize((nw, th), Image.ANTIALIAS)
                t = int(round(( th - nh ) / 2.0))
                print((0, t, nw, t + nh))
                image = image.crop((0, t, nw, t + nh))
            else:
                image = image.resize(size, Image.ANTIALIAS)

            filename = 'logo'
            path = join("trading", "%s" % self.cat.slug, "%s" % self.slug, "%s" % '200x200', filename)
            image.save(path)

    @property
    def available(self):
        for i in self.items:
            if not i.is_available:
                return False
        return True

    def sale(self, person_id=None):
        if not self.available or person_id is None:
            return False
        for item in self.items:
            item.shipment_log.create(shipped_to_id=person_id)
            item.content_object.quantity -= item.count
            item.content_object.save()
        return True


class ProductAssoc(models.Model):
    #product = models.ForeignKey(Product, related_name='items')
    parent = models.ForeignKey(Product, null=True)
    material = models.ForeignKey(DynamicItem, null=True)
    count = models.FloatField()

    @property
    def available(self):
        return self.content_object.is_available() >= self.count

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
        self.count = fields['count']
        self.product_id = fields['product_id']
        self.save()
