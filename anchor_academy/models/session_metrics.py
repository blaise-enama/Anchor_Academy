from typing import Optional


class SessionMetric:
    def __init__(
        self,
        metric_id: Optional[int] = None,
        session_id: Optional[int] = None,
        metric_name: str = "",
        metric_value: float = 0.0,
        unit: Optional[str] = None,
    ):
        self.metric_id = metric_id
        self.session_id = session_id
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.unit = unit

    def __repr__(self):
        return f"<Metric {self.metric_name}: {self.metric_value} {self.unit}>"