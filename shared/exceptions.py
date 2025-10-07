class AppError(Exception):
    """Base class for all application-level errors."""

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.context = context or {}


class DatabaseError(AppError):
    """Raised when database operation fails."""


# VERIFICATION ERRORS


class HeaderVerificationError(AppError):
    """Raised when header verification fails."""


class SignatureVerificationError(AppError):
    """Raised when signature verification fails."""


class MessageDoesNotExistError(AppError):
    """Raised when a message does not exist in the database."""


class MessageUpdateError(AppError):
    """Raised when a message update fails."""


class BatchSendError(AppError):
    """Raised when batch send to API fails."""


class UnexpectedAppError(AppError):
    """Raised for unhandled errors."""
