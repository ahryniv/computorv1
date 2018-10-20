import  sys
from    InputSyntaxException    import InputSyntaxException
from    decimal                 import Decimal

def main(line):
    try:
        line = line.replace(" ", "")
        polynomials = get_polynomials(line)
        print(polynomials)
        if not polynomials:
            print_all_are_solutions()
            return
        print_reduced_form(polynomials)
        polynomial_degree = max(polynomials)
        print_polynomial_degree(polynomial_degree)
        if len(polynomials) == 1 and polynomial_degree == 0 and next(iter(polynomials.values())) != 0:
            print_no_solutions()
            return
        if polynomial_degree == 2:
            solutions = calculate_quadratic(polynomials)
            print_solutions(solutions)
        elif polynomial_degree == 1:
            solution = calculate_simple(polynomials)
            print_solution(solution)
    except InputSyntaxException as err:
        print(err)
    except Exception:
        print("Invalid input")

def get_polynomials(line):
    polynomials = dict();

    two_parts = line.split("=")
    left = two_parts[0]
    right = two_parts[1]
    group_polynomials(left, polynomials, False)
    group_polynomials(right, polynomials, True)
    return polynomials

def group_polynomials(line, polynomials, reverse_sign_flag):
    while True:
        plus_pos = line.rfind("+")
        minus_pos = line.rfind("-")
        if plus_pos == minus_pos == -1:
            get_new_polynomial(polynomials, "+", line, reverse_sign_flag)
            break    
        elif plus_pos > minus_pos:
            tmp = line.rpartition("+")
            line = tmp[0]
        else:
            tmp = line.rpartition("-")
            line = tmp[0]
        get_new_polynomial(polynomials, tmp[1], tmp[2], reverse_sign_flag)
    
def get_new_polynomial(polynomials, sign, polynomial, reverse_sign_flag):
    polynomial = polynomial.lower()
    tmp2 = polynomial.split("*")
    try:
        quantity = Decimal(tmp2[0])
        power = Decimal(tmp2[1].replace("x^", ""))
        if power > 2:
            raise InputSyntaxException("The polynomial degree is stricly greater than 2, I can't solve.")
    except IndexError:
        raise InputSyntaxException('Invalid syntax. All terms should be of the form "a * X^p", "{0}" given.'.format(polynomial))
    except ValueError:
        raise InputSyntaxException('Invalid syntax. All terms should be of the form "a * X^p", "{0}" given.'.format(polynomial))
    if (reverse_sign_flag):
        sign = reverse_sign(sign)
    if not power in polynomials:
        polynomials[power] = Decimal(0)
    if sign == "+":
        polynomials[power] += quantity
    elif sign == "-":
        polynomials[power] -= quantity
    if polynomials[power] == 0:
        del polynomials[power]

def calculate_quadratic(polynomials):
    a = Decimal(0)
    b = Decimal(0)
    c = Decimal(0)

    if 2 in polynomials:
        a = Decimal(polynomials[2])
    if 1 in polynomials:
        b = Decimal(polynomials[1])
    if 0 in polynomials:
        c = Decimal(polynomials[0])
    discriminant = ( b ** Decimal(2) ) - ( Decimal(4) * a * c )
    print_discriminant( discriminant )
    if (discriminant > 0):
        b = b * Decimal(-1)
        x1 = ( b + discriminant ** Decimal(0.5) ) / ( Decimal(2) * a )
        x2 = ( b - discriminant ** Decimal(0.5) ) / ( Decimal(2) * a )
        x1 = x1 if x1 else Decimal(0)
        x2 = x2 if x2 else Decimal(0)
        return (x1, x2)
    elif (discriminant == 0):
        x = (b * (-1) / (2 * a))
        x = x if x else Decimal(0)
        return x,
    else:
        b_2a = Decimal((b * (-1)) / (2 * a))
        discriminant_minus = discriminant * Decimal(-1)
        imagine_part = Decimal((discriminant_minus ** Decimal(0.5))/(2*a))
        imagine_part = str(imagine_part) + "i"
        x1 = str(b_2a) + " + " if b_2a != 0 else ""
        x1 = x1 + imagine_part
        x2 = str(b_2a) + " - " if b_2a != 0 else ""
        x2 = x2 + imagine_part
        return (x1, x2)
        
def calculate_simple(polynomials):
    b = 0
    c = 0

    if 1 in polynomials:
        b = polynomials[1]
    if 0 in polynomials:
        c = polynomials[0]
    return (c * (-1)) / b

def reverse_sign(sign):
    if sign == "-":
        return "+"
    return "-"

def print_reduced_form(polynomials):
    reduced_form = ""
    if 2 in polynomials:
        reduced_form += "{0:+} * X^2 ".format(polynomials[2])
    if 1 in polynomials:
        reduced_form += "{0:+} * X ".format(polynomials[1])
    if 0 in polynomials:
        reduced_form += "{0:+} ".format(polynomials[0])
    if reduced_form and reduced_form[0] == "+":
        reduced_form = reduced_form[1:]
    print("Reduced form: {0}= 0".format(reduced_form))

def print_polynomial_degree(polynomial_degree):
    print("Polynomial degree: {0}".format(polynomial_degree))

def print_discriminant(discriminant):
    if discriminant > 0:
        print("Discriminant is strictly positive ({0}), the two solutions are:".format(discriminant))
    elif discriminant == 0:
        print("Discriminant is zero, the solution is:")
    else:
        print("Discriminant is negative({0}), two imaginary numbers are solutions".format(discriminant))

def print_solutions(solutions):
    for i in range(len(solutions)):
        print(solutions[i])

def print_solution(solution):
    print("The solution is:")
    print(solution)

def print_all_are_solutions():
    print("All real numbers are solutions")


def print_no_solutions():
    print("No solutions")

if __name__ == "__main__":
    try:
        line = sys.argv[1]
    except IndexError:
        print("Usage: main.py <arg1>")
        sys.exit(1)
    main(line)