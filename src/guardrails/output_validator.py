class OutputValidator:
    FORBIDDEN = ["i fabricated", "guaranteed breach without evidence"]

    def is_safe_and_grounded(self, report: str) -> bool:
        lowered = report.lower()
        if any(token in lowered for token in self.FORBIDDEN):
            return False
        return "incident summary" in lowered
