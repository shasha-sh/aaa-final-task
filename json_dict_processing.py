from typing import Callable

KeyPath = list[str | int]
Config = dict[str, KeyPath | tuple[KeyPath, Callable[[object], object | None]]]
ProcessorDict = Callable[[dict[str, object]], dict[str, object | None]]
ProcessorList = Callable[
    [list[dict[str, object]] | None],
    list[dict[str, object | None]]
]


def extract_nested_value(obj: object, keys: KeyPath) -> object | None:
    """
    Extracts a value from nested data structures by a chain of keys.

    :param obj: Nested data structure (dict or list) to extract from.
    :param keys: Chain of keys.
    :return: The extracted value, or None if the path does not exist.
    """
    cur = obj
    for k in keys:
        if isinstance(k, str) and isinstance(cur, dict):
            if k in cur:
                cur = cur[k]
            else:
                return None
        elif isinstance(k, int) and isinstance(cur, list):
            if 0 <= k < len(cur):
                cur = cur[k]
            else:
                return None
        else:
            return None
    return cur


def process_dictionary_with_config(dictionary: dict[str, object],
                                   config: Config) -> dict[str, object | None]:
    """
    Processes a single dictionary according to a config dictionary.

    :param dictionary: Dictionary to be processed.
    :param config: Config dict: for each name provide a path, or a (path, function) pair.
    :return: Dictionary with extracted values.
    """
    res = {}
    for name, path_info in config.items():
        if isinstance(path_info, list):
            res[name] = extract_nested_value(dictionary, path_info)
        elif isinstance(path_info, tuple):
            path, f = path_info
            res[name] = f(extract_nested_value(dictionary, path))
        else:
            raise TypeError(f"Incorrect config format: must be path"
                            f" or (path, function), got {path_info}.")
    return res


def process_list_of_dicts_with_config(list_of_dicts: list[dict[str, object]],
                                      config: Config) -> list[dict[str, object | None]]:
    """
    Processes a list of dictionaries.

    :param list_of_dicts: List of dictionaries to be processed.
    :param config: Config dict: for each name provide a path,
    or a (path, function) pair.
    :return: List of dictionaries with extracted values.
    """
    res = []
    for dct in list_of_dicts:
        res.append(process_dictionary_with_config(dct, config))
    return res


def create_processor(config: Config,
                     list_processor: bool = False) -> ProcessorDict | ProcessorList:
    """
    Creates a ready processor with a preloaded configuration.
    If list_processor == True, process_list_of_dicts_with_config
    is passed inside the processor;
    otherwise process_dictionary_with_config.

    :param config: Config dict: for each name provide a path, or
    a (path, function) pair.
    :param list_processor:  Flag indicating the processor type to create.
    :return: Processor function using the given config.
    """
    if list_processor:
        return lambda lst: process_list_of_dicts_with_config(lst, config)
    return lambda d: process_dictionary_with_config(d, config)


if __name__ == "__main__":
    dct = {"a": {"b": [{"c": 1}], "d": {"e": "2001-05-01"}}}
    assert extract_nested_value(dct, ["a", "b", 0, "c"]) == 1
    assert extract_nested_value(dct, ["a", "z"]) is None
    cfg = {
        "val": ["a", "b", 0, "c"],
        "y": (["a", "d", "e"], lambda s: int(s[:4])),
    }
    res = process_dictionary_with_config(dct, cfg)
    assert res["val"] == 1 and res["y"] == 2001
