# Evidence: Hume→Gemini migration trail + Cloud Run hosting

**What this is:** a file-timestamp inventory (`ls -la`, read-only SSH) showing the bot line's real
migration history as dated backup snapshots, plus verbatim Dockerfile/deploy-command excerpts
showing both systems are actually hosted services, not scripts run by hand.

**Redactions:** file sizes/owner/group columns from `ls` are dropped as noise; no paths to audio,
no secret *values* (only Secret Manager *reference names*, which are not secrets themselves).

## Migration trail — dated backup filenames, `1st House - Fred Beta/`

Every backup filename is a working snapshot the operator kept deliberately, one per meaningful
swap — this is a lineage record, not a code mirror:

```
pipeline.py.bak                                                  (undated baseline)
pipeline.py.bak_phase2
pipeline.py.bak_20260528T153850Z_codex_gemini_35_migration
pipeline.py.bak_20260421_transcription_model
pipeline.py.bak_20260811T195218Z_flash_lite_swap
pipeline.py.bak_20260818T231342Z_faster_whisper_option
pipeline.py.bak_20260822T193655Z_gemini_37_flash_canon
pipeline.py.bak_20260822T200515Z_thinking_budget_zero
```

Reading the names in order: a transcription-model swap, a migration onto Gemini 3.5 (`codex_gemini_35_migration`),
a lighter-weight model swap (`flash_lite_swap`), an evaluation of a local Whisper variant
(`faster_whisper_option`), a canonicalization onto Gemini 3.7 Flash (`gemini_37_flash_canon`), and
a thinking-budget tuning pass (`thinking_budget_zero`) — five months of live iteration on the
transcription/generation stack that sits downstream of Fred's audio pipeline, each step preserved
rather than overwritten. This is the "later Gemini migration" referenced in the operator's lineage
record, sitting alongside (not replacing) the separate Hume→openSMILE migration on the *detector*
side (see [`../DECISIONS.md`](../DECISIONS.md) and root [`LINEAGE.md`](../../../LINEAGE.md) thread 3).

## Cloud Run hosting — bot line

`1st House - Fred/Dockerfile` (verbatim):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1 \
    FRED_AUDIO_ANALYSIS_PROVIDER=auto \
    FRED_ENABLE_HUME_FALLBACK=1 \
    FRED_GEMINI_TRANSCRIPTION_MODEL=gemini-2.0-flash \
    FRED_LOCAL_ANALYSIS_TIMEOUT_SECONDS=45 \
    FRED_LOCAL_ANALYSIS_EXECUTOR=bridge \
    FRED_VOICE_PIPELINE_CONCURRENCY=1 \
    FRED_AGENT_DISPATCH_CONCURRENCY=1
ENV PORT=8080
EXPOSE 8080
CMD ["python", "main.py"]
```

`FRED_ENABLE_HUME_FALLBACK=1` alongside a Gemini transcription model shows the bot's runtime is
already provider-flexible at the env-var level — a live seam, not a hard dependency, which is part
of why the Hume-era lineage could later carry a Gemini migration on the generation side without a
rewrite.

## Cloud Run hosting — detector-adjacent full pipeline (GPU service)

`1st House - Fred Beta/cloud_run/server.py`, module docstring (verbatim, deploy command included):

```python
"""Fred Beta — Cloud Run service.

Full pipeline: diarize + identify + prosody + transcribe.
Runs on L4 GPU for fast pyannote diarization.

Endpoints:
    POST /diarize     — diarization only (fast, returns segments)
    POST /analyze     — full pipeline (diarize + ID + prosody + transcribe)
    GET  /health      — health check

Deploy:
    gcloud run deploy fred-beta \
        --source=. \
        --gpu=1 --gpu-type=nvidia-l4 \
        --memory=16Gi --cpu=8 \
        --min-instances=0 --max-instances=2 \
        --timeout=600 \
        --region=us-central1 \
        --set-secrets=HF_TOKEN=hf-token:latest,GEMINI_API_KEY=gemini-api-key:latest
"""
```

Matching Dockerfile is CUDA-based (`nvidia/cuda:12.1.1-runtime-ubuntu22.04`), `min-instances=0`
(scales to zero — this is why "dormant" is an accurate word, not a euphemism: nothing is running
or billing between invocations). Secret values are referenced by Secret Manager name
(`hf-token:latest`, `gemini-api-key:latest`) — no key material appears in the deploy command or
anywhere in this evidence set.
