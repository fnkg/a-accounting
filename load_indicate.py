import threading
import itertools
import time

def loading_indicator(stop_event):
    for frame in itertools.cycle(r'\|/-'):
        if stop_event.is_set():
            break
        print('\rRunning ' + frame, end='', flush=True)
        time.sleep(0.1)
    print('\rRunning complete!   ')
