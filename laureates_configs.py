from json_dict_processing import create_processor, ProcessorDict
from prizes_configs import prize_processor


def process_year(year_string: object) -> int | None:
    """
    Extracts the year from a "YYYY-MM-DD" format string.

    :param year_string: Date string to parse.
    :return: Year as int, or None if parsing is not possible.
    """
    if isinstance(year_string, str) and len(year_string) >= 4:
        return int(year_string[:4])
    else:
        return None


CONFIG_PERSON = {
    "id": ["id"],
    "name": ["knownName", "en"],
    "gender": ["gender"],
    "birth_year": (["birth", "date"], process_year),
    "country_birth": ["birth", "place", "country", "en"],
    "country_now": ["birth", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor()),
}

CONFIG_ORG = {
    "id": ["id"],
    "name": ["orgName", "en"],
    "founded_year": (["founded", "date"], process_year),
    "country_founded": ["founded", "place", "country", "en"],
    "country_now": ["founded", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor()),
}


def person_processor() -> ProcessorDict:
    """
    Creates a processor for person laureates.

    :return: Processor function using the CONFIG_PERSON.
    """
    return create_processor(CONFIG_PERSON)


def org_processor() -> ProcessorDict:
    """
    Creates a processor for organization laureates.

    :return: Processor function using the CONFIG_ORG.
    """
    return create_processor(CONFIG_ORG)


process_person = person_processor()
process_org = org_processor()
