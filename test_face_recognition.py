import cv2

from attendai.recognizer import FaceRecognizer

recognizer = FaceRecognizer()

image_path = "test_face.jpg"
image = cv2.imread(image_path)

if image is None:
    raise SystemExit(f"Could not read image: {image_path}")

results = recognizer.recognize(image)

print(f"Faces detected: {len(results)}")

for index, result in enumerate(results, start=1):
    print(f"\nFace {index}")

    for key, value in result.items():
        print(f"  {key}: {value}")
