from config import polynomial_regex, term_regex, term_border, MAPPING_SUPERSCRIPTS
import re
import string


def is_valid_equation(polynomial: str):
    # Различный вывод в зависимости от типа ошибки
    if polynomial.count('=') != 1:
        print('Это не уравнение')
        return False
    equation_alphabet_symbols = get_alphabet_symbols(polynomial)
    if len(equation_alphabet_symbols) > 1:
        print('The equation should only have at most one one-letter unknown')
        return False
    invalid_symbols = set(polynomial) - set(re.findall(rf'[{string.digits}.=*/+\-^\s"\'`{equation_alphabet_symbols}()]',
                                                       polynomial))
    if invalid_symbols:
        invalid_symbols = ''.join(invalid_symbols)
        print(f'Invalid characters are encountered: `{invalid_symbols}`')
        return False
    return True


def get_alphabet_symbols(polynomial):
    symbols = ''.join(set(re.findall(r'[a-zA-Zа-яА-Я_]', polynomial)))
    return symbols


def prepare_polynomial(line):
    # Любая буква при вводе уравнения
    var_symbol = get_alphabet_symbols(line)
    prepare_line = line
    if var_symbol:
        prepare_line = line.replace(var_symbol, 'X')
    prepare_line = re.sub(r'(\d)(X)', r'\1*\2', prepare_line).replace(' ', '')
    prepare_line = re.sub(r'(X)[*]{2}(\d|\()', r'\1^\2', prepare_line)

    prepare_line = re.sub(r'\s+', '', prepare_line).strip('\'"`')
    prepare_line = re.sub(r'[1]?X', '1*X', prepare_line)
    return prepare_line, var_symbol


def is_valid_polynomial(prepare_line: str):
    # Вывод того слагемого, который не удалось распарсить
    prepare_line = re.sub(r'(\d+)(X)', r'\1*\2', prepare_line).replace(' ', '')
    is_valid = False if not polynomial_regex.fullmatch(prepare_line) else True
    if not is_valid:
        log_line = 'Failed to parse the equation! Invalid terms:\n\t\t'
        start = 0
        for term in term_regex.finditer(prepare_line):
            if term.start() != start:
                invalid_line = prepare_line[start:term_regex.search(prepare_line[start:]).end()+start]
                invalid_line = invalid_line[:-1] if term_border.search(invalid_line[-1]) else invalid_line
                log_line += f"'{invalid_line}' | "
            start = term.end()
        print(log_line[:-2] if log_line.endswith(' | ') else log_line)
    return is_valid


def decimal2common_fraction(number):
    # Десятичные дроби
    if float(number).is_integer():
        return f'{int(number)}/1'
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


def transform_polynom_to_unicode(polynom_line: str, var_symbol='X'):
    polynom_line = re.sub(fr'({var_symbol})\^\(?(-?\d+)\)?', r'\1\2', polynom_line)
    while re.search(fr'{var_symbol}\^?(-?\d+)', polynom_line):
        regex = re.search(fr'{var_symbol}\^?(-?\d+)', polynom_line)
        search = regex.group(1)
        for old, new in MAPPING_SUPERSCRIPTS.items():
            search = search.replace(old, new)
            polynom_line = polynom_line[:regex.start(1)] + search + polynom_line[regex.end(1):]
    return polynom_line


def get_reduced_form(polynomial_struct: dict, var_symbol='X', use_common_fractions=False, use_superscripts=False):
    polynomial_reduce_line = ''
    polynomial_struct = dict(sorted(polynomial_struct.items(), key=lambda x: x[0], reverse=True))
    for degree, coef in polynomial_struct.items():
        if float(coef).is_integer():
            coef = int(coef)
        line_coef = str(abs(coef))
        if use_common_fractions:
            line_coef = decimal2common_fraction(abs(coef))
        if coef < 0:
            line_coef = f'- {line_coef}'
        elif coef > 0:
            line_coef = f'+ {line_coef}'
        polynomial_reduce_line += f' {line_coef}'
        if degree > 0:
            polynomial_reduce_line += f'*{var_symbol}^{degree}'
        elif degree < 0:
            polynomial_reduce_line += f'*{var_symbol}^({degree})'
    polynomial_reduce_line = polynomial_reduce_line.strip(' +') + ' = 0'
    polynomial_reduce_line = re.sub(r'^- ', r'-', polynomial_reduce_line)
    polynomial_reduce_line = re.sub(fr'([^/\d.]|^)([\-]?)1[*]{var_symbol}', fr'\1\2{var_symbol}', polynomial_reduce_line)
    polynomial_reduce_line = re.sub(fr'{var_symbol}[\^]1(?=[^\d])', var_symbol, polynomial_reduce_line)
    if use_superscripts:
        polynomial_reduce_line = transform_polynom_to_unicode(polynomial_reduce_line, var_symbol)
    return polynomial_reduce_line


def parse_args(argv):
    use_common_fractions = False
    history_mode = False
    debug_mode = False
    use_superscripts = False
    argv = argv[1:]
    if '-h' in argv or '--help' in argv:
        print('''
usage: computor.py [-h] [-c] [-d] [-i] [-s] [equation]

positional arguments:
  equation              The equation to be solved. If this argument is not present,
                        it will ask you to write via standard input

optional arguments:
  -h, --help            show this help message and exit
  -c, --common          display the result in ordinary fractions
  -d, --debug           debug mode
  -i, --interactive     interactive mode (only unix or Docker) - save history input (⇥ ↑ ↓)
  -s, --superscripts    display math symbols
        ''')
        exit()

    if '-c' in argv:
        use_common_fractions = True

    if '-s' in argv:
        use_superscripts = True

    if '-i' in argv:
        history_mode = True

    if '-d' in argv:
        debug_mode = True
    argv = [arg for arg in argv if not re.fullmatch(r'-\w', arg)]
    if not argv:
        try:
            argv = [input('\nEnter polynomial\n')]
        except KeyboardInterrupt:
            exit()
    polynomial_line = argv[0]
    return {'use_common_fractions': use_common_fractions, 'history_mode': history_mode, 'debug_mode': debug_mode,
            'use_superscripts': use_superscripts, 'polynomial_line': polynomial_line}
