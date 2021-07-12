from threading import Timer
def hello():
    print("hello world!")
    timer=Timer(1,hello)
    timer.start()

timer=Timer(1, hello)
timer.start()