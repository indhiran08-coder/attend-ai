import cv2
import torch
import time
from ultralytics import YOLO

MODEL_PATH = "yolov8n.pt"
CAMERA = "/dev/video0"
IMAGE_SIZE = 320
CONFIDENCE = 0.40


def main():
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable!")

    print("GPU:", torch.cuda.get_device_name(0))
    print("Loading YOLOv8 Nano...")

    model = YOLO(MODEL_PATH)

    cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

    if not cap.isOpened():
        raise RuntimeError(
            f"Cannot open {CAMERA}. Check the webcam connection."
        )

    cap.set(
        cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*"MJPG")
    )
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    fps = 0.0
    previous_time = time.perf_counter()

    print("ByteTrack started. Press Q to quit.")

    try:
        while True:
            success, frame = cap.read()

            if not success:
                print("Could not read camera frame.")
                break

            # Track people across consecutive frames
            result = model.track(
                source=frame,
                persist=True,
                tracker="bytetrack.yaml",
                device=0,
                classes=[0],
                imgsz=IMAGE_SIZE,
                conf=CONFIDENCE,
                verbose=False
            )[0]

            annotated = result.plot()

            # Calculate approximate processing FPS
            now = time.perf_counter()
            elapsed = now - previous_time
            previous_time = now

            if elapsed > 0:
                current_fps = 1.0 / elapsed
                fps = current_fps if fps == 0 else (
                    0.8 * fps + 0.2 * current_fps
                )

            # Display tracking IDs
            if result.boxes is not None and result.boxes.id is not None:
                track_ids = result.boxes.id.int().cpu().tolist()
                person_count = len(track_ids)
                ids_text = ", ".join(map(str, track_ids))
            else:
                person_count = 0
                ids_text = "None"

            cv2.putText(
                annotated,
                f"People: {person_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated,
                f"Processing FPS: {fps:.1f}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated,
                f"Track IDs: {ids_text[:70]}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            cv2.imshow("AttendAI - YOLO + ByteTrack", annotated)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nStopping tracker...")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam released.")


if __name__ == "__main__":
    main()
