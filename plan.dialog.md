# Plan: Transform `dialog.py` into a Google Generative AI interactive app

## Goal

Provide a minimal, secure, testable CLI app that lets a user interact with Google's Generative AI (Gemini/PaLM) from `dialog.py`.

## Scope

- Use the `google-genai` Python client (Gemini model).  
- Preferred auth: `GOOGLE_API_KEY` for quick testing; support ADC via `GOOGLE_APPLICATION_CREDENTIALS`.  
- Deliverables: interactive CLI, client wrapper, env example, requirements update, tests, README updates.

## Assumptions

- The workspace will run under a Python venv.  
- The `google-genai` package exposes `google.genai` as in existing `google-genai.py`.  
- The user will provide either an API key or ADC service account file.

## Files to add / modify

- Add: `google_client.py` — thin wrapper for auth and chat creation.  (done)  
- Add: `.env.example` — template for credentials. (done)  
- Modify: `dialog.py` — interactive CLI using the wrapper. (done)  
- Update: `requirements.txt` — ensure `google-genai`, `python-dotenv`, and `requests` present.  
- Add: `plan.dialog.md` — this file.  
- Add (optional): `tests/test_google_client.py` and `tests/test_dialog.py` for unit/integration tests.

## Implementation steps (detailed)

1. Environment & deps
   - Add or update `requirements.txt` with `google-genai`, `python-dotenv`, and pinned packages if desired.
   - Create `.env.example` and instruct user to copy to `.env`.

2. Client wrapper
   - Implement `google_client.create_client()` that prefer `GOOGLE_API_KEY` or falls back to ADC.
   - Implement `create_chat()` and `send_message_stream()` helpers that centralize model/config.

3. Interactive dialog
   - Make `dialog.py` import the wrapper and provide a prompt loop with clean exit (`quit`).
   - Stream responses to the terminal and handle chunk shapes safely (use `getattr(chunk, 'text', str(chunk))`).

4. Error handling & logging
   - Wrap network calls with try/except for `RuntimeError`, `ConnectionError`, and `TimeoutError`.
   - Provide user-friendly messages when credentials are missing or the package isn't installed.

5. Tests
   - Unit: mock `genai.Client` to verify wrapper behavior and chat creation.
   - Integration (manual): run `python dialog.py` with a valid key and ensure conversation flows.

6. Documentation
   - Update `README.md` with setup steps (venv, pip install, `.env`), run command, and security notes.

7. Security review
   - Add `.env` to `.gitignore` if not present.  
   - Document never committing credentials, and recommend using secret managers for production.

## Run / Test commands

1. Create and activate venv (Windows example):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install deps:

```bash
pip install -r requirements.txt
```

3. Copy credentials and run:

```bash
copy .env.example .env
# edit .env to set GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS
python dialog.py
```

## Next actions (recommended)

- Update `requirements.txt` to pin `google-genai` and `python-dotenv`.  
- Add basic exception handling and minimal logging in `google_client.py` and `dialog.py`.  
- Add tests under `tests/` and CI job to run them.

---
This plan file documents the concrete steps and artifacts. Tell me if you want me to update `requirements.txt` and add error handling now, and I'll proceed.
