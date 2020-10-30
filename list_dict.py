def safe_list_get(item, index, default=None):
    try:
        return item[index]
    except IndexError:
        return default


def safe_rest_of_list(item, index, default=None):
    try:
        return item[index:]
    except IndexError:
        return default


def find_item_by_attr(list_dict, attr, search):
    for item in list_dict:
        if item[attr] == search:
            return item
