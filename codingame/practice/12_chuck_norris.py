'''

https://www.codingame.com/training/easy/chuck-norris

'''


def convert_to_bytes(message: str) -> str:
    res = []
    for ch in message:
        converted = bin(int.from_bytes(ch.encode(), 'big'))[2:].zfill(7)
        res.append(converted)

    return ''.join(res)

binary = convert_to_bytes(input())

out = []
dig_count = 1
for i, dig_cur in enumerate(binary):

    flag = '0' if dig_cur == '1' else '00'
    
    try:
        dig_nxt = binary[i+1]
    except:
        dig_nxt = ''

    if dig_nxt:
        if dig_cur == dig_nxt:
            dig_count += 1
        else:
            out.append(flag + ' ' + '0'* dig_count)
            dig_count = 1
    else:
        out.append(flag + ' ' + '0'* dig_count)
        dig_count = 1 

print(' '.join(out))
