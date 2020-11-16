from config import term_regex, num_regex
import re


def search_terms(prepare_line):
    return [(term[1], term[-1]) for term in term_regex.findall(prepare_line)[:-1]]


def parse_term(term: str):
    coef = re.fullmatch(num_regex, term)
    if coef:
        return {'coef': float(coef.group())}
    degree = num_regex.search(term)
    if not degree:
        return {'degree': 1}
    return {'degree': int(degree.group())}


def combine_similar_terms(terms: list):
    combine_terms = {}
    for term in terms:
        degree = term['degree']
        combine_terms[degree] = combine_terms.get(degree, {})
        combine_terms[degree]['coef'] = combine_terms[degree].get('coef', 0) + term['coef']
    return {degree: coef['coef'] for degree, coef in combine_terms.items() if coef['coef']} or {0: 0.0}


def parse_polynomial(prepare_line, debug_mode=False):
    all_terms = []
    for i, part in enumerate(prepare_line.split('=')):
        curr_operation = ''
        coef = 1
        degree = 0
        for term, next_operation in search_terms(part):
            new_term = parse_term(term)
            if curr_operation == '/':
                num = new_term.get('coef', 1) * (-1 if curr_operation == '-' else 1)
                if num == 0:
                    print('You have no right to divide by zero')
                    exit()
                coef /= num
                degree -= new_term.get('degree', 0)
            else:
                coef *= new_term.get('coef', 1) * (-1 if curr_operation == '-' else 1)
                degree += new_term.get('degree', 0)
            if debug_mode:
                print(f'term={term}\tnext_operation={next_operation}', '-->', f'coef={coef},degree={degree}')
            if not next_operation or next_operation == '+' or next_operation == '-':
                all_terms.append({'degree': degree, 'coef': coef * (1 if i == 0 else -1)})
                degree = 0
                coef = 1
            curr_operation = next_operation
    return combine_similar_terms(all_terms)


def look_major_degree(polynomial_struct):
    return max(polynomial_struct)


def is_valid_degrees(polynomial_struct):
    return not set(polynomial_struct) - {0, 1, 2}


def get_invalid_degree(polynomial_struct):
    if max(polynomial_struct) > 2:
        return max(polynomial_struct)
    return min(polynomial_struct)
