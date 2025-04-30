# Audio Chapter Splitter

This tool is a Python script that splits audio files into chapters based on timestamps and names provided in a corresponding text file.

## Purpose

The script automates the process of dividing a single audio file (like an audiobook) into smaller files, with each file representing a chapter or segment defined in a simple text file.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd split-audio-to-chapters
    ```

    (Replace `<repository_url>` with the actual URL of the repository if applicable.)

2.  **Install Python Dependencies:**
    This project uses a Python virtual environment to manage dependencies.
    Run the provided batch script to set up the environment and install the necessary Python libraries:

    ```bash
    install.bat
    ```

    This will create a `venv` directory and install `ffmpeg-python`.

3.  **Install FFmpeg:**
    This script relies on the `ffmpeg` command-line tool for audio processing. You need to download and install `ffmpeg` separately and ensure it is added to your system's PATH.
    You can download `ffmpeg` from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html). Follow the instructions for your operating system to add the `ffmpeg` executable to your PATH.

## Usage

1.  **Place Input Files:**
    Put your audio files (e.g., `.mp3`) and their corresponding text files in the `input` directory.
    Ensure that for each audio file (`your_audio.mp3`), there is a text file with the same base name (`your_audio.txt`) in the same `input` directory.

2.  **Text File Format:**
    The text file should contain chapter definitions, with each line specifying a timestamp and the chapter name, in the following format:

    ```
    HH:MM:SS - Chapter Name
    ```

    Timestamps should be in chronological order. The first timestamp should ideally be `00:00:00` if you want the first segment to start from the beginning of the audio.

    See `input_example/example.txt` for an example.

3.  **Run the Script:**
    Open your terminal or command prompt in the project's root directory (`split-audio-to-chapters`) and run the following command:

    ```bash
    call activate_environment.bat && python main.py
    ```

    This will activate the Python virtual environment and run the script.

4.  **Output:**
    The script will process the files in the `input` directory. For each audio/text file pair, it will create a subdirectory in the `output` directory with the same base name as the audio file.
    Inside this subdirectory, you will find:
    -   A `complete` subdirectory containing the original input audio file.
    -   A `parts` subdirectory containing the generated audio files for each chapter.
