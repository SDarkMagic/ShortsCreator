# Multipurpose general utility functions

def timestring_to_ms(time: str):
    split_time = time.split(':')
    split_ms = split_time[-1].split('.')
    ms = split_ms[-1] if len(split_ms) > 1 else 0
    if len(split_time) == 1:
        return (int(split_ms[0]) * 1000) + int(ms)
    elif len(split_time) == 2:
        minutes = int(split_time[0])
        split_time[1] = str(float(minutes * 60) + float(split_time[1]))
        return timestring_to_ms(split_time[1])
    elif len(split_time) == 3:
        hours = int(split_time[0])
        split_time[1] = str(int(hours * 60) + int(split_time[1]))
        split_time.pop(0)
        return timestring_to_ms(':'.join(split_time))

def ms_to_timestring(ms: int):
    split_time = ['0', '0', '0']
    split_ms = [0, 0]
    split_ms[1] = int(ms % 1000)
    split_ms[0] = int(ms // 1000)
    split_time[2] = str(split_ms[0])
    if int(split_time[2]) > 60:
        split_time[1] = split_time[2] // 60
        split_time[2] = str(split_time[2] % 60)
    if int(split_time[1]) > 60:
        split_time[0] = str(split_time[1] // 60)
        split_time[1] = str(split_time[1] % 60)
    for i in split_time:
        if len(i) < 2:
            split_time[split_time.index(i)] = f'0{split_time[split_time.index(i)]}'
    return f'{":".join(split_time)}.{split_ms[1]}'
