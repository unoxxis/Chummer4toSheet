# Main file of chummer to sheet
# Author: Boris Wezisla

# Global Imports
import sys
import logging
import logging.handlers
import argparse

# Child Modules
from sheetwriter import WriteCharacterSheet
from chumreader import ChummerCharacter, ReadChumFile

# Global Variables
with open('VERSION', 'r') as version_file:
    _VERSION_ = version_file.read().replace('\n', '')

# Settings file, that store the configuration.
_DEFAULT_CFGFILENAME_ = 'Chummer4toSheet.cfg'

# Set up logging. If the version ends with -dev, log to screen,
# otherwise, log to file.
_DEFAULT_LOGFILENAME_ = 'Chummer4toSheet.log'
_LOGFORMAT_FILE_ = '%(asctime)s:%(name)s:%(levelname)s: %(message)s'
_LOGFORMAT_CONSOLE_ = '%(name)s:%(levelname)s: %(message)s'


# Main Function
def main(lowres=False, borders=False):
    """
    Main function of Chummer4toSheet

    Parameters:
        lowres (bool): Whether to use low res backgrounds for speed.
        borders (bool): Draw borders around each cell for debug purposes.
    """

    # Logging
    logger = logging.getLogger('main')
    logger.debug('Entering Function')

    # This is a placeholder to test the main two functions before the UI is ready.
    testfile = 'test/chars/Cassida.chum'
    char = ChummerCharacter(testfile)
    WriteCharacterSheet(char, 'test/Cassida.pdf', lowres=lowres, borders=borders)




# Root Function to set up logging and call the main loop:
if __name__ == '__main__':
    # Parse Command Line arguments.
    ap = argparse.ArgumentParser(description='A program to convert Chummer4 XML Character files (*.chum) into PDF character sheets.',
                                 # formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                 )
    ap.add_argument('-L', '--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'],
                    nargs='?', const='info',
                    help='Specify the log level (default: %(default)s)')
    ap.add_argument('-c', '--configfilename', default=_DEFAULT_CFGFILENAME_,
                    help='Filename of the config file (default: %(default)s)')
    ap.add_argument('-l', '--logfilename', default=_DEFAULT_LOGFILENAME_,
                    help='Filename of the logfile (default: %(default)s)')
    ap.add_argument('-X', '--nologfile', action='store_true',
                    help='Disable writing to logfile')
    ap.add_argument('-F', '--forcelogfile', action='store_true',
                    help='Force writing to logfile even in dev builds')
    ap.add_argument('--lowres', action='store_true',
                    help='Use lowres images')
    ap.add_argument('--border', action='store_true',
                    help='Draw border around each cell')
    ap.add_argument('--version', action='version', version=f'%(prog)s v{_VERSION_}')

    options = ap.parse_args()

    # Logging Handlers
    lh_stdout = logging.StreamHandler(sys.stdout)
    lh_stderr = logging.StreamHandler(sys.stderr)
    lh_stderr.setLevel(logging.ERROR)
    lh_logfile = logging.handlers.RotatingFileHandler(options.logfilename, mode='a', encoding='utf16',
                                                      maxBytes=1024 * 1024, backupCount=2)
    # Formatters
    lf_console = logging.Formatter(_LOGFORMAT_CONSOLE_)
    lh_stdout.setFormatter(lf_console)
    lh_stderr.setFormatter(lf_console)
    lf_file = logging.Formatter(_LOGFORMAT_FILE_, datefmt='%Y-%m-%d %H:%M:%S')
    lh_logfile.setFormatter(lf_file)

    if _VERSION_.lower().endswith('dev') or options.nologfile:
        # No File Handler in dev build or when explicitly disabled
        use_logfile = False
    else:
        use_logfile = True

    if options.forcelogfile:
        # Force logfile usage
        use_logfile = True

    if use_logfile:
        _LOGHANDLERS_ = [lh_stderr, lh_stdout, lh_logfile]
    else:
        _LOGHANDLERS_ = [lh_stderr, lh_stdout]

    # Loglevel
    logleveldict = {'debug': logging.DEBUG, 'info': logging.INFO,
                    'warning': logging.WARNING, 'error': logging.ERROR,
                    'critical': logging.CRITICAL}

    logging.basicConfig(
        level=logleveldict[options.loglevel],
        handlers=_LOGHANDLERS_,
    )
    lh_stderr.setLevel(logging.ERROR)

    # LOG FILE HEADER
    logging.info(f'****** This is Chummer4toSheet v{_VERSION_}')

    logging.debug(f'argv = {sys.argv}')
    logging.debug(f'options = {options}')

    try:
        main(lowres=options.lowres, borders=options.border)
        logging.info(f'Program terminated normally!\n******\n\n')

    except Exception:
        logging.critical('Unhandled Fatal Error!', exc_info=True)
        logging.critical(f'Program CRASHED!\n******\n\n')
