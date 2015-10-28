# coding: utf-8

"""
django informer checker base
"""

from informer.models import post_check


class InformerException(Exception):
    """
    A class to deal with exceptions.
    """
    pass


class Support(type):
    """
    A helper to automate the bind of features from Informer.
    """

    @staticmethod
    def trigger(func):
        """
        Trigger fired after checking by the signal.
        """
        def helper(instance, *args, **kwargs):
            result = func(instance, *args, **kwargs)

            measures = instance.__class__.get_measures()

            for measure in measures:

                if measure == 'check_availability':
                    value = result[0]
                else:
                    value = getattr(instance, measure, None)()

                post_check.send(
                    sender=instance, measure=measure, value=value)

            return result

        return helper

    def __new__(cls, clsname, superclasses, attributedict):
        """
        On instantiation, the trigger is added.
        """
        attributedict['check'] = cls.trigger(attributedict['check'])

        return type.__new__(cls, clsname, superclasses, attributedict)


class BaseInformer(object):
    """
    A base class to serve as infrastructure to new 'Informers'.
    """

    __metaclass__ = Support

    def __str__(self):
        return u'A small and explicit description from informer.'

    def check(self):
        """
        Each informer need 'inspect' the monitored resource or service.
        """
        raise NotImplementedError

    @staticmethod
    def get_class(namespace, classname):
        """
        Dynamic import from Informer
        """
        try:
            module = __import__(namespace, globals(), locals(), [classname])
            cls = getattr(module, classname)
        except ImportError:
            raise InformerException(
                '%s is unknown or undefined.' % classname)
        except AttributeError:
            raise InformerException(
                'The %s does not exists on %s.' % (classname, namespace))
        except Exception as error:
            raise InformerException(
                'A general exception occurred: %s.' % error)

        if not issubclass(cls, BaseInformer):
            raise InformerException('%s is not a Informer.' % classname)

        return cls

    @classmethod
    def get_measures(cls):
        """
        Get measures from Informer
        """
        measures = ['check_availability']  # initialized with default measure
        measures += [attr for attr in dir(cls) if attr.startswith('check_')]

        return measures
