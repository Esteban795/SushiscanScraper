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
    
def except_hook(exctype,value,traceback):
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
        case _:
            print(f"Something went wrong : {value}, {traceback}")