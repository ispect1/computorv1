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


def calc_discriminant(polynom_map):
    return polynom_map.get(1, 0) * polynom_map.get(1, 0) - 4 * polynom_map.get(0, 0) * polynom_map.get(2, 0)


def solve_negative_discriminant(polynom_map):
    a = polynom_map[2]
    b = polynom_map.get(1, 0)
    D = calc_discriminant(polynom_map)
    real = -b / (2 * a)
    imag_sqrtD = sqrt(-D)
    return [complex(real, -imag_sqrtD / (2 * a)), complex(real, +imag_sqrtD / (2 * a))]


def solve_second_degree_polynom(polynomial_struct):
    D = calc_discriminant(polynomial_struct)
    a = polynomial_struct[2]
    b = polynomial_struct.get(1, 0)
    if D < 0:
        print('Discriminant negative')
        return solve_negative_discriminant(polynomial_struct)
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
