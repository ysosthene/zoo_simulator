""" This file contains utils for the project. """

from enum import Enum


class ExtendedEnum(Enum):
    """ Customized enum class. """
    @classmethod
    def values_list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def names_list(cls):
        return list(map(lambda c: c.name, cls))


class genderEnum(ExtendedEnum):
    MALE = 'male'
    FEMALE = 'female'


class AnimalSpecieEnum(ExtendedEnum):
    LION = 'lion'
    TIGER = 'tiger'
    COYOTE = 'coyote'
    ELEPHANT = 'elephant'
    ANTELOPE = 'antelope'
    GIRAFFE = 'giraffe'


class AnimalSpecieDietEnum(ExtendedEnum):
    LION = 'carnivorous'
    TIGER = 'carnivorous'
    COYOTE = 'carnivorous'
    ELEPHANT = 'herbivorous'
    ANTELOPE = 'herbivorous'
    GIRAFFE = 'herbivorous'


class PlantspecieEnum(ExtendedEnum):
    SEAWEED = "seaweed"


class SpecieTypeEnum(ExtendedEnum):
    ANIMAL = 'animal'
    PLANT = 'plant'
