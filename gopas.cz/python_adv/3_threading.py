from threading import Thread

class MyThread(Thread):

    def __init__(self, name, id, counter):
        self.id = id
        self.name = name
        self.counter = counter

    def run(selfl):
        print("start ", self.name, self.id, self.counter)



if __name__ == "__main__":
    thread1 = MyThread()
    thread1.start()
    print("main exit")