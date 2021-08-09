"""
Integration Reference Code

For use in Cogniac "Integration" application type

"""

# import our relevant configuration

from edgeflow import APP_INPUT_SUBJECT_UIDS       # list of this app's input  subject_uids
from edgeflow import APP_OUTPUT_SUBJECT_UIDS      # list of this app's output subject_uids
from edgeflow import TENANT_CAMERA_CONFIG         # list of all tenant cameras
from edgeflow import TENANT_SUBJECT_CONFIG        # list of all tenant subjects
from edgeflow import TENANT_CUSTOM_DATA           # contents of the tenant's custom_data field

"""
The individual tenant subject config dictionaries include the following info:

      subject_uid (string):    The subject_uid of the input or output subject
      name (string):           The name of the subject
      external_id(string):     The subject external_id (if any)
      custom_data(string):     The subject custom_data (if any)
"""


def process_input(media,
                  input_subject_association,
                  other_subject_associations):
    """
    Integration handler: called for each input to this application.

    media(dict):                       Media dictionary as defined below
    input_subject_association(dict):   The immediate subject association input to this app
    other_subject_associations(list):  List of dictionaries for preceeding (upstream) subject associations

    For both input_subject_association and other_subject_associations, the subject association
    dictionary contents are as follows:

        subject_uid (string):    The subject_uid for this association.
        focus (dict):            Focus dictionary if any
        probability (float):     The probability of the subject-media association.
        app_data_type (string):  The type of the optional app_data, or None
        app_data (object):       The optional app data object, or None

    The media dictionary is defined as follows:

        media_bytes (string):        The actual media bytes. May be None if no media available yet.
        media_type (string):         "image" or "video" (required if media_bytes is present)
        capture_timestamp (float):   Unix epoch timestamp associated with media capture (optional)
        domain_unit (string):        The "domain unit" associated with this media (optional)
        trigger_id (string):         Unique trigger identifier leading to this media or sequence of media (optional)
        trigger_timestamp (float):   Unix expoch timestamp associated with the trigger event
        sequence_ix (integer):       Index of this media within a trigger_id sequence (optional)
        external_media_id (string):  external system identifier associated with this media (optional)
        custom_data (string):        external system data associated with this media (optional)


    This function should return a tuple as follows:

    (media, [output_associations])

    The output media dictionary should be in the same format as the input media dictionary.

    The [output_associations] is a list of dictionaries of the same format as subject_associations.
    The subject_uid in each output_assocation must be from the application's configured output subjects.

    """
    print("process_input: {}".format(input_subject_association))

    if not APP_OUTPUT_SUBJECT_UIDS:
        return {}, []

    subject_uid = APP_OUTPUT_SUBJECT_UIDS[0]
    data = {'foo': 'baz'}

    output_association = {'subject_uid': subject_uid,
                          'focus': None,
                          'probability': 1,
                          'app_data_type': 'raw',
                          'app_data': data}

    return media, [output_association]
