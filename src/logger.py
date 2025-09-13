import time


LEVELS = ["INFO", "WARN", "ERROR"]


class Logger:
    def __init__(self, file=None, prefix=""):
        self.__prefix = prefix
        self.__file = file
        if file:
            self.file = open(file, "w")
        else:
            self.file = open("log.txt", "w")

    def log(self, statement, level=0):
        self.file.write(
            f"[{time.strftime('%G-%m-%dT%H:%M:%SZ',time.gmtime())}]:[{LEVELS[level]}]: {self.__prefix} {statement}\n")

    def append(self, prefix):
        return Logger(file=self.__file, prefix=f"{self.__prefix}:{prefix}")

    def __del__(self):
        self.file.close()
