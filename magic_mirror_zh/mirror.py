# -*- coding: utf-8 -*-

import time
import json

from wenwen.assistant import Assistant
from message_bus import MessageBus
import wenwen.player as player


# TODO: Get a key from https://ai.chumenwenwen.com
KEY = ''


class Mirror(Assistant):
    def __init__(self, key=KEY):
        super(Mirror, self).__init__(key)

        self.set_keywords(['开灯', '关灯', '播放音乐', '几点了', '暂停', '魔镜', '显示天气', '隐藏天气'])
        # self.set_keywords(['魔镜'])

        self.kws = False
        self.message_bus = MessageBus()

    def start(self):
        super(Mirror, self).start()
        self.message_bus.start()

    def stop(self):
        super(Mirror, self).stop()
        self.message_bus.stop()

    def hotword_start(self):
        self._lib.mobvoi_recognizer_start(5)
        self.kws = True

    def hotword_stop(self):
        self._lib.mobvoi_recognizer_stop()

    def on_partial_transcription(self, text):
        if self.kws:
            if text.find('魔镜') >= 0:
                # self.message_bus.put('>'')
                self.kws = False
                self.recognizer_start()
            elif text.find('开灯') >= 0:
                pass
            elif text.find('关灯') >= 0:
                pass
            elif text.find('显示天气') >= 0:
                self.message_bus.put('{"action": "SHOW","module":"module_4_currentweather"}', 'REMOTE_ACTION')
            elif text.find('隐藏天气') >= 0:
                self.message_bus.put('{"action": "HIDE","module":"module_4_currentweather"}', 'REMOTE_ACTION')
        else:
            self.message_bus.put(text)
        print('on_partial_transcription: {}'.format(text))

    def on_final_transcription(self, text):
        self.message_bus.put(text)
        print('on_final_transcription: {}'.format(text))

    def on_result(self, text):
        print('on_result:')
        response = json.loads(text)
        print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False))

        self.hotword_stop()
        if response['status'] == 'success':
            if 'languageOutput' in response:
                text = response['languageOutput']['displayText']
                speech = self.synthesize(text)

                self.message_bus.put(text)
                player.play(data=speech)

        self.hotword_start()


def main():
    from voice_engine.source import Source

    src = Source(rate=16000, channels=1)
    assistant = Mirror()

    src.pipeline(assistant)
    src.pipeline_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()

if __name__ == '__main__':
    main()