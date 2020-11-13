import re


MAPPING_SUPERSCRIPTS = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸',
                        '9': '⁹', '-': '⁻'}

non_negative_int_regex = re.compile(r'(((0)+)|([1-9]\d*))')
num_regex = re.compile(fr'(([-]?[.]\d+)|([-+]?\d+[.]\d*)|([-+]?{non_negative_int_regex.pattern}))')
term_border = re.compile(r'(^|([\-+*=/])|$)')
degree_part_regex = re.compile(fr'([-+]?X(\^({non_negative_int_regex.pattern}|(\([-+]?'
                               fr'{non_negative_int_regex.pattern}\))))?)')
term_regex = re.compile(fr'(({num_regex.pattern}|{degree_part_regex.pattern}){term_border.pattern})|$')
polynomial_regex = re.compile(fr'^({term_regex.pattern})+$')
