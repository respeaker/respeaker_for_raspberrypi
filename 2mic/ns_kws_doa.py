"""
Record audio from respeaker 2 mic hat for raspberry pi, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.
"""

import signal
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.ns import NS
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_2mic_hat import DOA
from pixels import pixels


def main():
    src = Source(rate=16000, frames_size=160, channels=2)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    ns = NS(rate=src.rate, channels=1)
    kws = KWS()
    doa = DOA(rate=16000, chunks=40)


    # data flow between elements
    # ---------------------------
    # src -> ns -> kws
    #    \
    #    doa
    src.pipeline(ch0, ns, kws)

    src.link(doa)

    def on_detected(keyword):
        direction = doa.get_direction()
        print('detected {} at direction {}'.format(keyword, direction))
        pixels.wakeup(direction)

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
    pixels.off()

    # wait a second to allow other threads to exit
    time.sleep(1)

if __name__ == '__main__':
    main()
