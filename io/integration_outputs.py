"""
Integration example using 2 output channels of the IPC output board

RESULT_READY_CHANNEL tells a PLC that the EF has made a pass/fail decision
RESULT_PASS_CHANNEL tells the PLC that the current part has passed (signal high)
    or that the current part has failed (signal low)

"""

import os
from time import sleep

from ipcio import write_channels


# read in all channel config from environment
RESULT_READY_CHANNEL = os.environ['RESULT_READY_CHANNEL']
RESULT_PASS_CHANNEL = os.environ['RESULT_PASS_CHANNEL']


def process_input(media, sma, prev_smas):
    """
    determine if a part passed or failed based on input
    subject_media_association.

    when results are ready, set RESULT_READY_CHANNEL high.

    if part passed, set RESULT_PASS_CHANNEL high, else low.

    hold output signal for 200ms
    """
    detection_probability = sma['probability']
    if detection_probability >= 0.5:
        # defect found
        # set RESULT_PASS_CHANNEL low
        passfail = 1 << RESULT_READY_CHANNEL
    else:
        # no defect found, part passed
        # set RESULT_PASS_CHANNEL high
        passfail = 1 << RESULT_READY_CHANNEL | 1 << RESULT_PASS_CHANNEL
   
    # write pass/fail status to io board
    write_channels(passfail)

    # hold output signal for 200ms
    sleep(0.2)

    # set everything back to 0/low
    write_channels(0x0)
