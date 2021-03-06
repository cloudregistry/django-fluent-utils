"""
Optional integration with django-any-Imagefield
"""
from __future__ import absolute_import
from django.db import models
from fluent_utils.django_compat import is_installed

if is_installed('any_imagefield'):
    from any_imagefield.models import AnyFileField as BaseFileField, AnyImageField as BaseImageField
else:
    BaseFileField = models.FileField
    BaseImageField = models.ImageField


# subclassing here so South or Django migrations detect a single class.
class AnyFileField(BaseFileField):
    """
    A FileField that can refer to an uploaded file.

    If *django-any-imagefield* is not installed, the filebrowser link will not be displayed.
    """
    def south_field_triple(self):
        # Masquerade as normal FileField, so the soft-dependency also exists in the migrations.
        from south.modelsinspector import introspector
        path = "{0}.{1}".format(models.FileField.__module__, models.FileField.__name__)
        args, kwargs = introspector(self)
        return (path, args, kwargs)

    def deconstruct(self):
        # For Django 1.7 migrations, masquerade as normal FileField too
        name, path, args, kwargs = super(AnyFileField, self).deconstruct()
        path = "{0}.{1}".format(models.FileField.__module__, models.FileField.__name__)
        return name, path, args, kwargs


# subclassing here so South or Django migrations detect a single class.
class AnyImageField(BaseImageField):
    """
    An ImageField that can refer to an uploaded image file.

    If *django-any-imagefield* is not installed, the filebrowser link will not be displayed.
    """
    def south_field_triple(self):
        # Masquerade as normal ImageField, so the soft-dependency also exists in the migrations.
        from south.modelsinspector import introspector
        path = "{0}.{1}".format(models.ImageField.__module__, models.ImageField.__name__)
        args, kwargs = introspector(self)
        return (path, args, kwargs)

    def deconstruct(self):
        # For Django 1.7 migrations, masquerade as normal ImageField too
        name, path, args, kwargs = super(AnyImageField, self).deconstruct()
        path = "{0}.{1}".format(models.ImageField.__module__, models.ImageField.__name__)
        return name, path, args, kwargs
