# Church numeral for zero: lambda f, x: x
def zero(f):
    return lambda x: x


# Church numeral for add_one: lambda n: lambda f, x: f(n(f)(x))，其中 n(f)(x) 意为 n(f) 会返回一个函数，然后将返回的函数应用到x
def add_one(n):
    return lambda f: lambda x: f(n(f)(x))


# Define the successor function
succ = lambda n: n + 1
# succ_str = lambda n: str(n) * 2


def succ_str(n):
    return str(n) * 2


# Convert Church numeral to Python integer
def church_to_int(n):
    return n(succ)(0)


def church_to_str(n):
    return n(succ_str)('-')


# Convert Python integer to Church numeral
def int_to_church(i):
    if i == 0:
        return zero
    else:
        return add_one(int_to_church(i - 1))


# Test zero and add_one
if __name__ == '__main__':
    print("Church representation of zero:", church_to_int(zero))  # Output: 0
    print("Church representation of one:", church_to_int(add_one(zero)))  # Output: 1
    print("Church representation of two:", church_to_int(add_one(add_one(zero))))  # Output: 2

    # Convert Python integer to Church numeral and back to integer
    num = 5
    church_num = int_to_church(num)
    print("Church representation of", num, ":", church_to_int(church_num))  # Output: 5

    print("Church representation of zero:", church_to_str(zero))  # Output: 0
    print("Church representation of one:", church_to_str(add_one(zero)))  # Output: 1
    print("Church representation of two:", church_to_str(add_one(add_one(zero))))  # Output: 2
