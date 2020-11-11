#!/usr/bin/env python3
import string
import re
import readline
from sys import argv


term_polynom_regex = re.compile(r'X(((\^)|(\*\*))((\d+)|(\(([+-]?\d+)\))))?')
num_regex = re.compile(r'([-+]?[.]\d+)|([-+]?\d+[.]?\d*)')
term_regex = re.compile(rf'((({num_regex.pattern})|({term_polynom_regex.pattern}))(([+*-/](?=.))|$))')


MAPPING_SUPERSCRIPTS = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸',
                        '9': '⁹', '-': '⁻'}


def abs(a):
    return a if a >= 0 else -a


def max(iter_obj):
    lst = list(iter_obj)
    max_object = lst[0]
    for num in lst:
        if num > max_object:
            max_object = num
    return max_object


def min(iter_obj):
    lst = list(iter_obj)
    min_object = lst[0]
    for num in lst:
        if num < min_object:
            min_object = num
    return min_object


def sqrt(n):
    sgn = 0
    if n < 0:
        sgn = -1
        n = -n
    val = n
    while True:
        last = val
        val = (val + n / val) * 0.5
        if abs(val - last) < 1e-9:
            break
    if sgn < 0:
        return complex(0, val)
    return val


def decimal2common_fraction(number):
    if number == 0:
        return '0/1'
    sign = '' if number >= 0 else '-'
    number = abs(float(number))
    num, denom = 1, 1
    for _ in range(10_000):
        while num / denom > number:
            denom += 1
        if number - num / denom < 1e-12:
            break
        num += 1
    else:
        num = num / denom
        denom = 1
    if denom == 1:
        num = str(num)
    else:
        num = f'{num}/{denom}'
    return f'{sign}{num}'


def parse_term(term: str):
    if not term:
        return None

    res = re.fullmatch(num_regex, term)
    if res:
        num = float(res.group())
        return {'coef': num}
    res = term_polynom_regex.fullmatch(term)
    if res:
        return {'degree': int(res.group(6) or res.group(8) or 1)}


def search_terms(polynom_part):
    return [[r[1], r[-1]] for r in term_regex.findall(polynom_part)]


def get_alphabet_symbols(polynomial):
    symbols = ''.join(set(re.findall(r'[a-zA-Zа-яА-Я_]', polynomial)))
    return symbols


def is_valid_polynomial(polynomial: str):
    if polynomial.count('=') != 1:
        print('Это не уравнение')
        return False
    if len(get_alphabet_symbols(polynomial)) > 1:
        print('В уравнении должен быть только не больше одной однобуквенной неизвестной')
        return False
    invalid_symbols = set(polynomial) - set(f'{string.digits}.=*/+-^ X()')
    if invalid_symbols:
        invalid_symbols = ''.join(invalid_symbols)
        print(f'Встречаются недопустимые символы: `{invalid_symbols}`')
        return False
    for polynom_part in polynomial.split('='):
        if not re.fullmatch(f'{term_regex.pattern}+', polynom_part):
            print(f"Неверная часть уравнения: '{polynom_part}'")
            search_terms(polynom_part)
            return False
    return True


def look_major_degree(polynom_map):
    return max(polynom_map)


def is_valid_degrees(polynom_map):
    return not set(polynom_map) - {0, 1, 2}


def calc_discriminant(polynom_map):
    return polynom_map.get(1, 0) * polynom_map.get(1, 0) - 4 * polynom_map.get(0, 0) * polynom_map.get(2, 0)


def combine_similar_terms(terms: list):
    combine_terms = {}
    for term in terms:
        degree = term['degree']
        combine_terms[degree] = combine_terms.get(degree, {})
        combine_terms[degree]['coef'] = combine_terms[degree].get('coef', 0) + term['coef']
    return {degree: coef['coef'] for degree, coef in combine_terms.items() if coef['coef']} or {0: 0.0}


def parse_polynom(polynom, is_print_debug_info=False):
    all_terms = []
    for i, part in enumerate(polynom.split('=')):
        curr_operation = ''
        coef = 1
        degree = 0
        for term, next_operation in search_terms(part):
            new_term = parse_term(term)
            if curr_operation == '/':
                coef /= new_term.get('coef', 1) * (-1 if curr_operation == '-' else 1)
                degree -= new_term.get('degree', 0)
            else:
                coef *= new_term.get('coef', 1) * (-1 if curr_operation == '-' else 1)
                degree += new_term.get('degree', 0)
            if is_print_debug_info:
                print(f'{term=},{curr_operation=}, {next_operation=}')
                print(f'{coef=},{degree=}')
            if not next_operation or next_operation == '+' or next_operation == '-':
                all_terms.append({'degree': degree, 'coef': coef * (1 if i == 0 else -1)})
                degree = 0
                coef = 1
            curr_operation = next_operation
    return combine_similar_terms(all_terms)


def solve_negative_discriminant(polynom_map):
    a = polynom_map[2]
    b = polynom_map.get(1, 0)
    D = calc_discriminant(polynom_map)
    real = -b/(2 * a)
    imag_sqrtD = sqrt(-D)
    return [complex(real, -imag_sqrtD/(2*a)), complex(real, +imag_sqrtD/(2*a))]


def solve_second_degree_polynom(D, polynom_map):
    a = polynom_map[2]
    b = polynom_map.get(1, 0)
    if D < 0:
        print('Discriminant negative')
        return solve_negative_discriminant(polynom_map)
    elif D == 0:
        print('Discriminant is zero')
        res = [- b / (2 * a)]
    else:
        print('Discriminant is strictly positive')
        sqrtD = sqrt(D)
        res = [(-b - sqrtD) / (2 * a), (-b + sqrtD) / (2 * a)]
    solutions = []
    for sol in res:
        if float(sol).is_integer():
            sol = int(sol)
        solutions.append(sol)
    return solutions


def transform_polynom_to_unicode(polynom_line: str):
    polynom_line = re.sub(r'(X)\^\(?(-?\d+)\)?', r'\1\2', polynom_line)
    while re.search(r'X\^?(-?\d+)', polynom_line):
        regex = re.search(r'X\^?(-?\d+)', polynom_line)
        search = regex.group(1)
        for old, new in MAPPING_SUPERSCRIPTS.items():
            search = search.replace(old, new)
            polynom_line = polynom_line[:regex.start(1)] + search + polynom_line[regex.end(1):]
    return polynom_line


def get_reduced_form(polynom_map: dict, var_symbol='X', use_common_fractions=False, use_superscripts=False):
    polynom_line = ''
    polynom_map = dict(sorted(polynom_map.items(), key=lambda x: x[0], reverse=True))
    for degree, coef in polynom_map.items():
        if float(coef).is_integer():
            coef = int(coef)
        line_coef = str(abs(coef))
        if use_common_fractions:
            line_coef = decimal2common_fraction(abs(coef))
        if coef < 0:
            line_coef = f'- {line_coef}'
        elif coef > 0:
            line_coef = f'+ {line_coef}'
        polynom_line += f' {line_coef}'
        if degree > 0:
            polynom_line += f'*{var_symbol}^{degree}'
        elif degree < 0:
            polynom_line += f'*{var_symbol}^{degree}'
    polynom_line = polynom_line.strip(' +') + ' = 0'
    polynom_line = re.sub(r'^- ', r'-', polynom_line)
    polynom_line = re.sub(r'(-?)1\*', r'\1', polynom_line)
    if use_superscripts:
        polynom_line = transform_polynom_to_unicode(polynom_line)
    return polynom_line


# line = "-5 + 4 * X + 2*X*2= X^2 +  12 + X^0 + 12*X^(+2)"
# line = "X^2=5*5*5-1X"
# line = "5 * X^0 = 5 * X^0"
# line = "5 * X^03 = 5 * X^02"
# line = "5 * X^4 = 5 * X^4"
# line = "5 + 4 * X + X^2= X^2"
# line = "5 * X^0 + 4 * X^1 = 4 * X^0"
# line = '+X^2-12X=0'
# line = "-5 * X^(-3) + 4 * X^1 - 1 * X^2 = 1 * X^1"
# line = '5x^2+4x+4=0'


def prepare_polynom(polynom):
    for num, superscript in MAPPING_SUPERSCRIPTS.items():
        polynom = polynom.replace(superscript, f'^{num}')
    polynom = polynom.replace('**', '^')
    var_symbol = get_alphabet_symbols(polynom)
    if var_symbol:
        polynom = polynom.replace(var_symbol[0], 'X')

    polynom = re.sub(r'[\t ]', '', polynom).replace('-X', '-1*X').replace('+X', '+1*X').strip('\'"` ')
    polynom = re.sub(fr'(^){num_regex.pattern}X', r'\2\3*X', polynom)
    return polynom, var_symbol


def get_invalid_degree(polynom_map):
    if max(polynom_map) > 2:
        return max(polynom_map)
    return min(polynom_map)


def main(dirty_polynom_line, use_common_fractions=False, is_print_debug_info=False, use_superscripts=False):
    polynom_line, var_symbol = prepare_polynom(dirty_polynom_line)
    if not is_valid_polynomial(polynom_line):
        print('Invalid polynom')
        return
    polynom_data = parse_polynom(polynom_line, is_print_debug_info)
    print(f'Reduced form: {get_reduced_form(polynom_data, var_symbol, use_common_fractions, use_superscripts)}')
    if not is_valid_degrees(polynom_data):
        print(f'Invalid polynomial degree: {get_invalid_degree(polynom_data)}')
        return
    major_degree = look_major_degree(polynom_data)
    print(f'Polynomial degree: {major_degree}')
    if major_degree == 0:
        coef = polynom_data.get(major_degree)
        if not coef:
            solutions = '\u211d'
        else:
            solutions = '\u2205'
    elif major_degree == 1:
        if not polynom_data.get(0):
            solutions = f'{var_symbol} = {0}'
        elif not polynom_data[1]:
            solutions = '\u2205'
        else:
            sol = - polynom_data[0] / polynom_data[1]
            sol = int(sol) if float(sol).is_integer() else sol
            if use_common_fractions:
                sol = decimal2common_fraction(sol)
            solutions = f'{var_symbol} = {sol}'
    else:
        D = calc_discriminant(polynom_data)
        solutions = solve_second_degree_polynom(D, polynom_data)
        if use_common_fractions and D > 0:
            solutions = list(map(lambda x: decimal2common_fraction(x), solutions))
        if not solutions:
            solutions = '\u2205'
        elif len(solutions) == 1:
            solutions = f'{var_symbol} = {solutions[0]}'
        else:
            if D < 0:
                solutions = list(map(
                    lambda x:
                    f'{decimal2common_fraction(x.real) if use_common_fractions else x.real}'
                    f'{"+" if x.imag > 0 else ""}'
                    f'{decimal2common_fraction(x.imag) if use_common_fractions else x.imag}i',
                    solutions))
            solutions = f'{var_symbol}\u2080 = {solutions[0]}\n{var_symbol}\u2081 = {solutions[1]}'

    print(f'The solution is:\n{solutions}')
    return


names = []


def completer(text, state):
    options = [x for x in names if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


if __name__ == '__main__':

    use_common_frac = False
    history_mode = False
    debug_mode = False
    use_superscripts = False
    argv = argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print('usage: computor\n\tLINE\n\t[-h] (help)\n\t[-c] (print common fractions)\n\t[-d] (print debug info)\n\t'
              '[-i] (use interactive mode)')
        exit()
    if '-c' in argv:
        use_common_frac = True

    if '-s' in argv:
        use_superscripts = True

    if '-i' in argv:
        history_mode = True

    if '-d' in argv:
        debug_mode = True

    line = argv[0]
    if not history_mode:
        main(line, use_common_fractions=use_common_frac, is_print_debug_info=debug_mode,
             use_superscripts=use_superscripts)
        exit()
    while True:
        readline.set_completer(completer)
        readline.set_completer_delims('')

        readline.parse_and_bind("tab: complete")

        if line and line != '-i':
            main(line, use_common_fractions=use_common_frac, is_print_debug_info=debug_mode,
                 use_superscripts=use_superscripts)
        try:
            line = input('\nEnter polynomial\n')
        except (KeyboardInterrupt, EOFError):
            break
        if not line or line == 'q':
            break
        if line not in names:
            names.append(line)
