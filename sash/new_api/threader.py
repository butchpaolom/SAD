import threading


def do_thread(fnc,arg):
    if not arg:
        thread = threading.Thread(target=fnc, args=(arg,))
    else:
        thread = threading.Thread(target=fnc)
    thread.start()