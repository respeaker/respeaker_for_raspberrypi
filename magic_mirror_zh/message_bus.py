# -*- coding: utf-8 -*-

import time
import threading
import requests
import sys
if sys.version_info < (3, 0):
    import Queue as queue
else:
    import queue


class MessageBus(object):
    def __init__(self):
        self.session = requests.Session()

        self.queue = queue.Queue()

        self.is_quit = False

        self.url = 'http://localhost:8080/kalliope'


    def put(self, payload, notification='KALLIOPE'):
        self.queue.put((payload, notification))

    def start(self):
        self.is_quit = False
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.is_quit = True
        self.queue.put(('', ''))

    def _run(self):
        while not self.is_quit:
            payload, notification = self.queue.get()
            while self.queue.qsize():
                payload, notification = self.queue.get()

            data = {
                "notification": notification,
                "payload": payload
            }
            self.session.post(self.url, data=data)



if __name__ == '__main__':
    bus = MessageBus()
    
    bus.start()
    bus.put('hello world')
    time.sleep(3)
    bus.put('你好帅！')
    time.sleep(3)
    bus.stop()
