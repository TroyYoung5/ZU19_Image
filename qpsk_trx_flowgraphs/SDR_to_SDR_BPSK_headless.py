#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SDR_to_SDR_BPSK
# GNU Radio version: 3.6.1git-10128-g92f5e418

from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading




class SDR_to_SDR_BPSK_headless(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "SDR_to_SDR_BPSK", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.tx_gain = tx_gain = 0
        self.timing_loop_bw = timing_loop_bw = 0.0628
        self.samp_rate = samp_rate = 2e6
        self.rx_gain = rx_gain = 10
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 45*nfilts)
        self.excess_bw = excess_bw = 0.35
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bpsk.set_npwr(1.0)
        self.arity = arity = 2

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_1_1_0_1 = zeromq.pub_sink(gr.sizeof_char, 1, 'tcp://0.0.0.0:10003', 100, False, (-1), '', True, True)
        self.zeromq_pub_sink_1_1_0_0 = zeromq.pub_sink(gr.sizeof_float, 1, 'tcp://0.0.0.0:10005', 100, False, (-1), '', True, True)
        self.zeromq_pub_sink_1_1_0 = zeromq.pub_sink(gr.sizeof_float, 1, 'tcp://0.0.0.0:10004', 100, False, (-1), '', True, True)
        self.zeromq_pub_sink_1_1 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://0.0.0.0:10002', 100, False, (-1), '', True, True)
        self.zeromq_pub_sink_1_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://0.0.0.0:10000', 100, False, (-1), '', True, True)
        self.zeromq_pub_sink_0_0_1 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://0.0.0.0:10001', 100, False, (-1), '', True, True)
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('0.0.0.0', 8000), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            sps,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_map_bb_1 = digital.map_bb([0,1])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(arity, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(timing_loop_bw, 2, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts('01',
          0, '')
        self.digital_constellation_modulator_0_0 = digital.generic_mod(
            constellation=bpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(tx_gain+1)
        self.blocks_char_to_float_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_random_source_x_1 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, (0.01*(rx_gain+0.01)), 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.zeromq_pub_sink_0_0_1, 0))
        self.connect((self.analog_random_source_x_1, 0), (self.digital_constellation_modulator_0_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.zeromq_pub_sink_1_1_0, 0))
        self.connect((self.blocks_char_to_float_0_1, 0), (self.zeromq_pub_sink_1_1_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.zeromq_pub_sink_1_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_char_to_float_0_1, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_1, 0))
        self.connect((self.digital_map_bb_1, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_map_bb_1, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.digital_map_bb_1, 0), (self.zeromq_pub_sink_1_1_0_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.zeromq_pub_sink_1_1, 0))


    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 45*self.nfilts))
        self.digital_symbol_sync_xx_0.set_sps(self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 45*self.nfilts))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.blocks_multiply_const_vxx_0.set_k(self.tx_gain+1)

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.timing_loop_bw)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.analog_noise_source_x_0.set_amplitude((0.01*(self.rx_gain+0.01)))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk
        self.digital_constellation_decoder_cb_0.set_constellation(self.bpsk)

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity




def main(top_block_cls=SDR_to_SDR_BPSK_headless, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
