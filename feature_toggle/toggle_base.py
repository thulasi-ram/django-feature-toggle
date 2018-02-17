# -*- coding: utf-8 -*-
import abc


class BaseToggle(object):
    """
    Interface for implementing toggle class
    """

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError('Subclasses must define name property')

    @abc.abstractproperty
    def code(self):
        raise NotImplementedError('Subclasses must define code property')

    @abc.abstractproperty
    def environment(self):
        raise NotImplementedError('Subclasses must define environment property')

    @abc.abstractmethod
    def is_active(self):
        raise NotImplementedError('Subclasses must define is_active method')

    @abc.abstractmethod
    def is_enabled(self):
        raise NotImplementedError('Subclasses must define is_enabled method')

    def __bool__(self):
        return self.is_active()
    __nonzero__=__bool__
