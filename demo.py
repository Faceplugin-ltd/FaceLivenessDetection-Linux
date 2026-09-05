"""Gradio demo — Face Liveness (local only; not shipped in Docker)."""

from __future__ import annotations

import base64
import os
from pathlib import Path

import gradio as gr
import requests

ROOT = Path(__file__).resolve().parent
SAMPLES = ROOT / "assets" / "examples" / "samples"
API = os.environ.get("API_BASE", "http://127.0.0.1:8084").rstrip("/")
DEMO_PORT = int(os.environ.get("DEMO_PORT", "9004"))
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def _b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def _examples() -> list[str]:
    if not SAMPLES.is_dir():
        return []
    return sorted(
        str(p)
        for p in SAMPLES.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def check_image(path):
    if not path:
        return "**Error:** Image required"
    try:
        r = requests.post(f"{API}/api/liveness", json={"image": _b64(path)}, timeout=180)
        payload = r.json()
    except Exception as ex:  # noqa: BLE001
        return f"**Error:** {ex}"
    if not isinstance(payload, dict) or not payload.get("success"):
        msg = payload.get("message") if isinstance(payload, dict) else payload
        return f"**Error:** {msg}"
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    result = data.get("result", "—")
    score = data.get("score", "—")
    passed = data.get("pass")
    pass_s = "true" if passed is True else "false" if passed is False else "—"
    return f"## {result}\n\n**Score:** {score}\n\n**Pass:** {pass_s}"


with gr.Blocks(title="Face Liveness Demo") as demo:
    gr.Markdown(
        "# FacePlugin Face Liveness — Demo\n"
        "Upload a face photo (webcam capture is on the image picker)."
    )
    with gr.Row():
        with gr.Column():
            img = gr.Image(type="filepath", label="Face")
            examples = _examples()
            if examples:
                gr.Examples(examples, inputs=img, label="Examples")
            btn = gr.Button("Check liveness", variant="primary")
        with gr.Column():
            summary = gr.Markdown(value="*Run an action to see the result.*")
    btn.click(check_image, inputs=[img], outputs=[summary])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=DEMO_PORT)
