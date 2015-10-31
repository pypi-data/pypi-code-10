from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Extra(models.Model):
    field_name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __str__(self):
        return "{}: {}".format(self.field_name, self.value)

class Person(models.Model):
    order = models.PositiveIntegerField(default=0)

    extras = models.ManyToManyField(Extra, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)

    class Meta:
        abstract = True

class OtherPeople(Person):
    text = models.CharField(max_length=2048, default="")

    class Meta:
        verbose_name_plural = 'Other people'

    def __str__(self):
        return self.text

class Human(Person):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    role = models.CharField(max_length=256)

    location = models.CharField(max_length=512, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['order', 'last_name']

    def __str__(self):
        return "{}: {} {}".format(self.role, self.first_name, self.last_name)

    def email_safe(self):
        return self.email.replace("@" ," [at] ")

