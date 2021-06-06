# Global Data

import logging
import yaml


def init():
    """
    Loads the global data. Call only once!!
    """

    # Logging
    logger = logging.getLogger('chumdata.init')
    logger.debug('Entering Function')

    yamlfile = 'data/metatypes.yaml'
    with open(yamlfile, mode='r') as fp:
        global Metatypes
        Metatypes = yaml.safe_load(fp)
    logger.info(f"Read Metatype Data from '{yamlfile}'")
