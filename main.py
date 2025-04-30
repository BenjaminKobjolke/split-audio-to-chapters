import os
import re
import subprocess
from datetime import timedelta
import shutil

def parse_chapters(text_file_path):
    """Parses the chapter definition text file."""
    chapters = []
    with open(text_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.match(r'(\d{2}:\d{2}:\d{2}) - (.*)', line)
            if match:
                timestamp_str, chapter_name = match.groups()
                h, m, s = map(int, timestamp_str.split(':'))
                timestamp = timedelta(hours=h, minutes=m, seconds=s)
                chapters.append({'timestamp': timestamp, 'name': chapter_name.strip()})
            else:
                print(f"Warning: Skipping invalid line in {text_file_path}: {line}")
    # Sort chapters by timestamp
    chapters.sort(key=lambda x: x['timestamp'])
    return chapters

def sanitize_filename(name):
    """Sanitizes a string to be safe for use as a filename."""
    # Replace problematic characters with hyphen and space
    print(f"Original name: {name}")
    name = name.replace(':', ' -')
    name = re.sub(r'[–—−]', '-', name)    
    # Remove characters invalid in Windows filenames
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    print(f"Sanitized filename: {name}")
    return name

def split_audio(audio_file_path, chapters, output_dir):
    """Splits the audio file into chapters using ffmpeg."""
    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    base_output_dir = output_dir # output/basefilename
    parts_dir = os.path.join(base_output_dir, 'parts')
    os.makedirs(parts_dir, exist_ok=True)

    # Handle segments between chapter timestamps (from chapter i start to chapter i+1 start - 1 second)
    for i in range(len(chapters) - 1):
        start_time = chapters[i]['timestamp']
        end_time = chapters[i+1]['timestamp'] - timedelta(seconds=1)
        chapter_name = chapters[i]['name'] # Name of the starting chapter for the segment
        sanitized_chapter_name = sanitize_filename(chapter_name)
        chapter_number = str(i + 1).zfill(2)

        output_filename = f"{base_name} - {chapter_number} - {sanitized_chapter_name}.mp3"
        output_path = os.path.join(parts_dir, output_filename) # Save in parts directory

        command = [
            'ffmpeg',
            '-i', audio_file_path,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c:a', 'libmp3lame',
            output_path
        ]

        print(f"Splitting segment from {start_time} to {end_time}")

        try:
            subprocess.run(command, check=True, capture_output=True)
            print(f"Created chapter: {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error splitting chapter {output_filename}: {e}")
            print(f"ffmpeg stderr: {e.stderr.decode()}")

    # Handle the last segment (from the last chapter's timestamp to the end)
    if chapters: # Check if there's at least one chapter
        last_segment_start_time = chapters[-1]['timestamp']
        last_chapter_name = chapters[-1]['name'] # Using the name of the last defined chapter
        sanitized_last_chapter_name = sanitize_filename(last_chapter_name)
        last_chapter_number = str(len(chapters)).zfill(2) # Number of the last defined chapter

        last_output_filename = f"{base_name} - {last_chapter_number} - {sanitized_last_chapter_name}.mp3"
        last_output_path = os.path.join(parts_dir, last_output_filename) # Save in parts directory

        command = [
            'ffmpeg',
            '-i', audio_file_path,
            '-ss', str(last_segment_start_time),
            '-c:a', 'libmp3lame',
            last_output_path
        ]
        print(f"Splitting last segment from {last_segment_start_time} to end")
        try:
            subprocess.run(command, check=True, capture_output=True)
            print(f"Created last segment: {last_output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error splitting last segment {last_output_filename}: {e}")
            print(f"ffmpeg stderr: {e.stderr.decode()}")


def main():
    input_dir = 'input'
    output_base_dir = 'output'

    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return

    for filename in os.listdir(input_dir):
        name, ext = os.path.splitext(filename)
        if ext.lower() in ['.mp3']: # Add other audio extensions if needed
            audio_file_path = os.path.join(input_dir, filename)
            text_file_path = os.path.join(input_dir, f"{name}.txt")

            if os.path.exists(text_file_path):
                print(f"Processing {filename}...")
                chapters = parse_chapters(text_file_path)
                if chapters:
                    output_dir = os.path.join(output_base_dir, name)
                    split_audio(audio_file_path, chapters, output_dir)

                    # Move original input file to 'complete' subdirectory
                    complete_dir = os.path.join(output_dir, 'complete')
                    os.makedirs(complete_dir, exist_ok=True)
                    original_filename = os.path.basename(audio_file_path)
                    destination_path = os.path.join(complete_dir, original_filename)
                    try:
                        shutil.move(audio_file_path, destination_path)
                        print(f"Moved original file to {destination_path}")
                    except Exception as e:
                        print(f"Error moving original file {audio_file_path} to {destination_path}: {e}")

                    # Move original input text file to 'complete' subdirectory
                    original_text_filename = os.path.basename(text_file_path)
                    destination_text_path = os.path.join(complete_dir, original_text_filename)
                    try:
                        shutil.move(text_file_path, destination_text_path)
                        print(f"Moved original text file to {destination_text_path}")
                    except Exception as e:
                        print(f"Error moving original text file {text_file_path} to {destination_text_path}: {e}")

                else:
                    print(f"No valid chapters found in {name}.txt")
            else:
                print(f"No corresponding text file found for {filename}")

if __name__ == "__main__":
    main()
