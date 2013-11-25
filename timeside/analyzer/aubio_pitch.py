# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>

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

# Author: Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from preprocessors import downmix_to_mono, frames_adapter
from aubio import pitch


class AubioPitch(Analyzer):
    implements(IAnalyzer)  # TODO check if needed with inheritance

    def __init__(self):
        super(AubioPitch, self).__init__()
        self.input_blocksize = 2048
        self.input_stepsize = self.input_blocksize / 2

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(AubioPitch, self).setup(channels,
                                      samplerate,
                                      blocksize,
                                      totalframes)
        self.p = pitch("default", self.input_blocksize, self.input_stepsize,
                       samplerate)
        self.p.set_unit("freq")
        self.block_read = 0
        self.pitches = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_pitch"

    @staticmethod
    @interfacedoc
    def name():
        return "f0 (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return "Hz"

    def __str__(self):
        return "pitch values"

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        #time = self.block_read * self.input_stepsize * 1. / self.samplerate()
        self.pitches += [self.p(frames)[0]]
        self.block_read += 1
        return frames, eod

    def post_process(self):
        pitch = self.new_result(data_mode='value', time_mode='framewise')

        # parameters : None # TODO check with Piem "default" and "freq" in
        # setup

        pitch.data_object.value = self.pitches
        self.pipe.results.add(pitch)
