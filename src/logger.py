import time


LEVELS = ["INFO", "WARN", "ERROR"]


class Logger:
    def __init__(self, file=None):
        if file:
            self.file = open(file, "w")
        else:
            self.file = open("log.txt", "w")

    def log(self, statement, level=0):
        self.file.write(f"[{time.strftime('%G-%m-%dT%H:%M:%SZ',time.gmtime())}]:[{LEVELS[level]}]: {statement}\n")
