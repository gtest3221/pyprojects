from moviepy.editor import VideoFileClip
import speech_recognition as sr
from googletrans import Translator

def translate_video(video_path, output_audio_path="extracted_audio.wav", output_text_file="translated_text.txt"):
    # 1. Extract Audio
    print("Extracting audio...")
    extract_audio(video_path, output_audio_path)
    print("Audio extracted.")

    # 2. Transcribe Audio (Hindi)
    print("Transcribing audio...")
    hindi_text = transcribe_audio(output_audio_path, language="hi-IN")
    print(f"Transcription (Hindi): {hindi_text}")

    # 3. Translate Text (Hindi to English)
    print("Translating text...")
    english_text = translate_text(hindi_text, src_lang="hi", dest_lang="en")
    print(f"Translation (English): {english_text}")

    # Save translated text to a file
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(english_text)
    print(f"Translated text saved to {output_text_file}")

# Helper functions (as defined above)
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio(audio_path, language="hi-IN"):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from service; {e}"

def translate_text(text, src_lang="hi", dest_lang="en"):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    return translated_text

if __name__ == "__main__":
    video_file = "your_hindi_video.mp4"  # Replace with your video file
    translate_video(video_file)