from config.settings import (
    TRACKER_IOU_THRESHOLD,
    MAX_MISSED_FRAMES,
)


def intersection_over_union(a, b):
    """Calculate overlap between two bounding boxes."""

    left = max(a["left"], b["left"])
    top = max(a["top"], b["top"])
    right = min(a["right"], b["right"])
    bottom = min(a["bottom"], b["bottom"])

    width = max(0.0, right - left)
    height = max(0.0, bottom - top)
    intersection = width * height

    area_a = max(0.0, a["right"] - a["left"]) * max(
        0.0, a["bottom"] - a["top"]
    )
    area_b = max(0.0, b["right"] - b["left"]) * max(
        0.0, b["bottom"] - b["top"]
    )

    union = area_a + area_b - intersection
    return intersection / union if union > 0 else 0.0


class IoUTracker:
    """Simple tracker that assigns temporary IDs to detections."""

    def __init__(self):
        self.next_id = 1
        self.tracks = {}

    def update(self, detections):
        for track in self.tracks.values():
            track["missed"] += 1

        candidates = []

        for index, detection in enumerate(detections):
            for track_id, track in self.tracks.items():
                score = intersection_over_union(
                    detection, track["box"]
                )

                if score >= TRACKER_IOU_THRESHOLD:
                    candidates.append((score, index, track_id))

        candidates.sort(reverse=True)

        used_detections = set()
        used_tracks = set()
        ids = [None] * len(detections)

        for _, index, track_id in candidates:
            if index in used_detections or track_id in used_tracks:
                continue

            self.tracks[track_id]["box"] = detections[index].copy()
            self.tracks[track_id]["missed"] = 0

            ids[index] = track_id
            used_detections.add(index)
            used_tracks.add(track_id)

        for index, detection in enumerate(detections):
            if index in used_detections:
                continue

            track_id = self.next_id
            self.next_id += 1

            self.tracks[track_id] = {
                "box": detection.copy(),
                "missed": 0,
            }
            ids[index] = track_id

        expired = [
            track_id
            for track_id, track in self.tracks.items()
            if track["missed"] > MAX_MISSED_FRAMES
        ]

        for track_id in expired:
            del self.tracks[track_id]

        return ids
