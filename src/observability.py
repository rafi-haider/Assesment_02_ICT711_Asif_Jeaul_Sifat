from datetime import datetime


def log_event(service_name, message, correlation_id):
    """
    it Produces a well-organized log entry.

    This is an example of structured logging and correlation IDs to show observability.
    """

    log = {
        "timestamp": datetime.now().isoformat(),
        "service": service_name,
        "message": message,
        "correlation_id": correlation_id
    }

    print(f"[STRUCTURED LOG] {log}")
