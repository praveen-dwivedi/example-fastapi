def double(x):
    """
    This is where we put optional doc string that eplains what the funs does
    For example, this function multiplies its input by 2
    """
    return x * 2


def apply_to_one(f):
    """Calls function f with argument 1"""
    return f(1)


my_double = double
print(apply_to_one(my_double))
# print(double(5))

def my_print(message = "my default message"):
    print(message)

my_print("Hello")

my_print()


def full_name(first = "What's his-name", last = "Someone"):
    return first + " " + last

print(full_name("Joel", "Grus"))
print(full_name("Joel"))
print(full_name(last ="Grus"))