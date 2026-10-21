import cv2
from insightface.app import FaceAnalysis

# Load SCRFD + ArcFace
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

app.prepare(ctx_id=-1, det_size=(640, 640))

# Open an image
image_path = "test_face.jpg"
image = cv2.imread(image_path)

if image is None:
    print(f"ERROR: Could not load {image_path}")
    print("Place a test image named test_face.jpg in this folder.")
    raise SystemExit(1)

# Detect faces
faces = app.get(image)

print(f"Faces detected: {len(faces)}")

for i, face in enumerate(faces, start=1):
    print(f"\nFace {i}")
    print(f"  Bounding box: {face.bbox.astype(int)}")
    print(f"  Detection score: {face.det_score:.3f}")
    print(f"  Embedding dimensions: {face.embedding.shape[0]}")

    # Draw the detection
    x1, y1, x2, y2 = face.bbox.astype(int)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.putText(
        image,
        f"Face {i}: {face.det_score:.2f}",
        (x1, max(y1 - 10, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

# Save the result
output_path = "face_detection_result.jpg"
cv2.imwrite(output_path, image)

print(f"\nResult saved to: {output_path}")
