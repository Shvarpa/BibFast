def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def fix_list_to_dict(curr):
    return {str(index): curr[index] for index in range(len(curr))}


def iterate_dicts(curr, func):
    for key, value in curr.items():
        if isinstance(value, list):
            curr[key] = func(value)
        if isinstance(value, dict):
            iterate_dicts(value, func)
    return curr


def dict_get_path(dict_data, path, default=None):
    if isinstance(path, str): path = path.split('/')
    for p in path:
        if isinstance(dict_data, dict):
            dict_data = dict_data.get(p)
        else:
            return default
    return dict_data