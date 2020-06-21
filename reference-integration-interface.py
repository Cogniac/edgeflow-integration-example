"""
Integration Reference Code

For use in Cogniac "Integration" application type
"""


def configure_subjects(input_subjects, output_subjects):
    """
    configure the integration app subjects.  This is called once at startup.
    If application configuration changes this module will terminate and be reloaded.

    input_subjects:   list of input subject dictionaries
    output_subjects:  list of output subject dictionaries

    contents of the subject dictionaries are as follows:
      subject_uid (string):    The subject_uid of the input or output subject
      name (string):           The name of the subject
      external_id(string):     The subject external_id
    """
    if input_subjects:
        print "Input Subjects:"
    for i in input_subjects:
        print "\t", i
    if output_subjects:
        print "Ouput Subjects:"
    for i in output_subjects:
        print "\t", i



def process_input(subject_associations,
                  media_bytes=None,
                  domain_unit=None):

    """
    Integration handler: called for each input subject association:

    subject_associations(list):  List of dictionaries for each upstream subject association.
                                 The most recent input association (e.g. containing this app's subject_uid)
                                 will be found at the end of the list.
                                 The subject association contents are as follows:
        subject_uid (string):    The subject_uid for this association.
        focus (dict):            Focus dictionary if any
        probability (float):     The probability of the subject-media association.
        app_data_type (string):  The type of the optional app_data, or None
        app_data (object):       The optional app data object, or None

    media_bytes (string):        The actual media bytes. May be None if no media available yet.
    domain_unit (string):        The "domain unit" association with this media if known.

    This function should return a tuple as follows:

    (output_associations, media_bytes, domain_unit)

    The output_associations is a list of dictionaries of the same format as subject_associations.
    The subject_uid in the output_assocation list is limited to the application's configured output subjects.

    media_bytes should be None unless new media has been created

    The output domain_unit must be None if an input domain_unit was not None. E.g. a domain unit can only
    be specified if there is no preceeding domain unit.
    """
    print "process_input", subject_associations, domain_unit
    return ([], None, None)
