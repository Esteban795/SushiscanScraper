import sys

class NotFound404(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidWebsite(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidStatusCode(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidRangeFormat(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class EmptyResults(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoResultsFound(ValueError):
    def __init__(self,name, *args: object) -> None:
        super().__init__(*args)
        self.name = name

def except_hook(exctype,value,traceback) -> None:
    match exctype:
        case IndexError(msg):
            print(f"Bad index : {msg}")
        case NotFound404(msg):
            print(f"URL {msg} was not found.")
        case InvalidStatusCode(msg):
            print(f"Invalid status code returned by : {msg}")
        case InvalidWebsite(msg):
            print(f"Invalid website : {msg}")
        case FileExistsError(msg):
            print(f"File already exists : {msg}")
        case InvalidRangeFormat(msg):
            print(f"Invalid range format : {msg}")
        case EmptyResults(msg):
            print(f"Empty result : {msg}")
        case NoResultsFound() as e:
            print(f"No results found for : {e.name}")
        case KeyboardInterrupt():
            print("Interrupted by user input.")
        case Exception as e:
            print(f"Something went wrong : {e}")
    return