from logging import Logger, Formatter, FATAL, DEBUG,ERROR, FileHandler, StreamHandler

def _getFormatter() -> Formatter:
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return formatter

def _addFileHandlerForAll(logger: Logger, formatter: Formatter) -> Logger:
    fh = FileHandler(f"logs/debug_{logger.name}.log") if logger.name else FileHandler("debug.log")
    fh.setLevel(DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def _addStreamHandlerForError(logger: Logger, formatter: Formatter) -> Logger:
    ch = StreamHandler()
    ch.setLevel(ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def _getDebugLogger(expected=False, formatter: Formatter = _getFormatter()) -> Logger:
    logger_name = "expected" if expected else "unexpected"
    level = DEBUG if expected else FATAL
    logger = Logger(logger_name)
    logger.setLevel(level)
    streamhandled_logger = _addStreamHandlerForError(logger, formatter)
    filehandled_logger = _addFileHandlerForAll(streamhandled_logger, formatter)
    return filehandled_logger

