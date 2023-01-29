from datetime import datetime


class POI_suggestions:
    def __init__(
        self, pid, suggestion_name, notes, submission_time, submitted_by
    ) -> None:
        self.pid = pid
        self.suggestion_name = suggestion_name
        self.notes = notes
        self.submission_time = submission_time
        self.submitted_by = submitted_by

    def get_pid(self):
        return self.pid

    def to_dict(self):
        poi_suggestion_dict = {
            "_pid": self.pid,
            "suggestion_name": self.suggestion_name,
            "notes": self.notes,
            "submission_time": self.submission_time,
            "submitted_by": self.submitted_by,
        }
        return poi_suggestion_dict

    def from_dict(self, poi_suggestion):
        pass
