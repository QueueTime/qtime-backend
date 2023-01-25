class POI_suggestions:
    def __init__(
        self, pid, suggestion_name, notes, submission_time, submitted_by
    ) -> None:
        self.pid = pid
        self.suggestion_name = suggestion_name
        self.notes = notes
        self.submission_time = submission_time
        self.submitted_by = submitted_by
