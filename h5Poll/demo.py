import random


def random_build_mac_addr(format=2):
    if format not in [2, 4]:
        return 'mac address format error'
    x = []
    if format == 2:
        n = 6
        symbol = ':'
    else:
        n = 4
        symbol = '-'

    for i in range(0, n):
        s = ''.join(random.sample('abcdef0123456789', format))
        x.append(s)
    return symbol.join(x).upper()


def build_mac_addr_from_sn(sn, format=2):
    if format not in (2, 4) or len(sn) < 32:
        return 'error'

    if format == 2:
        l = 2
        symbol = ':'
    else:
        l = 4
        symbol = '-'
    mac_str = sn[-16:]

    n=0
    d=[]
    while n<len(mac_str):
        d.append(mac_str[n:n+l])
        n = n+l

    return symbol.join(d).upper()

print(build_mac_addr_from_sn('sdfaasfklasklfasdfskljadfskljasfkljkjkldaskljfdaswklj',4))
print(random_build_mac_addr(2))
print(random_build_mac_addr(4))

