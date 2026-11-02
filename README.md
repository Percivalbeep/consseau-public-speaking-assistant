# Consseau Public Speaking Assistant

Mobile pronunciation practice for Mia and Amy. The names and practice lists are public, with the project owner's explicit approval. Tabs select lists, not authenticated accounts. Practice checkmarks stay in the current browser only. No analytics or recording uploads.

Website: https://percivalbeep.github.io/consseau-public-speaking-assistant/

Direct links: `?student=mia` and `?student=amy`.

Mia's five groups and ten audio files are retained from the original supplied HTML. Amy's six groups use prerecorded US English synthetic speech (Samantha). Slow audio uses FFmpeg atempo=0.7 to preserve pitch. Audio requires a tap. WeChat playback depends on client and network; a browser-opening fallback is included.

Edit index.html to maintain lists and add MP3 files to assets/audio. students.json is a reference copy of the word data. GitHub Actions deploys main to Pages. Temporary voice files and build helpers are excluded from Git.

Pronunciation reference: https://dictionary.cambridge.org/us/pronunciation/english/fortunate and https://dictionary.cambridge.org/pronunciation/ . IPA and reminders are coaching aids; speech is synthetic, not a human teacher's recording.
