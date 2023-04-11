""" This file contains utils for the project. """

import os
import datetime
from enum import Enum

CONFIG_FILENAME = "data/config.yaml"
LOG_REPORT_PATH = "log_reports/report.txt"


def log_to_file(content: str):
    path = LOG_REPORT_PATH
    mode = "w"
    if os.path.isfile(path):
        mode = "a"

    with open(path, mode=mode) as file:
        file.write(
            f"""
------------- {datetime.datetime.now()} -------------
{content}
"""
        )


class ExtendedEnum(Enum):
    """Customized enum class."""

    @classmethod
    def values_list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def names_list(cls):
        return list(map(lambda c: c.name, cls))


class LivingBeingStateEnum(ExtendedEnum):
    ALIVE = "alive"
    DEAD = "dead"


class genderEnum(ExtendedEnum):
    MALE = "male"
    FEMALE = "female"


class AnimalSpecieEnum(ExtendedEnum):
    LION = "lion"
    TIGER = "tiger"
    COYOTE = "coyote"
    ELEPHANT = "elephant"
    ANTELOPE = "antelope"
    GIRAFFE = "giraffe"


class DietEnum(ExtendedEnum):
    CARNIVOROUS = "carnivorous"
    HERBIVOROUS = "herbivorous"


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
    ANIMAL = "animal"
    PLANT = "plant"
