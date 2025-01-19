from enum import StrEnum

class Errors(StrEnum):
    UNAUTHORIZED = "unauthorized"
    UNAUTHENTIFIED = "unauthentified"
    UNKNOWN = "unknown"
    SERVER_ERROR = "server_error"
