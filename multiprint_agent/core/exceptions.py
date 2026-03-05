class AppError(Exception):
    status_code = 500
    error_code = "internal_error"
    default_message = "Unexpected error"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = 400
    error_code = "bad_request"
    default_message = "Bad request"


class UnauthorizedError(AppError):
    status_code = 401
    error_code = "unauthorized"
    default_message = "Unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    error_code = "forbidden"
    default_message = "Forbidden"


class NotFoundError(AppError):
    status_code = 404
    error_code = "not_found"
    default_message = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    error_code = "conflict"
    default_message = "Conflict"


class TooManyRequestsError(AppError):
    status_code = 429
    error_code = "rate_limited"
    default_message = "Rate limit exceeded"


class ServiceUnavailableError(AppError):
    status_code = 503
    error_code = "service_unavailable"
    default_message = "Service temporarily unavailable"
    