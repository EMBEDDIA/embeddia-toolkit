class ServiceNotAvailableError(Exception):
    """Raised when service is not available.""" 
    pass

class ServiceFailedError(Exception):
    """Raised when service returns non-200 response."""
    pass