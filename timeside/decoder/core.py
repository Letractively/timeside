#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2007-2011 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2011 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2011 Paul Brossier <piem@piem.org> 
#
# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Authors: Paul Brossier <piem@piem.org>
#          Guilaume Pellerin <yomguy@parisson.com>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IDecoder
from numpy import array, frombuffer, getbuffer, float32, append
from timeside.decoder.sink import *

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init()

class FileDecoder(Processor):
    """ gstreamer-based decoder """
    implements(IDecoder)

    audioformat = None
    audiochannels = None
    audiorate = None
    audionframes = None
    mimetype = ''
    
    # IProcessor methods

    @staticmethod
    @interfacedoc
    def id():
        return "gstreamerdec"

    def setup(self, channels = None, samplerate = None, nframes = None):
        
        self.sink = TimesideSink(self.uri)
        self.sink.setup()
    
    @interfacedoc
    def channels(self):
        return  self.sink.audiochannels

    @interfacedoc
    def samplerate(self):
        return self.sink.audiorate

    @interfacedoc
    def nframes(self):
        return self.sink.audionframes

    @interfacedoc
    def process(self, frames = None, eod = False):
        try:
            #buf = self.sink.emit('pull-buffer')                
            buf = self.sink.pull()
            print 'o'
        except SystemError, e:
            # should never happen
            print 'SystemError', e
            return array([0.]), True
        if buf == None:
            return array([0.]), True
        return buf, False

    @interfacedoc
    def release(self):
        # nothing to do for now
        pass

    ## IDecoder methods

    @interfacedoc
    def __init__(self, uri):
        self.uri = uri

    @interfacedoc
    def format(self):
        # TODO check
        if self.mimetype == 'application/x-id3':
            self.mimetype = 'audio/mpeg'
        return self.mimetype

    @interfacedoc
    def encoding(self):
        # TODO check
        return self.mimetype.split('/')[-1]

    @interfacedoc
    def resolution(self):
        # TODO check: width or depth?
        return self.audiowidth

    @interfacedoc
    def metadata(self):
        # TODO check
        return self.tags


