#!/usr/bin/env python3


EXPECTED_ANSWER = 'apple'


def level() -> str:
    print('''\
Here comes your first riddle!
Small, red, round, and sweet!
Bring me one of this simple treat!
''')

    return input('> ').lower()
