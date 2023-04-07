""" This file contains utils for the project. """

from enum import Enum


class ExtendedEnum(Enum):
    """ Customized enum class. """
    @classmethod
    def values_list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def keys_list(cls):
        return list(map(lambda c: c.key, cls))


class genderEnum(ExtendedEnum):
    MALE = 'male'
    FEMALE = 'female'
