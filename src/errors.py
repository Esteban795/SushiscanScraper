class NotFound404(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidWebsite(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidStatusCode(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidRangeFormat(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoResultsFound(Exception):
    def __init__(self,*args: object) -> None:
        super().__init__(*args)