import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init()
from numpy import array, frombuffer, getbuffer, float32, append

class TimesideSink(object):
    """
    a simple sink element with a hopsize property to adjust the size of the buffer emitted
    """
    
    # duration ms, before discovery process times out
    MAX_DISCOVERY_TIME = 3000

    audioformat = None
    audiochannels = None
    audiorate = None
    audionframes = None
    mimetype = ''
    
    _caps = gst.caps_from_string('audio/x-raw-float, \
                    rate=[ 1, 2147483647 ], \
                    channels=[ 1, 2147483647 ], \
                    endianness={ 1234, 4321 }, \
                    width=32')

    __gsttemplates__ = ( 
            gst.PadTemplate ("sink",
                gst.PAD_SINK,
                gst.PAD_ALWAYS,
                _caps),
            )

    def __init__(self, uri):
        
        # is this a file?
        import os.path
        if os.path.exists(uri):
            # get the absolute path
            uri = os.path.abspath(uri)
            # first run the file/uri through the discover pipeline
            self.discover(uri)
            # and make a uri of it
            from urllib import quote
            self.uri = 'file://'+quote(uri)
        else:
            self.uri = uri
        
        self.blocksize = 2048
        
    def setup(self):
        # the output data format we want
        caps = "audio/x-raw-float, width=32"
        
        self.adapter = gst.Adapter()
        src = gst.element_factory_make('uridecodebin')
        src.set_property('uri', self.uri)
        src.connect('pad-added', self.source_pad_added_cb)

        self.conv = gst.element_factory_make('audioconvert')
        self.apad = self.conv.get_pad('sink')

        capsfilter = gst.element_factory_make('capsfilter')
        capsfilter.set_property('caps', gst.caps_from_string(caps))

        # TODO
        #self.sink.set_property('emit-signals', True)

        self.pipeline = gst.Pipeline()
        self.pipeline.add(src, self.conv, capsfilter)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::tag', self.on_tag)
        self.bus.connect('message::error', self.on_error)

        gst.element_link_many(self.conv, capsfilter)

        self.mainloop = gobject.MainLoop()

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.mainloop.run()

    def source_pad_added_cb(self, src, pad):
        name = pad.get_caps()[0].get_name()
        if name == 'audio/x-raw-float' or name == 'audio/x-raw-int':
            if not self.apad.is_linked():
                pad.link(self.conv.get_pad("sink"))

    def on_eos(self, bus, msg):
        #print 'on_eos'
        self.pipeline.set_state(gst.STATE_NULL)
        self.mainloop.quit()

    def on_tag(self, bus, msg):
        taglist = msg.parse_tag()
        """
        print 'on_tag:'
        for key in taglist.keys():
            print '\t%s = %s' % (key, taglist[key])
        """

    def on_error(self, bus, msg):
        error = msg.parse_error()
        print 'on_error:', error[1]
        self.mainloop.quit()

#    def do_render(self, buffer):
#        self.adapter.push(buffer)
#        return gst.FLOW_OK

    def pull(self):
        print 'ok'
        # TODO use signals
        remaining = self.apad.adapter.available()
        if remaining == 0:
            return None
        if remaining >= self.blocksize:
            return self.gst_buffer_to_numpy_array(self.adapter.take_buffer(self.blocksize))
        if remaining < self.blocksize and remaining > 0:
            return gst_buffer_to_numpy_array(self.adapter.take_buffer(remaining))

    ## gst.extend discoverer

    def discover(self, path):
        """ gstreamer based helper function to get file attributes """
        from gst.extend import discoverer
        d = discoverer.Discoverer(path, timeout = self.MAX_DISCOVERY_TIME)
        d.connect('discovered', self.discovered)
        self.mainloop = gobject.MainLoop()
        d.discover()
        self.mainloop.run()

    def discovered(self, d, is_media):
        """ gstreamer based helper executed upon discover() completion """
        if is_media and d.is_audio:
            # copy the discoverer attributes to self
            self.audiorate = d.audiorate
            self.mimetype= d.mimetype
            self.audiochannels = d.audiochannels
            self.audiowidth = d.audiowidth
            # conversion from time in nanoseconds to frames
            from math import ceil
            duration = d.audiorate * d.audiolength * 1.e-9
            self.audionframes = int (ceil ( duration ) )
            self.tags = d.tags
        elif not d.is_audio:
            print "error, no audio found!"
        else:
            print "fail", path
        self.mainloop.quit()

    def gst_buffer_to_numpy_array(self, buf):
        """ gstreamer buffer to numpy array conversion """
        chan = self.audiochannels
        samples = frombuffer(buf.data, dtype=float32)
        samples.resize([len(samples)/chan, chan])
        return samples


