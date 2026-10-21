import os
import sys
import cv2
import numpy as np
import pandas as pd

from pathlib import Path
from insightface.app import FaceAnalysis


# --------------------------------------------------
# AttendAI: Student Face Registration
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "Student.csv"
PHOTO_DIR = PROJECT_DIR / "student_photos"
DATABASE_DIR = PROJECT_DIR / "face_database"

EMBEDDINGS_PATH = DATABASE_DIR / "student_embeddings.npz"
REPORT_PATH = DATABASE_DIR / "registration_report.csv"

DETECTION_SIZE = (640, 640)
MIN_FACE_CONFIDENCE = 0.60

REQUIRED_COLUMNS = [
    "Reg_id",
    "name",
    "department",
    "year",
    "section",
    "photo_filename",
]


def normalize_embedding(embedding):
    """Return a unit-normalized facial embedding."""
    embedding = np.asarray(embedding, dtype=np.float32)

    norm = np.linalg.norm(embedding)

    if norm == 0:
        raise ValueError("Embedding has zero norm.")

    return embedding / norm


def main():
    # Verify input files
    if not CSV_PATH.is_file():
        print(f"ERROR: Student CSV not found: {CSV_PATH}")
        sys.exit(1)

    if not PHOTO_DIR.is_dir():
        print(f"ERROR: Photo directory not found: {PHOTO_DIR}")
        sys.exit(1)

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Read student records
    students = pd.read_csv(CSV_PATH, dtype={"Reg_id": str})

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in students.columns
    ]

    if missing_columns:
        print("ERROR: Missing CSV columns:", missing_columns)
        sys.exit(1)

    students["Reg_id"] = students["Reg_id"].str.strip()
    students["photo_filename"] = (
        students["photo_filename"].fillna("").astype(str).str.strip()
    )

    if students["Reg_id"].eq("").any():
        print("ERROR: One or more records have an empty Reg_id.")
        sys.exit(1)

    if students["Reg_id"].duplicated().any():
        duplicates = students.loc[
            students["Reg_id"].duplicated(keep=False), "Reg_id"
        ].tolist()

        print("ERROR: Duplicate registration IDs found:", duplicates)
        sys.exit(1)

    # Initialize InsightFace on CPU
    print("Loading SCRFD + ArcFace models...")

    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"],
        allowed_modules=["detection", "recognition"],
    )

    app.prepare(
        ctx_id=-1,
        det_size=DETECTION_SIZE,
    )

    embeddings = []
    registered_ids = []
    report_rows = []

    print(f"\nProcessing {len(students)} student records...\n")

    for index, student in students.iterrows():
        reg_id = student["Reg_id"]
        name = str(student["name"]).strip()
        filename = student["photo_filename"]

        photo_path = PHOTO_DIR / filename

        status = ""
        detail = ""
        embedding = None

        # Validate the photo path
        if not filename:
            status = "MISSING_FILENAME"
            detail = "No photo filename in CSV"

        elif not photo_path.is_file():
            status = "MISSING_PHOTO"
            detail = f"Photo not found: {filename}"

        else:
            image = cv2.imread(str(photo_path))

            if image is None:
                status = "UNREADABLE_IMAGE"
                detail = "OpenCV could not read the image"

            else:
                try:
                    faces = app.get(image)

                    if len(faces) == 0:
                        status = "NO_FACE"
                        detail = "No face detected"

                    elif len(faces) > 1:
                        status = "MULTIPLE_FACES"
                        detail = (
                            f"Detected {len(faces)} faces; "
                            "manual review required"
                        )

                    else:
                        face = faces[0]
                        confidence = float(face.det_score)

                        if confidence < MIN_FACE_CONFIDENCE:
                            status = "LOW_CONFIDENCE"
                            detail = (
                                f"Detection confidence {confidence:.3f}"
                            )

                        else:
                            embedding = normalize_embedding(
                                face.embedding
                            )

                            status = "REGISTERED"
                            detail = (
                                f"Detection confidence {confidence:.3f}"
                            )

                except Exception as exc:
                    status = "PROCESSING_ERROR"
                    detail = str(exc)

        if embedding is not None:
            embeddings.append(embedding)
            registered_ids.append(reg_id)

        report_rows.append({
            "Reg_id": reg_id,
            "name": name,
            "photo_filename": filename,
            "status": status,
            "details": detail,
        })

        print(
            f"[{index + 1:02d}/{len(students)}] "
            f"{reg_id} | {name} | {status}"
        )

    # Save embeddings without modifying original student data
    report = pd.DataFrame(report_rows)
    report.to_csv(REPORT_PATH, index=False)

    if embeddings:
        np.savez_compressed(
            EMBEDDINGS_PATH,
            reg_ids=np.asarray(registered_ids, dtype=str),
            embeddings=np.stack(embeddings).astype(np.float32),
        )

    # Summary
    print("\n" + "=" * 55)
    print("ATTENDAI STUDENT REGISTRATION SUMMARY")
    print("=" * 55)

    print(f"Total student records : {len(students)}")
    print(f"Registered embeddings: {len(embeddings)}")
    print(f"Needs review          : {len(students) - len(embeddings)}")

    print("\nStatus breakdown:")
    print(report["status"].value_counts().to_string())

    if embeddings:
        print(f"\nEmbedding database: {EMBEDDINGS_PATH}")
        print(f"Embedding shape: {np.stack(embeddings).shape}")
    else:
        print("\nNo embeddings saved because no students were registered.")

    print(f"Registration report: {REPORT_PATH}")
    print("\nOriginal CSV and student photos were not modified.")


if __name__ == "__main__":
    main()
