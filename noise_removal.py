import subprocess
import os

def remove_noise_from_video(input_video, output_video):
    """Removes background noise from a video using FFmpeg and SoX."""

    # 1. Extract Audio
    audio_file = "temp_audio.wav"
    subprocess.run(['ffmpeg', '-i', input_video, '-vn', '-acodec', 'pcm_s16le', audio_file], check=True)

    # 2. Create Noise Profile
    noise_profile = "noise_profile.prof"
    subprocess.run(['sox', audio_file, '-n', 'trim', '0', '0.5', 'noiseprof', noise_profile], check=True)

    # 3. Reduce Noise
    cleaned_audio = "cleaned_audio.wav"
    subprocess.run(['sox', audio_file, cleaned_audio, 'noisered', noise_profile, '0.21'], check=True)

    # 4. Reintegrate Clean Audio
    subprocess.run(['ffmpeg', '-i', input_video, '-i', cleaned_audio, '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_video], check=True)

    # Clean up temporary files
    os.remove(audio_file)
    os.remove(noise_profile)
    os.remove(cleaned_audio)

if __name__ == "__main__":
    input_video = "input_video.mp4"  # Replace with your input video file
    output_video = "output_video.mp4"  # Replace with your desired output video file
    remove_noise_from_video(input_video, output_video)
    print(f"Cleaned video saved as {output_video}")