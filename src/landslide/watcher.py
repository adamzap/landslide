import sys
import time

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, DirModifiedEvent
except ImportError:
    print 'Error: The watchdog module must be installed to use the -w option'
    print 'Exiting...'
    sys.exit(1)


def watch(watch_dir, generate_func):
    event_handler = LandslideEventHandler(generate_func)
    observer = Observer()

    observer.schedule(event_handler, path=watch_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


class LandslideEventHandler(FileSystemEventHandler):
    def __init__(self, generate_func):
        super(LandslideEventHandler, self).__init__()

        self.generate_func = generate_func

    def on_modified(self, event):
        if isinstance(event, DirModifiedEvent):
            self.generate_func()
