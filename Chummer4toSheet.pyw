# Main file of chummer to sheet
# Author: Boris Wezisla

# Global Imports
import sys
import logging
import logging.handlers

# Child Modules
from sheetwriter import WriteCharacterSheet

# Global Variables
with open('VERSION', 'r') as version_file:
    _VERSION_ = version_file.read().replace('\n', '')

# Settings file, that store the configuration.
_SETTINGS_FILENAME_ = 'Chummer4toSheet.cfg'

# Set up logging. If the version ends with -dev, log to screen,
# otherwise, log to file.
_LOGFILENAME_ = 'Chummer4toSheet.log'
_LOGFORMAT_FILE_ = '%(asctime)s:%(name)s:%(levelname)s: %(message)s'
_LOGFORMAT_CONSOLE_ = '%(name)s:%(levelname)s: %(message)s'


# Main Function
def main():
    # Logging
    logger = logging.getLogger('main')
    logger.debug('Entering Function')

    dummychar = {'Name': 'Doof', 'SomeParameter': 'Value1'}

    WriteCharacterSheet(dummychar, 'Testdatei.pdf')


# Root Function to set up logging and call the main loop:
if __name__ == '__main__':
    # Parse Command Line arguments.
    _DEBUG_ = False
    if(len(sys.argv) > 1):
        if sys.argv[1].lower() == 'debug':
            _DEBUG_ = True
    # TODO: Replace this with argparse to set char.xml, pdfname, debug, loglevel, ...

    # Logging Handlers
    lh_stdout = logging.StreamHandler(sys.stdout)
    lh_stderr = logging.StreamHandler(sys.stderr)
    lh_stderr.setLevel(logging.ERROR)
    lh_logfile = logging.handlers.RotatingFileHandler(_LOGFILENAME_, mode='a', encoding='utf16',
                                                      maxBytes=1024 * 1024, backupCount=5)
    # Formatters
    lf_console = logging.Formatter(_LOGFORMAT_CONSOLE_)
    lh_stdout.setFormatter(lf_console)
    lh_stderr.setFormatter(lf_console)
    lf_file = logging.Formatter(_LOGFORMAT_FILE_, datefmt='%Y-%m-%d %H:%M:%S')
    lh_logfile.setFormatter(lf_file)

    if _VERSION_.lower().endswith('dev'):
        # No File Handler in dev build
        use_logfile = False
    else:
        use_logfile = True

    if use_logfile:
        _LOGHANDLERS_ = [lh_stderr, lh_stdout, lh_logfile]
    else:
        _LOGHANDLERS_ = [lh_stderr, lh_stdout]

    # Loglevel
    if _DEBUG_:
        _LOGLEVEL_ = logging.DEBUG
    else:
        _LOGLEVEL_ = logging.INFO

    logging.basicConfig(
        level=_LOGLEVEL_,
        handlers=_LOGHANDLERS_,
    )
    lh_stderr.setLevel(logging.ERROR)

    # LOG FILE HEADER
    logging.info(f'****** This is Chummer4toSheet v{_VERSION_}')

    if _DEBUG_:
        logging.debug(f'Debug flag is set to true, outputting debug information from now on!')
    logging.debug(f'argv = {sys.argv}')

    try:
        main()
        logging.info(f'Program terminated normally!\n******\n\n')

    except Exception:
        logging.critical('Unhandled Fatal Error!', exc_info=True)
        logging.critical(f'Program CRASHED!\n******\n\n')
