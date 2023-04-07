"""
This class contains all the logic our enclosure.
"""

from itertools import groupby
from entities.enclosure import Enclosure


def report_enclosure_state(enclosure: Enclosure) -> str:
    if enclosure is None or not (isinstance(enclosure, Enclosure)):
        raise ValueError(
            "`enclosure` should be a valid instance of Enclosure."
        )

    report = f"""
        You could find for now {len(enclosure.get_plants())} plants
    """
    if not enclosure.get_animals():
        report += """
        There is no animal at this stage.
        """
        return report

    report += f"""
        There is also the following {len(enclosure.get_animals())} animals:
    """
    # Group animals by name and gender
    animal_groups = groupby(
        enclosure.get_animals(), lambda animal: (animal.name, animal.gender)
    )
    # (Lion, male)
    for agg, group in animal_groups:
        report += f"""
            - {agg[1]} {agg[0]} : {len(list(group))}"""

    return report


def move_forward_in_time(enclosure: Enclosure) -> Enclosure:
    """
    Triggers all related actions needed for the biodiversity
    inside an enclosure.

    Parameters
        ----------
            enclosure: Enclosure

        Returns
        -------
        Enclosure
    """

    # No actions yet

    # Trigger reportings

    # Return
    return enclosure
