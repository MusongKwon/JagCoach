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
This program also analyzes the presenter visually using the DeepFace module.  For this, you will need to run the command below for the DeepFace module and its dependencies:
```sh
pip install opencv-python dlib numpy mediapipe deepface tf-keras
```

You will also need to install CMake on your device.  You can download that here: https://cmake.org/download/
 
If you are on Windows you will also need the Visual Studio C++ build tool (2019 or later) on your device.  You can install that here: https://visualstudio.microsoft.com/visual-cpp-build-tools/


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

Below is what this branch currently looks like - Redhouse:
<img width="1512" alt="Screenshot 2025-04-10 at 4 40 02 PM" src="https://github.com/user-attachments/assets/46e2f6db-b66e-4b58-bddf-685097b20245" />

SECOND UPDATE THIS IS THE USER PROFILE (Mock data for visuals):
![image](https://github.com/user-attachments/assets/47a06697-31ab-4d00-a830-3c3959e0b0ec)

