# Consseau Public Speaking Assistant

Mobile pronunciation practice for Mia and Amy. The names and practice lists are public, with the project owner's explicit approval. Tabs select lists, not authenticated accounts. No analytics or recording uploads.

Website: https://percivalbeep.github.io/consseau-public-speaking-assistant/

Direct links: `?student=mia` and `?student=amy`.

Mia's original five word groups are retained. All eleven word groups use the SAME prerecorded US English synthetic voice (Kokoro af_heart). There are no checkmarks, recording uploads or practice counters. Word audio uses native Kokoro speeds 0.65 and 0.5; no post-synthesis time stretching. Audio requires a tap. WeChat playback depends on client and network; a browser-opening fallback is included.

Edit index.html to maintain lists and add MP3 files to assets/audio. students.json is a reference copy of the word data. GitHub Actions deploys main to Pages. Temporary voice files and build helpers are excluded from Git.

Pronunciation reference: https://dictionary.cambridge.org/us/pronunciation/english/fortunate and https://dictionary.cambridge.org/pronunciation/ . IPA and reminders are coaching aids; speech is synthetic, not a human teacher's recording.

## Local teacher studio

On this Mac, run `python3 tools/teacher_server.py` and open http://127.0.0.1:8766/teacher . Requires the isolated `.work/tts-venv` environment, Kokoro model/voices under `.work/kokoro/`, FFmpeg/ffprobe, and authenticated GitHub CLI for publishing. These are installed on the coach's Mac. No paid TTS API is called. The server only binds localhost and requires a per-launch request token for generation and publication. It does not enable cross-origin requests.

Paste text or import DOCX/UTF-8 TXT. Check the English body before generating. Choose a slow, moderate or faster native synthesis preset; labels do not promise exact words per minute. Sentence and paragraph pauses increase in slower presets. Preview and download the normal MP3 or independently synthesized slower version. The teacher must review prosody: synthetic speech cannot guarantee performance-level stress and emotion.

Generation keeps the manuscript and outputs in ignored `.work/studio/`. Only after clicking the explicit public-publication button are the reviewed MP3s and title committed to the public repository and listed on the selected student's page. Manuscript text is not published by this workflow. GitHub Pages cannot run this local voice service. The publicly hosted teacher.html provides setup instructions instead of a working public generation endpoint.

## Local voice engine

Kokoro-82M uses Apache-2.0 model weights; kokoro-onnx is an MIT-licensed runner. Sources: https://huggingface.co/hexgrad/Kokoro-82M and https://github.com/thewh1teagle/kokoro-onnx . All synthesis is local, with no per-character API charges. The model and Python environment are excluded from the repository.

To rebuild locally, create a Python 3.12 virtual environment at `.work/tts-venv`, install `tools/requirements-tts.txt`, and download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from the runner's official `model-files-v1.1` release into `.work/kokoro/model.onnx` and `.work/kokoro/voices.bin`. SHA256 values: model `beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a`; voices `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`.

Blamed is synthesized as three repetitions with explicit phonemes, then the middle repetition is extracted at the surrounding silence boundaries to avoid a spurious leading vowel in isolated generation. Both speeds are generated independently.
