# import random
# import pickle


def get_all_unicode():
    '''Generates all unicode characters in the specified ranges and stores
    it in a list which can randomly be selected from'''

    try:
        get_char = unichr
    except NameError:
        get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [  # these ranges selected for interesting non-alphanumeric characters with minimal gaps

        (0x2200, 0x22FF), # Mathematical Operators
        (0x0400, 0x04FF), # Cyrillic
        (0x0250, 0x02AF), # IPA Extensions
        (0x30A0, 0x30FF), # Katakana, almost no missing characters
        (0x0600, 0x06FF), # Arabic
        (0x03A3, 0x03FF), # Greek
        (0x05D0, 0x05EA), # Hebrew, no missing characters
        (0x0904, 0x0939), # Devanagari
        (0xF900, 0xFA6D), # CJK compatibility ideographs, almost no missing characters
    ]

    alphabet = [  # generate all unicode in ranges
        get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)
    ]

    return alphabet
