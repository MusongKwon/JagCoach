# JagCoach
JagCoach is an AI-assisted coaching platform for oral presentations (made by Musong Kwon, Caleb Holt, Jesus Lopez, Reyden Rodriguez, Talia Ortiz, and Syrus Redhouse).  This application was made for students who hope to improve their class presentations and develop stronger public speaking skills.


## Approach

The presentation evaluation is done by the Meta Llama 3.2.  After being uploaded, the video file is converted to a .wav file.  Using the open-source Python "my-voice-analysis" module and the "openai-whisper" module, the student's speech is analyzed and transcribed.  This data is given to the LLM, compared to a benchmark, and evaluated to provide feedback and a grade to the student.

## Setup
We used Python 3.12 and various Python packages, most notably [Open-AI's Whisper](https://github.com/openai/whisper) for transcription and an open-source library named [my-voice-analysis] from Shahabks on GitHub (https://github.com/Shahabks/my-voice-analysis) for speech analysis. You can install JagCoach's dependencies using the commands below.  Be sure to run these commands as an administrator:

For the web framework, install the flask module:
```sh
pip install flask
```

You'll first need to install choco to install ffmpeg:
```sh
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

If you don't see any errors, install ffmpeg:
```sh
choco install ffmpeg
```

For .wav conversion and sound configuration, install audio_extract and pydub:
```sh
pip install pydub
pip install audio_extract
```

For the speech analysis, you will need my-voice-analysis
```sh
pip install my-voice-analysis
```

For transcription, install openai-whisper:
```sh
pip install -U openai-whisper
```

Run the following command to update it to the lastest version from the GitHub repo:
```sh
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```
Lastly, you will need to download the Ollama LLM from the website (https://ollama.com/download), and install its Python package:
```sh
pip install ollama
```

Alternatively, you can run the following Linux command to download the LLM:
```sh
curl -fsSL https://ollama.com/install.sh | sh
```
Once these dependencies are installed, you can download JagCoach from the GitHub Repository (https://github.com/MusongKwon/JagCoach) and run it in an IDE or use the commands below:

```sh
git clone https://github.com/MusongKwon/JagCoach.git
cd JagCoach
python3 app.py
```
Note: Ollama should be running in the background as JagCoach is running.

## Example usage

Below is an example of JagCoach being used to grade a student's presentation.
Click the IP address:
![image](https://github.com/user-attachments/assets/a344ca01-c0f8-41bf-a8fa-81239c54c6f6)

This page should appear:
![image](https://github.com/user-attachments/assets/05615bb4-26fd-4426-86b2-9d6aeebde3ec)

Choose a video file to upload:
![chrome_qpbGKbNd0V](https://github.com/user-attachments/assets/9916de43-82b9-42d3-83dc-1d18e79083ba)

After selecting a video, the transcription and presentation evaluation will begin:
![image](https://github.com/user-attachments/assets/439eb2a2-8965-40b5-b85a-33f3d5066d88)

The evalution and transcription should appear in their respective text boxes after they finish:
![image](https://github.com/user-attachments/assets/01be7191-4344-44d9-814d-31d409b9a85d)




