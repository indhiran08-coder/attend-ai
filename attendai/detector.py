import cv2
import numpy as np
from insightface.app import FaceAnalysis


class FaceDetector:
    """Face detection and embedding extraction for AttendAI."""

    def __init__(self, det_size=(640, 640)):
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
            allowed_modules=["detection", "recognition"],
        )

        self.app.prepare(
            ctx_id=-1,
            det_size=det_size,
        )

    def detect_faces(self, image):
        """Detect faces in a BGR image."""
        if image is None or image.size == 0:
            raise ValueError("Invalid or empty image.")

        return self.app.get(image)

    def extract_faces(self, image):
        """Return bounding boxes, confidence scores and embeddings."""
        results = []

        for face in self.detect_faces(image):
            results.append({
                "bbox": face.bbox.astype(int),
                "confidence": float(face.det_score),
                "embedding": face.embedding.astype(np.float32),
            })

        return results
