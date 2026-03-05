from multiprint_agent.core.exceptions import BadRequestError


class PrintRequestDTO:

    VALID_MODES = {"print", "test"}

    def __init__(self, data: dict):

        if not isinstance(data, dict):
            raise BadRequestError("Invalid JSON payload")

        self.mode = data.get("mode") or "print"  # Default to 'print' if not provided

        if self.mode not in self.VALID_MODES:
            raise BadRequestError(f"Invalid mode '{self.mode}'")

        self.raw = data.get("raw")
        self.content_type = data.get("contentType")
        self.encoding = data.get("encoding")

        if self.mode != "test" and not self.raw:
            raise BadRequestError("raw is required")