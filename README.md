ReSpeaker for Raspberry Pi
==========================

The repository contains some examples to use ReSpeaker series mic arrays on Raspberry Pi.

The examples are included in [the custom image](https://v2.fangcloud.com/share/7395fd138a1cab496fd4792fe5?folder_id=188000207913&lang=en) with pre-installed `seeed-voicecard`, `snowboy`, `voice-engine` and etc. You can flash the custom image to get started easily.

### Hardware
ReSpeaker 2 Mic Hat, ReSpeaker 4 Mic Array or ReSpeaker 6 Mic Array (they are all pi hats)

### Software
+ snowboy for KWS (Keyword Search / Keyword Spotting)
+ webrtc audio processing for NS (Noise Suppression)
+ speexdsp for AEC (Acoustic Echo Cancellation)
+ GCC-PHAT for DOA (Direction Of Arrial)
+ avs for alexa voice service
+ voice-engine for connecting all the elements together


```
pip install webrtc-audio-processing speexdsp voice-engine avs
```
and go to [kitt-ai/snowboy](http://github.com/kitt-ai/snowboy) to install snowboy.



### Files

----------------------------------------------------------

```
├── 2mic                               # ReSpeaker 2 Mic Hat
│   └── ns_kws_doa_alexa.py                hands-free alexa with NS, KWS and DOA (0 ~ 180 degree)
├── 4mic                               # ReSpeaker 4 Mic Array
│   ├── kws_doa.py                         KWS and then DOA
│   ├── ns_kws_doa_alexa.py                hands-free alexa with NS, KWS and DOA (0 ~ 360 degree)
│   └── ns_kws_doa.py
├── 6mic                               # ReSpeaker 6 Mic Array
│   ├── aec_ns_kws_doa_alexa.py            hands-free alexa with AEC, NS, KWS and DOA (0 ~ 360 degree)
│   ├── aec_ns_kws_doa.py                  has 2 loopback channels for AEC
│   └── kws_doa.py
├── ns_kws_alexa.py
├── ns_kws.py
└── ns_vs_raw.py                       Compare KWS between raw audio and audio with NS
```

