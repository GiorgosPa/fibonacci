blacklisted_numbers = set()


def blacklist_number(number: int):
    blacklisted_numbers.add(number)


def whitelist_number(number: int):
    blacklisted_numbers.remove(number)
