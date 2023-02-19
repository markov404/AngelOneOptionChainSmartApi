

def sort_by_name_of_option_and_split_result_on_chunks(
        options_map: dict, names: set) -> dict:
    utility_dictionary = dict()
    for name in names:
        utility_dictionary[name] = []

    for option in options_map:
        utility_dictionary[option['name']].append(option)

    # on this step i am planning to do sorting

    for key in utility_dictionary.keys():
        list_of_options = utility_dictionary[key]
        chunks_of_options = list_split_on_chunks(list_of_options, 1000)
        utility_dictionary[key] = chunks_of_options

    return utility_dictionary


def make_token_list_for_web_socket(options_map: list) -> list:
    token_list = []
    for opt in options_map:
        try:
            token_list.append(str(opt['token']))
        except BaseException:
            next

    return token_list


def make_set_of_option_names(options_map: list) -> set:
    set_of_names = set()
    for option in options_map:
        try:
            st_one = (option['name'] not in set_of_names)
            st_two = (option['name'] != '')
            st_three = (isinstance(option['name'], str))
            if st_one and st_two and st_three:
                set_of_names.add(option['name'])
        except BaseException:
            next

    return set_of_names


def list_split_on_chunks(listA, n):
    chunks = []
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n + x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n - len(every_chunk))]
        removed_none_items = [x for x in every_chunk if x is not None]

        chunks.append(removed_none_items)
    return chunks


def check_on_error(msg) -> Exception:
    if "errorCode" in msg:
        raise Exception(f"{msg}")
