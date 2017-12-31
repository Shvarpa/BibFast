import ctypes


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


def filter_dict(data, filter_path=None, filter_item=None):
    if isinstance(filter_item, str): filter_item = tuple(None if x == '' else x for x in filter_item.split(':'))
    if filter_item[0] and filter_item[1]:
        data = {k: v for k, v in data.items() if filter_item in dict_get_path(data[k], filter_path, {}).items()}
    elif filter_item[1]:
        data = {k: v for k, v in data.items() if
                filter_item[1] == dict_get_path(data[k], filter_path, {}).get(filter_item[0])}
    elif filter_item[0]:
        data = {k: v for k, v in data.items() if filter_item[0] in dict_get_path(data[k], filter_path, {})}
    return data


def dict_get_path(data, path, default=None):
    if isinstance(path, str): path = path.split('/')
    for p in path:
        if isinstance(data, dict):
            data = data.get(p)
        else:
            return default
    return data


def hide_file(filename):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ret = ctypes.windll.kernel32.SetFileAttributesW(filename, FILE_ATTRIBUTE_HIDDEN)
    return ret
