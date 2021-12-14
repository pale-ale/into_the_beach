import datetime

class Logger:
    """
    A simple logging helper. Writes text to a file named after current start date/time.
    Log levels are: 0:Debug, 1:Warning, 2:Error
    """
    _LOG_FILE_PATH = str(datetime.datetime.now()) + ".log"
    _VERBOSITY = 0
    _SUFFIXES=["[DEBUG]", "[WARNING]", "[ERROR]"]
    # 01 for terminal, 10 for file, 11 for both, 00 for neither
    _OUTPUT_MODE = 0b10
    _OUTPUT_MODE_FILE = 0b01
    _OUTPUT_MODE_TERM = 0b10


def log(text:str, level:int):
    """
    Write text to terminal or to file.
    @text: Text to write.
    @level: Log level for filtering and prefix.
    """
    assert(0 <= level and level < len(Logger._SUFFIXES))
    if level >= Logger._VERBOSITY:
        if Logger._OUTPUT_MODE & Logger._OUTPUT_MODE_FILE:
            _log_to_file(text=text, level=level)
        if Logger._OUTPUT_MODE & Logger._OUTPUT_MODE_TERM:
            _log_to_term(text=text, level=level)

def _log_to_term(text:str, level:int):
    """Writes to the terminal"""
    print(f"{Logger._SUFFIXES[level]}: {text}")

def _log_to_file(text:str, level:int):
    """Writes into a file"""
    with open(Logger._LOG_FILE_PATH, "a") as file:
        file.write("f{Logger._SUFFIXES[level]}: {text}\n")