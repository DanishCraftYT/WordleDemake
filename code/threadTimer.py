import threading
import timeit
import time as tm

class ThreadTimer:
    thread = None
    thread_event = None
    def __init__(self, time : float, callback, args : list=[]):
        self.thread_event = threading.Event()
        self.thread = threading.Thread(target=self.__timer, args=[time, callback, args], daemon=True)
        self.thread.start()

    def __timer(self, time, callback, callback_args : list, use_exit_flag=True) -> None: # the exit flag determines if the loop was stopped or successfully finished executing.
        if not callable(callback):
            raise Exception(f"Timer callback is not a function!")
        start_time = timeit.default_timer()
        while True:
            tm.sleep(0.05) # reduces peformance issues caused by the timer.
            if self.thread_event.is_set():
                if use_exit_flag:
                    callback_args.append(-1)
                    if callback_args: # determines if callback_args tuple is empty or not. this is used to determine if the callback has args or not.
                        callback(-1)
                    else:
                        callback(callback_args)
                break
            current_time = timeit.default_timer()
            if current_time - start_time >= time:
                if use_exit_flag:
                    callback_args.append(0)
                if callback_args: # determines if callback_args tuple is empty or not. this is used to determine if the callback has args or not.
                    callback()
                else:
                    callback(callback_args)
                break
            continue
