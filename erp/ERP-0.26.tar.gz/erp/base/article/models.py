from os.path import join

from django.db import models

from erp.base.directory import Person


class Category(models.Model):
    def get_cat_upload_path(self, filename):
        ext = filename.split('.')[-1]
        return join("article", "cat_%s" % self.slug, 'title.{}'.format(ext))

    title = models.CharField(max_length=20)
    slug = models.SlugField()
    parent = models.ForeignKey('Category', related_name='child_cat', blank=True, null=True)
    pic = models.ImageField(upload_to=get_cat_upload_path, null=True, blank=True)

    class Meta():
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-category', kwargs={'slug': self.slug})



class Tag(models.Model):

    title = models.CharField(max_length=20)
    slug = models.SlugField()
    desc = models.TextField()

    class Meta():
        verbose_name_plural = "tags"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-tag', kwargs={'slug': self.slug})


class Article(models.Model):

    def get_img_upload_path(self, filename):
        ext = filename.split('.')[-1]
        return join("article", "%s" % self.cat.slug, '{}.{}'.format(self.slug, ext))

    title = models.CharField(max_length=100)
    slug = models.SlugField()
    cat = models.ForeignKey(Category, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles')
    img = models.ImageField(upload_to=get_img_upload_path, null=True, blank=True)
    body = models.TextField()
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
    author = models.ForeignKey(Person)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Img(models.Model):

    def get_img_upload_path(self, filename):
        return join("article", "%s" % self.article.cat.slug, filename)

    article = models.ForeignKey(Article, related_name='images')
    img = models.ImageField(upload_to=get_img_upload_path)

    class Meta():
        verbose_name = 'image'
        verbose_name_plural = 'images'