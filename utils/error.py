class Error:
    def __init__(self, code: int = 0, message: str = ""):
        self.code = code
        self.message = message

    def __repr__(self):
        return f"Error: {self.message} (code: {self.code})"

    def is_empty(self):
        return self.code == 0


def no_error():
    return Error()

def new_error(code, message):
    return Error(code, message)
