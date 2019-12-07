def has_twice_repeated_digit(n):
    s = str(n)

    cur_partition = []
    cur = None

    for c in s:
        if cur != c:
            if len(cur_partition) == 2:
                return True
            cur = c
            cur_partition = []
        cur_partition.append(c)

    return len(cur_partition) == 2


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
            if has_twice_repeated_digit(i) and strictly_increasing(i)
        )
    )


print(valid_passwords(236491, 713787))
