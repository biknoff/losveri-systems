#!/usr/bin/env python3
# Excerpt from tools/abraxas_tts.py — the chunked Gemini TTS pipeline that
# renders ABRAXAS's spoken replies. Redactions: none (no keys inline —
# get_api_key() reads from env or an untracked api.info file, not shown here).

VOICE = "Leda"          # ABRAXAS's voice; Kubera uses "Achernar" (en-US)
LANG = "en-GB"
MODEL = "gemini-3.1-flash-tts-preview"
MAX_BYTES = 3800         # stay under the API's 4000-byte request limit
SILENCE_SEC = 0.8        # pause inserted between chunk boundaries
SAMPLE_RATE = 24000

async def generate_audio(text, mp3_path):
    from google import genai
    from google.genai import types

    client = genai.Client()  # GOOGLE_API_KEY resolved via get_api_key()

    voice_config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE)
            ),
            language_code=LANG,
        ),
    )

    # Long scripts are split on "...\n" section breaks first, then by
    # sentence, keeping every chunk under the API's byte limit.
    chunks = chunk_text(text)

    silence = b'\x00\x00' * int(SAMPLE_RATE * SILENCE_SEC)
    all_audio = bytearray()

    for i, chunk in enumerate(chunks):
        for attempt in range(3):
            try:
                response = await client.aio.models.generate_content(
                    model=MODEL, contents=chunk, config=voice_config,
                )
                data = response.candidates[0].content.parts[0].inline_data.data
                all_audio.extend(data)
                if i < len(chunks) - 1:
                    all_audio.extend(silence)   # stitch chunks with a pause
                break
            except Exception:
                if attempt < 2:
                    time.sleep(2)     # retry transient API failures
                else:
                    raise

    # Raw PCM -> WAV -> MP3 via ffmpeg; WAV is a scratch file, discarded.
    wav_path = mp3_path.replace(".mp3", ".wav")
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SAMPLE_RATE)
        wf.writeframes(bytes(all_audio))
    subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-b:a", "192k", mp3_path],
                    capture_output=True, check=True)
    os.remove(wav_path)
    return mp3_path

# Downstream: tools/send_channel_agent_response.py -> send_telegram_voice()
# posts the rendered mp3/ogg to Telegram's `sendVoice` endpoint, delivering
# the reply as a voice note back to the family — closing voice-in -> voice-out.
