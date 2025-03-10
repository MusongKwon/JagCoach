# JagCoach
JagCoach is an AI-Assisted coaching platform for oral presentations made by Musong, Caleb, Jesus, Talia, and Redhouse.


## Approach

The presentation evaluation is done by the Meta Llama 3.2.  After being uploaded, the video file is converted to a .wav file.  Using the open-source Python "my-voice-analysis" module and the "openai-whisper" module, the student's speech is analyzed and transcribed.  This data is given to the LLM, compared to a benchmark, and evaluated to provide a feedback and a grade to the student.

## Setup
We used Python 3.12 and various Python packages, most notably [Open-AI's Whisper](https://github.com/openai/whisper) for transciption and an open-source library named [my-voice-analysis] from Shahabks on GitHub (https://github.com/Shahabks/my-voice-analysis) for speech analysis. You can install JagCoach's dependacies using the commands below:

For the web framework, install the flask module:
```sh
pip install flask
```

For .wav conversion and sound configuration, install audio_extract and pydub:

```sh
pip install pydub
pip install audio_extract
```
You will likely need to install setup-tools: 
```sh
pip install setuptools
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
Once these dependancies are installed, you can download JagCoach from the GitHub Repository (https://github.com/MusongKwon/JagCoach) and run it in an IDE or use the commands below:

```sh
git clone https://github.com/MusongKwon/JagCoach.git
cd JagCoach
python3 app.py
```

## Example usage

Below is an example of JagCoach being used to grade a students presentation.
