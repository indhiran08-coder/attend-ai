import csv
from pathlib import Path


class DetectionLogger:
    def __init__(self, output_path):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.file = self.output_path.open(
            "w", newline="", encoding="utf-8"
        )
        self.writer = csv.writer(self.file)

        self.writer.writerow([
            "frame_number",
            "timestamp_seconds",
            "track_id",
            "confidence",
            "left",
            "top",
            "right",
            "bottom",
        ])

    def log_frame(self, frame_number, timestamp, detections, track_ids):
        for detection, track_id in zip(detections, track_ids):
            self.writer.writerow([
                frame_number,
                round(timestamp, 3),
                track_id,
                round(detection["confidence"], 4),
                round(detection["left"], 2),
                round(detection["top"], 2),
                round(detection["right"], 2),
                round(detection["bottom"], 2),
            ])

        self.file.flush()

    def close(self):
        if not self.file.closed:
            self.file.close()
