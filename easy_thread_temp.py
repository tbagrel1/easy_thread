#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple way to create basic decorrelated threads with Python 3."""

from threading import Thread

DEBUG_LEVEL = 2

class TaskState(object):
    """Represents task states."""

    def __init__(self, state_value):
        """Init method."""
        self.state_value = state_value

def NO_PARENT_LINK(value):
    """Do nothing."""
    pass

NOT_STARTED = TaskState(0)
RUNNING = TaskState(1)
FAILED = TaskState(2)
DAEMON = False

class EasyThread(Thread):
    """Easy thread instance."""

    def __init__(
        self, name, func, args, kwargs, debug_level=DEBUG_LEVEL,
        parent_link=NO_PARENT_LINK):
        """Init method."""
        super().__init__()
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.debug_level = debug_level
        self.parent_link = parent_link
        self.parent_link(NOT_STARTED)
    
    def run(self):
        """Main method of the thread."""
        self.log(2, "    --> Starting thread")
        self.parent_link(RUNNING)
        try:
            self.parent_link(self.func(*self.args, **self.kwargs))
        except Exception as e:
            self.log(0, "Error during runtime: <{}>".format(e))
            self.parent_link(FAILED)
        self.log(2, "    --> Exiting thread")

    def log(self, level, msg):
        """Prints msg iif level <= self.debug_level."""
        if level <= self.debug_level:
            print("[Thread {}] {}".format(self.name, msg))

class ThreadPool(object):
    """Thread pool instance."""

    def __init__(self, daemon=DAEMON, debug_level=DEBUG_LEVEL):
        """Init method."""
        self.daemon = daemon
        self.count = 0
        self.results = {}
        self.debug_level = debug_level

    def build_link(self, id):
        """Creates link function."""
        def link(value):
            self.results[id] = value
        return link

    def add(self, func, *args, **kwargs):
        """Creates and executes a new thread with the specified function."""
        id = self.count
        self.count += 1
        new_thread = EasyThread(
            str(id), func, args, kwargs,
            debug_level=self.debug_level,
            parent_link=self.build_link(id)
        )
        new_thread.daemon = self.daemon
        new_thread.start()
        return id

    def addc(self, func, *args, **kwargs):
        self.add(func, *args, **kwargs)
        return self

    def get_result(self, id):
        """Returns the result of the specified thread."""
        return self.results[id]

def main():
    """Launcher."""
    from urllib.request import urlopen
    import time
    def get_page():
        return urlopen("https://www.google.com").read()
    pool = ThreadPool()
    id = pool.add(get_page)
    c = 0
    while pool.get_result(id) == RUNNING:
        c += 1
        print("waiting for the page to load...[{}]".format(c))
        time.sleep(0.01)
    print(pool.get_result(id))

if __name__ == "__main__":
    main()
