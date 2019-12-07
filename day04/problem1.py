def has_repeated_digit(n):
    s = str(n)
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            return True
    return False


def strictly_increasing(n):
    s = str(n)
    for i in range(len(s) - 1):
        if int(s[i]) > int(s[i + 1]):
            return False
    return True


def valid_passwords(lower, upper):
    return len(
        list(
            i
            for i in range(lower, upper + 1)
            if has_repeated_digit(i) and strictly_increasing(i)
        )
    )


print(valid_passwords(236491, 713787))
