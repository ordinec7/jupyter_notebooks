from sys import stdout
import time


class ProgressBar(object):
    def __init__(self, name, min, max):
        self.min = min
        self.max = max
        self.maxLength = 50
        self.value = min
        self.displayLength = 0

        title = '\n[= %s ' % name
        titleLength = len(title)
        if titleLength > self.maxLength - 2:
            self.maxLength = titleLength + 2
        title += '='*(self.maxLength - len(title) + 1) + ']'
        print(title)

        self.addChars(0)

    def setValue(self, value):
        newLength = int((value-self.min) / (self.max-self.min) * self.maxLength)
        if newLength > self.displayLength:
            self.addChars(newLength)

    def addChars(self, newValue):
        if newValue == 0:
            stdout.write('[')
        elif newValue == self.maxLength:
            stdout.write(']\n')
        elif newValue > self.displayLength:
            stdout.write("%s" % '='*(newValue-self.displayLength))
            self.displayLength = newValue
        else:
            return

        stdout.flush()


if __name__ == "__main__":
    start = 342
    end = 5621
    bar = ProgressBar('Runge Kutta 5th adaptive TEST', start, end)
    for i in range(start, end + 1, 15):
        bar.setValue(i)
        time.sleep(0.01)
    bar.setValue(end)
