class FinanceError(Exception):
    """Base class for all expected (user-facing) errors in yapp."""


class InvalidInputError(FinanceError):
    """Raised when user-provided input fails validation."""
