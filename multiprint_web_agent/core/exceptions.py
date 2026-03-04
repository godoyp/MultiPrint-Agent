class AppError(Exception):
    status_code = 500
    error_code = "internal_error"

    def __init__(self, message=None):
        self.message = message or "Unexpected error"
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = 400
    error_code = "bad_request"


class UnauthorizedError(AppError):
    status_code = 401
    error_code = "unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    error_code = "forbidden"


class NotFoundError(AppError):
    status_code = 404
    error_code = "not_found"


class ConflictError(AppError):
    status_code = 409
    error_code = "conflict"


class TooManyRequestsError(AppError):
    status_code = 429
    error_code = "rate_limited"


class ServiceUnavailableError(AppError):
    status_code = 503
    error_code = "service_unavailable"