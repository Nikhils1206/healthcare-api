class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, 409)


class BadRequestException(AppException):
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, 400)