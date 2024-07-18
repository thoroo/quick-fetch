"""Exception subclasses for file downloading."""

class FailedGrabError(Exception):
    """Base exception for grab exceptions."""
    pass

class FailedFetchError(Exception):
    """Base exception for fetch exceptions."""
    pass