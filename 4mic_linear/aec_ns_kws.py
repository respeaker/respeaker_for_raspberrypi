"""
Record audio from a 6 microphone array, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

The hardware is respeaker 6 mic array for raspberry pi.
"""

import signal
import time
from voice_engine.source import Source
from voice_engine.ec import EC
from voice_engine.ns import NS
from voice_engine.kws import KWS
from gpiozero import LED

led = LED(5)
led.off()


def main():
    src = Source(rate=16000, frames_size=320, channels=8)
    ec = EC(channels=src.channels, capture=0, playback=7)
    ns = NS(rate=src.rate, channels=1)
    kws = KWS()

    # data flow between elements
    # ---------------------------
    # src -> ec -> ns -> kws
    src.pipeline(ec, ns, kws)

    def on_detected(keyword):
        led.toggle()
        print('detected {}'.format(keyword))

    kws.on_detected = on_detected

    is_quit = []
    def signal_handler(sig, frame):
        is_quit.append(True)
        print('quit')
    signal.signal(signal.SIGINT, signal_handler)

    src.pipeline_start()
    while not is_quit:
        time.sleep(1)

    src.pipeline_stop()

    # wait a second to allow other threads to exit
    time.sleep(1)
    led.off()


if __name__ == '__main__':
    main()
