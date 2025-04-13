import cv2
import os
from natsort import natsorted
from tqdm import tqdm

def stitch_frames_to_video(output_folder, output_video_path, fps=30):
    # Get list of all image files in the folder, naturally sorted
    frames = [f for f in os.listdir(output_folder) if f.endswith(('.jpg', '.png'))]
    frames = natsorted(frames)  # Natural sort to keep frame order like frame_0001, frame_0002, ...

    if not frames:
        print("❌ No frames found in the folder.")
        return

    # Read the first frame to get dimensions
    first_frame = cv2.imread(os.path.join(output_folder, frames[0]))
    height, width, _ = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use 'XVID'
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Use tqdm for progress bar
    with tqdm(total=len(frames), desc="Stitching frames", unit="frame") as pbar:
        for frame_name in frames:
            frame_path = os.path.join(output_folder, frame_name)
            frame = cv2.imread(frame_path)
            if frame is not None:
                out.write(frame)

            pbar.update(1)  # Update progress bar for each frame processed

    out.release()
    print(f"✅ Video saved to {output_video_path}")

# Example usage
stitch_frames_to_video("frames", "stitched_video.mp4", fps=30)
