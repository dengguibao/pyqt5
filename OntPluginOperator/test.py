import threading
import time


def test(i):
    print('%s' % i)
    time.sleep(1)


t_list = [threading.Thread(target=test, args=(i,)) for i in range(0, 521)]

while True:
    if len(t_list) > 0 and threading.active_count() <= 100:
        t_list[0].start()
        t_list.pop(0)

    if len(t_list) > 0 and threading.active_count() >= 100:
        time.sleep(1)

    if len(t_list) == 0 and threading.active_count() == 1:
        break
print('-' * 30, 'end', '-' * 30)
