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

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from utils import downsample_blocking
import numpy as np


class Waveform(Analyzer):
    implements(IAnalyzer)  # TODO check if needed with inheritance

    def __init__(self):
        self.input_blocksize = 2048
        self.input_stepsize = self.input_blocksize / 2

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Waveform, self).setup(channels, samplerate,
              blocksize, totalframes)
        self.values = []
        self.result_blocksize = 1
        self.result_stepsize = 1

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform Analyzer"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.input_blocksize):
            self.values.append(samples)

        return frames, eod

    def release(self):
        # set Result
        waveform = self.new_result(data_mode='value', time_mode='framewise')

        # Set Data
        waveform.data_object.value = np.asarray(self.values).flatten()

        self._results.add(waveform)
