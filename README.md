# Consseau Public Speaking Assistant

Mobile pronunciation practice for Mia and Amy. The names and practice lists are public, with the project owner's explicit approval. Tabs select lists, not authenticated accounts. No analytics or recording uploads.

Website: https://percivalbeep.github.io/consseau-public-speaking-assistant/

Direct links: `?student=mia` and `?student=amy`.

Mia's original five word groups are retained. All eleven word groups use the SAME prerecorded US English synthetic voice (Samantha, 155 words/minute). There are no checkmarks, recording uploads or practice counters. Slow audio uses FFmpeg atempo=0.7 to preserve pitch. Audio requires a tap. WeChat playback depends on client and network; a browser-opening fallback is included.

Edit index.html to maintain lists and add MP3 files to assets/audio. students.json is a reference copy of the word data. GitHub Actions deploys main to Pages. Temporary voice files and build helpers are excluded from Git.

Pronunciation reference: https://dictionary.cambridge.org/us/pronunciation/english/fortunate and https://dictionary.cambridge.org/pronunciation/ . IPA and reminders are coaching aids; speech is synthetic, not a human teacher's recording.

## Local teacher studio

On this Mac, run `python3 tools/teacher_server.py` and open http://127.0.0.1:8766/teacher . Requires macOS Samantha voice, FFmpeg/ffprobe, and authenticated GitHub CLI for publishing. These are already present on the coach's Mac. No paid TTS API is called. The server only binds localhost and requires a per-launch request token for generation and publication. It does not enable cross-origin requests.

Paste text or import DOCX/UTF-8 TXT. Check the English body before generating. Choose 110, 135, or 155 words per minute. Blank paragraphs add a short pause. Preview and download the normal MP3 or pitch-preserving 0.85× version. The teacher must review prosody: system speech cannot guarantee performance-level stress and emotion.

Generation keeps the manuscript and outputs in ignored `.work/studio/`. Only after clicking the explicit public-publication button are the reviewed MP3s and title committed to the public repository and listed on the selected student's page. Manuscript text is not published by this workflow. GitHub Pages cannot run this local voice service. The publicly hosted teacher.html provides setup instructions instead of a working public generation endpoint.
