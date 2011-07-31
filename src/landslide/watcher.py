import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

    
def watch(source_files, generate_func):
    event_handler = LandslideEventHandler(generate_func)
    observer = Observer()
    for source in source_files:
        #recursive is set to True to avoid a bug in the current version of
        #pathtools a dependency of watchdog. It shouldn't be a big deal 
        #since we are watching individual files
        observer.schedule(event_handler, path=source, recursive=True)
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
        self.generate_func()
