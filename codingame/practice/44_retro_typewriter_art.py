'''

https://www.codingame.com/ide/puzzle/retro-typewriter-art

'''

import re
import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


def get_count(matches) -> int:
    if matches.group(1):
        count = int(matches.group(1))
    else:
        count = 1

    return count


chunks = input().split()

conversions = {
    r'^(\d+)sp$': ' ',
    r'^(\d+)bS$': '\\',
    r'^(\d+)sQ$': '\'',
    r'^()nl$': '\n',
}

general = r'^(\d+)(.)$'

res = ''
for chunk in chunks:

    for pattern, char in conversions.items():
        matches = re.match(pattern, chunk)
        if matches:
            res += char * get_count(matches)
    
    matches = re.match(general, chunk)
    if matches:
        res += matches.group(2) * get_count(matches)

print(res)
