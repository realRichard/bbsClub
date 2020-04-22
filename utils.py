import time


def log(*args, **kwargs):
    t = time.strftime("%H:%M:%S", time.localtime())
    with open('log.txt', 'a', encoding='utf-8') as f:
        # redirect output to file
        print(t, *args, file=f, **kwargs)


def find_all_and_separate(raw_list, **kwargs):
    for k, v in kwargs.items():
        key = k
        value = v
    new_list = []
    for i, s in enumerate(raw_list):
        if s.__dict__[key] == value:
            new_list.append(raw_list.pop(i))
    return new_list
