#!/usr/bin/env python3
import sys
from ft_math import solve_second_degree_polynom
from parsing import decimal2common_fraction
from preprocessing import look_major_degree, is_valid_degrees, get_invalid_degree
from parsing import is_valid_equation, prepare_polynomial, is_valid_polynomial, get_reduced_form
from preprocessing import parse_polynomial
from parsing import parse_args


def prepare_solutions(solutions, var_symbol='X', use_common_fractions=False):
    if not solutions:
        return '∅'
    if float('inf') in solutions:
        return 'ℝ'
    solutions_line = ''
    for solution in solutions:

        if type(solution) == complex:
            solution = f'{decimal2common_fraction(solution.real) if use_common_fractions else solution.real}' \
                       f'{"+" if solution.imag > 0 else ""}' \
                       f'{decimal2common_fraction(solution.imag) if use_common_fractions else solution.imag}i'
        elif use_common_fractions:
            solution = decimal2common_fraction(solution)
        solutions_line += f'{var_symbol} = {solution}\n'
    return solutions_line.strip()


def solve_equation(polynomial_struct):
    major_degree = look_major_degree(polynomial_struct)
    print(f'Polynomial degree: {major_degree}')

    if major_degree == 0:
        coef = polynomial_struct.get(major_degree)
        if not coef:
            solutions = [float('inf')]
        else:
            solutions = []

    elif major_degree == 1:
        if not polynomial_struct.get(0):
            solutions = [0]
        elif not polynomial_struct[1]:
            solutions = []
        else:
            solution = - polynomial_struct[0] / polynomial_struct[1]
            solution = int(solution) if float(solution).is_integer() else solution
            solutions = [solution]

    else:
        solutions = solve_second_degree_polynom(polynomial_struct)
    return solutions


def main(dirty_polynomial_line, use_common_fractions=False, debug_mode=False, use_superscripts=False):
    if not is_valid_equation(dirty_polynomial_line):
        return
    prepare_polynomial_line, var_symbol = prepare_polynomial(dirty_polynomial_line)

    if not is_valid_polynomial(prepare_polynomial_line):
        return

    polynomial_struct = parse_polynomial(prepare_polynomial_line, debug_mode)
    print(f'Reduced form: {get_reduced_form(polynomial_struct, var_symbol, use_common_fractions, use_superscripts)}')
    if not is_valid_degrees(polynomial_struct):
        print(f'Invalid polynomial degree: {get_invalid_degree(polynomial_struct)}')
        return
    solutions = solve_equation(polynomial_struct)
    solutions_line = prepare_solutions(solutions, var_symbol, use_common_fractions)
    print(f'The solution is:\n{solutions_line}')
    return


names = set()


def completer(text, state):
    options = [x for x in names if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


if __name__ == '__main__':
    arguments = parse_args(sys.argv)
    input_line = arguments.pop('polynomial_line')
    if not arguments.pop('history_mode'):
        main(input_line, **arguments)
        exit()
    while True:
        try:
            import readline
        except (ModuleNotFoundError, ImportError):
            print('Interactive mode is not supported on your system')
            exit()

        readline.set_completer(completer)
        readline.set_completer_delims('')

        readline.parse_and_bind("tab: complete")

        if input_line and input_line != '-i':
            if input_line not in names:
                names.add(input_line)
            main(input_line, **arguments)
        try:
            input_line = input('\nEnter polynomial\n')
        except (KeyboardInterrupt, EOFError):
            break
        if not input_line or input_line in ('q', 'exit', 'quit', 'exit()', 'quit()'):
            break
