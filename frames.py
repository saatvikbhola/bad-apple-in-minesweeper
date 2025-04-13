import cv2
import os
from tqdm import tqdm

def extract_frames(video_path, output_folder, frame_rate=1):
    os.makedirs(output_folder, exist_ok=True)

    # Load video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error: couldn't open file")
        return

    frame_count = 0
    saved_count = 0
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video

    # Use tqdm for progress bar
    with tqdm(total=total_frames, desc="Extracting frames", unit="frame") as pbar:
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Extract frames based on frame rate
            if int(frame_count % (fps // frame_rate)) == 0:
                frame_filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_count += 1

            frame_count += 1
            pbar.update(1)  # Update progress bar for each frame processed

    video.release()
    print(f"Extracted {saved_count} frames to {output_folder}")

# Example usage: Extract 1 frame per second
extract_frames("video.mp4", "frames", frame_rate=30)  # Adjust frame_rate as needed
