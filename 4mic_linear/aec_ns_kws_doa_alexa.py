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
from doa_respeaker_4mic_linear_array import DOA
from gpiozero import LED
from avs.alexa import Alexa

led = LED(5)
led.off()


def main():
    src = Source(rate=16000, frames_size=320, channels=8)
    ec = EC(channels=src.channels, capture=0, playback=7)
    ns = NS(rate=src.rate, channels=1)
    kws = KWS()
    doa = DOA(rate=16000, chunks=20)
    alexa = Alexa()

    alexa.state_listener.on_listening = led.on
    alexa.state_listener.on_finished = led.off

    src.pipeline(ec, ns, kws, alexa)

    src.link(doa)

    def on_detected(keyword):
        direction = doa.get_direction()
        print('detected {} at direction {}'.format(keyword, direction))
        led.on()
        alexa.listen()

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
    led.off()

    # wait a second to allow other threads to exit
    time.sleep(1)

if __name__ == '__main__':
    main()
