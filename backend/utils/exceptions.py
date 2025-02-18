class BasicException(BaseException):
    GENERAL_MESSAGE = ""

    def __init__(self, value=""):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def get_err_msg(self):
        return f"{self.GENERAL_MESSAGE}: {str(self.value)}"


class UserError(BasicException):
    GENERAL_MESSAGE = "User Error"


class MissingInputError(BasicException):
    GENERAL_MESSAGE = "Missing Input Error"


class AlreadyExistError(BasicException):
    GENERAL_MESSAGE = "Already Exist Error"
