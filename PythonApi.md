# Note: This project has been moved to [yomguy/TimeSide on GitHub](https://github.com/yomguy/TimeSide). #

# Python API #

_Warning: this page describes the new API proposal for TimeSide 0.2_. It is a work in progress.

The TimeSide python API provides server-side tools for audio transcoding, effects, analysis, and visualization.
It is primarily meant to run on a web server, thus serving data to the [TimeSide UI](UiGuide.md) components,
but can also be used in other contexts such as native applications.

This API relies on two main concepts: _processors_ and _pipes_. Processors can be piped into each other
in order to, for example: decode a file, compute its max level, produce a waveform and encode to a compressed
audio format. The pipe paradigm allows to performs several operations in one run, so that the source file/stream
is decoded and read only once.

## Quick Start ##

A most basic operation, transcoding, is easily performed with two processors:

```
from timeside import Decoder, OggEncoder

decoder = Decoder('myfile.wav')
encoder = OggEncoder("myfile.ogg")
pipe    = decoder | encoder
pipe.run()
```

As one can see in the above example, creating a processing pipe is performed with
the binary OR operator.

Audio data visualisation can be performed using graphers, such as Waveform and
Spectrogram. All graphers return a [PIL image](http://www.pythonware.com/library/pil/handbook/image.htm):

```
from timeside import Decoder, Spectrogram

decoder     = Decoder('myfile.wav')
spectrogram = Spectrogram(width=400, height=150)

(decoder | spectrogram).run()

spectrogram.render().save('graph.png')
```

It is possible to create longer pipes, as well as subpipes, here for both
analysis and encoding:

```
from timeside import Decoder, Waveform, MaxLevel, MeanLevel, Mp3Encoder, FlacEncoder

decoder  = Decoder('myfile.wav')
max      = MaxLevel()
mean     = MeanLevel()
encoders = Mp3Encoder('myfile.mp3') | FlacEncoder('myfile.flac')

(decoder | max | mean | encoders).run()

print "Max level: %s, Mean level: %s" % (max, mean)
```

A common operation, normalization, can be performed in two steps, using
both an analyzer and an effect, which also shows that processors (here the Decoder)
can be reused in several runs:

```
from timeside import Decoder, MaxLevel, Gain, WavEncoder

decoder  = Decoder('source.wav')
max      = MaxLevel()

(decoder | max).run()

gain = max.result() > 0 and (1 / max.result()) or 1

(decoder | Gain(gain) | WavEncoder('normalized.wav')).run()
```