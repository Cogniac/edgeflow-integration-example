"""
Integration example using 1 input channel

Route assertions to 1 subject for PART_TYPE_CHANNEL high,
and another way if PART_TYPE_CHANNEL low.
"""

import os
from time import sleep

from ipcio import read_channel


# read channel config from environment
PART_TYPE_CHANNEL = os.environ['PART_TYPE_CHANNEL']


# other required config
SUBJECT_A = 'subject_a_xyz'
SUBJECT_B = 'subject_b_123'


def process_input(media, sma, prev_smas):
    """
    Check current part type bitstate upon function call

    If signal is high, route to subject A, else subject B
    """

    part_type_bitstate = read_channel(PART_TYPE_CHANNEL)

    if part_type_bitstate == 1:
        # route to subject A when signal is high
        output_sma = {'subject_uid': SUBJECT_A, 'probability': 1.0}
    else:
        # route to subject B when signal is low
        output_sma = {'subject_uid': SUBJECT_B, 'probability': 1.0}

    return media, [output_sma]
