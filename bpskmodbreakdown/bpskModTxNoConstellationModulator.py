#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: bpskModTxNoConstellationModulator
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
import numpy
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class bpskModTxNoConstellationModulator(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "bpskModTxNoConstellationModulator", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.time_offset = time_offset = 1
        self.taps = taps = 1
        self.sps = sps = 4
        self.samp_rate = samp_rate = 20000000
        self.noise_volt = noise_volt = 0.05
        self.freq_offset = freq_offset = 0
        self.excess_bw = excess_bw = 0.35
        self.bpsk = bpsk = digital.constellation_bpsk().base()

        ##################################################
        # Blocks
        ##################################################
        self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_char*1, 500.0, 0.15)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("Sample Rate: "+str(samp_rate)), 500)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 10000))), True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.blocks_probe_rate_0, 'rate'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_probe_rate_0, 0))


    def get_time_offset(self):
        return self.time_offset

    def set_time_offset(self, time_offset):
        self.time_offset = time_offset

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_message_strobe_0.set_msg(pmt.intern("Sample Rate: "+str(self.samp_rate)))

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk




def main(top_block_cls=bpskModTxNoConstellationModulator, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
