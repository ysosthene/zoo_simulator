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


class LivingBeingStateEnum(ExtendedEnum):
    ALIVE = 'alive'
    DEAD = 'dead'


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


class DietEnum(ExtendedEnum):
    CARNIVOROUS = 'carnivorous'
    HERBIVOROUS = 'herbivorous'


class AnimalSpecieDietEnum(ExtendedEnum):
    LION = DietEnum.CARNIVOROUS.value
    TIGER = DietEnum.CARNIVOROUS.value
    COYOTE = DietEnum.CARNIVOROUS.value
    ELEPHANT = DietEnum.HERBIVOROUS.value
    ANTELOPE = DietEnum.HERBIVOROUS.value
    GIRAFFE = DietEnum.HERBIVOROUS.value


class PlantspecieEnum(ExtendedEnum):
    SEAWEED = "seaweed"


class SpecieTypeEnum(ExtendedEnum):
    ANIMAL = 'animal'
    PLANT = 'plant'
