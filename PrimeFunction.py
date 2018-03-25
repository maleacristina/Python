def is_prime(x):
    if x < 2:
        return False
    else:
        for n in range(2, x - 1):
            if x % n == 0:
                return False
        return True


print is_prime(0)
print is_prime(2)
print is_prime(5)
print is_prime(9)
print is_prime(19)
print is_prime(91)
