from json_dict_processing import create_processor, ProcessorList


def parse_int(x: object) -> int | None:
    """
    Parse value as int.

    :param x: Input value.
    :return: int on success, otherwise None.
    """
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def parse_float(x: object) -> float | None:
    """
    Parse value as float.

    :param x: Input value.
    :return: float on success, otherwise None.
    """
    try:
        if x is None:
            return None
        s = str(x).replace(" ", "").replace(",", ".")
        return float(s)
    except (TypeError, ValueError):
        return None


CONFIG_PRIZE = {
    "prize_amount": (["prizeAmount"], parse_float),
    "prize_amount_adjusted": (["prizeAmountAdjusted"], parse_float),
    "award_year": (["awardYear"], parse_int),
    "category_en": ["category", "en"],
    "prize_status": ["prizeStatus"],
}


def prize_processor() -> ProcessorList:
    """
    Creates a processor for prize lists.

    :return: Processor function using the CONFIG_PRIZE.
    """
    return create_processor(CONFIG_PRIZE, list_processor=True)
