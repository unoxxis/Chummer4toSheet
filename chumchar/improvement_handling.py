# Scan for Improvements

import logging


def ScanImprovements(improvements, itype=None, iproperty=None, iattribute=None, ieffect=None, return_text=False):
    """
    Scans the improvement list and collects similar improvements. Returns the associated value.

    Mandatory Parameters:
        improvements (dict): The improvements dict from a character.
        itype (str): Type of improvement

    Optional Parameters:
        depend on the improvement type and select improvements. Matching improvements will be added.

    Returns:
        modified value for numeric type improvements
        true/false for effect improvements
    """

    # Logging
    logger = logging.getLogger('chumchar.ScanImprovements')
    # logger.debug('Entering Function')

    if itype is None:
        raise AttributeError('itype argument is mandatory')

    text = ''
    if itype == 'attribute':
        # Get Attribute Modifiers:
        retval = 0
        for key, impr in improvements.items():
            if impr['type'] == itype:
                if impr['property'] == iproperty and impr['attribute'] == iattribute:
                    retval += impr['value']
                    text += f"{impr['value']:+d} ({impr['text']})\n"
    elif itype == 'derived':
        # Get Attribute Modifiers:
        retval = 0
        for key, impr in improvements.items():
            if impr['type'] == itype:
                if impr['property'] == iproperty:
                    retval += impr['value']
                    text += f"{impr['value']:+d} ({impr['text']})\n"
    elif itype == 'special':
        retval = False
        for key, impr in improvements.items():
            if impr['type'] == itype:
                if impr['effect'] == ieffect:
                    retval = True

    if text != '':
        text = text[:-1]  # Kill last newline

    if retval != 0:
        logger.debug(f"Return value: {retval} '{text}'")

    if return_text:
        return retval, text
    else:
        return retval
