class PrintResponseDTO:
    def __init__(self, success: bool, data: dict | None = None, error: dict | None = None):
        self.success = success
        self.data = data or {}
        self.error = error

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
        }