"""
utils/exceptions.py
-------------------
Custom exception hierarchy for CampusConnect Analytics.
All domain errors raise a subclass of CampusConnectError so the UI
can catch them in a single broad handler when needed.
"""


class CampusConnectError(Exception):
    """Base exception for all CampusConnect domain errors."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}\n{self.details}"
        return self.message


# ---------------------------------------------------------------------------
# Entity not-found errors
# ---------------------------------------------------------------------------

class EventNotFoundError(CampusConnectError):
    """Raised when an event with the given ID does not exist."""


class StudentNotFoundError(CampusConnectError):
    """Raised when a student with the given ID does not exist."""


class RegistrationNotFoundError(CampusConnectError):
    """Raised when a registration record does not exist."""


class FeedbackNotFoundError(CampusConnectError):
    """Raised when a feedback record does not exist."""


# ---------------------------------------------------------------------------
# Duplicate record errors
# ---------------------------------------------------------------------------

class DuplicateEventError(CampusConnectError):
    """Raised when attempting to create an event with an existing ID."""


class DuplicateStudentError(CampusConnectError):
    """Raised when attempting to create a student with an existing ID."""


class DuplicateRegistrationError(CampusConnectError):
    """Raised when a student tries to register for an event they are already registered for."""


class DuplicateFeedbackError(CampusConnectError):
    """Raised when a student submits feedback for an event more than once."""


# ---------------------------------------------------------------------------
# Registration business-rule errors
# ---------------------------------------------------------------------------

class EventFullError(CampusConnectError):
    """Raised when event capacity has been reached."""


class RegistrationClosedError(CampusConnectError):
    """Raised when registration deadline has passed or event status disallows registration."""


class EventCancelledError(CampusConnectError):
    """Raised when attempting to register for a cancelled event."""


# ---------------------------------------------------------------------------
# Feedback business-rule errors
# ---------------------------------------------------------------------------

class InvalidFeedbackError(CampusConnectError):
    """Raised when feedback violates business rules (rating out of range, not registered, etc.)."""


class FeedbackNotAllowedError(CampusConnectError):
    """Raised when a student who is not registered tries to submit feedback."""


class EventNotCompletedError(CampusConnectError):
    """Raised when feedback is submitted before the event is marked as completed."""


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------

class ValidationError(CampusConnectError):
    """Raised when input data fails validation checks."""


# ---------------------------------------------------------------------------
# Authentication errors
# ---------------------------------------------------------------------------

class AuthenticationError(CampusConnectError):
    """Raised when login credentials are incorrect."""


class AuthorizationError(CampusConnectError):
    """Raised when a user tries to perform an action they are not authorized for."""


# ---------------------------------------------------------------------------
# Storage errors
# ---------------------------------------------------------------------------

class DataStorageError(CampusConnectError):
    """Raised when a file read/write operation fails."""
