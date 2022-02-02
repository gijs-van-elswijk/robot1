import time

class Stopwatch:
    def __init__(self):
        self.tstart = time.time()

    def elapsed(self) -> float:
        return (time.time() - self.tstart)

    def reset(self):
        self.tstart = time.time()

