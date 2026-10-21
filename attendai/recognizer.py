import numpy as np
from pathlib import Path

from attendai.detector import FaceDetector


class FaceRecognizer:
    """Match detected faces against registered student embeddings."""

    def __init__(
        self,
        database_path=None,
        min_detection_confidence=0.60,
        min_similarity=0.45,
        min_similarity_margin=0.05,
    ):
        project_dir = Path(__file__).resolve().parent.parent

        if database_path is None:
            database_path = (
                project_dir
                / "face_database"
                / "student_embeddings.npz"
            )

        database_path = Path(database_path)

        if not database_path.is_file():
            raise FileNotFoundError(
                f"Embedding database not found: {database_path}"
            )

        data = np.load(database_path, allow_pickle=False)

        self.reg_ids = data["reg_ids"].astype(str)
        self.embeddings = data["embeddings"].astype(np.float32)

        if self.embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D array.")

        if self.embeddings.shape[0] != len(self.reg_ids):
            raise ValueError(
                "Student IDs and embeddings have different lengths."
            )

        if self.embeddings.shape[1] != 512:
            raise ValueError("Expected 512-dimensional embeddings.")

        norms = np.linalg.norm(self.embeddings, axis=1)

        if np.any(norms == 0):
            raise ValueError("Database contains a zero embedding.")

        # Ensure every registered embedding is normalized.
        self.embeddings /= norms[:, None]

        self.min_detection_confidence = min_detection_confidence
        self.min_similarity = min_similarity
        self.min_similarity_margin = min_similarity_margin

        self.detector = FaceDetector()

    def recognize(self, image):
        """
        Recognize faces in a BGR image.

        Returns one result per detected face. A match is accepted only
        when the best similarity and the gap over the runner-up pass
        the configured initial thresholds.
        """
        detected_faces = self.detector.extract_faces(image)
        results = []

        for face in detected_faces:
            embedding = face["embedding"].astype(np.float32)
            norm = np.linalg.norm(embedding)

            if norm == 0:
                results.append({
                    "status": "UNKNOWN",
                    "reg_id": None,
                    "similarity": None,
                    "margin": None,
                    "reason": "Invalid zero embedding",
                    "bbox": face["bbox"].tolist(),
                })
                continue

            embedding /= norm

            # Embeddings are normalized, so dot product gives
            # cosine similarity.
            similarities = self.embeddings @ embedding

            ranked_indices = np.argsort(similarities)[::-1]
            best_idx = int(ranked_indices[0])
            best_similarity = float(similarities[best_idx])

            if len(ranked_indices) > 1:
                second_similarity = float(
                    similarities[int(ranked_indices[1])]
                )
                margin = best_similarity - second_similarity
            else:
                margin = float("inf")

            detection_ok = (
                face["confidence"] >= self.min_detection_confidence
            )
            similarity_ok = best_similarity >= self.min_similarity
            margin_ok = margin >= self.min_similarity_margin

            if not detection_ok:
                status = "REVIEW"
                reason = "Low face-detection confidence"
            elif not similarity_ok:
                status = "UNKNOWN"
                reason = "Similarity below threshold"
            elif not margin_ok:
                status = "REVIEW"
                reason = "Top two candidates are too close"
            else:
                status = "MATCH"
                reason = "Initial thresholds passed"

            results.append({
                "status": status,
                "reg_id": (
                    str(self.reg_ids[best_idx])
                    if status == "MATCH"
                    else None
                ),
                "candidate_reg_id": str(self.reg_ids[best_idx]),
                "similarity": round(best_similarity, 4),
                "margin": round(margin, 4),
                "detection_confidence": round(
                    float(face["confidence"]), 4
                ),
                "reason": reason,
                "bbox": face["bbox"].tolist(),
            })

        return results
