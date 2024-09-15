#!/usr/bin/env python3

import threading

class Timer:
    def __init__(self, frequency=20, callback=lambda: ...):
        """
        Initializes the custom timer.
        :param frequency: The time frequency between each callback execution in seconds.
        :param callback: The callback function to be executed.
        """
        self.frequency = frequency
        self.callback = callback
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run)

    def start(self):
        """
        Starts the timer.
        """
        self.thread.start()

    def _run(self):
        """
        The running loop that executes the callback periodically.
        """
        period = 1/self.frequency
        while not self.stop_event.wait(period):
            self.callback()

    def stop(self):
        """
        Stops the timer.
        """
        self.stop_event.set()
        self.thread.join()

if __name__ == "__main__":
    freq  = 10 
    timer = Timer(freq, lambda: print ("callback"))
    timer.start()