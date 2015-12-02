def permutate(s):
    if len(s) == 2:
        yield s
        yield s[1] + s[0]
    else:
        # Pull out each and permutate the remainder
        for n, c in enumerate(s):
            for p in permutate(s[:n] + s[n + 1:]):
                build = c + p
                yield build
