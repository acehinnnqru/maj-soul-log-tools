from collections import defaultdict


def longest_fail_user(user_result):
    m = defaultdict(list)
    for u, result in user_result.items():
        m[__longest_fail(result)].append(u)

    longest = max(m.keys())
    return longest, m[longest], m


def __longest_fail(result: list) -> int:
    longest = 0
    current = 0
    for r in result:
        if r == 0:
            current += 1
        else:
            longest = max(longest, current)
            current = 0
    return longest
