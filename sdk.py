"""ctypes bindings to libFaceLivenessSDK.so (Face Liveness).

Native libs live in lib/cpu/.
"""

from __future__ import annotations

import base64
import ctypes
import io
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "lib" / "cpu"
SO = LIB / "libFaceLivenessSDK.so"

os.chdir(ROOT)
os.environ["LD_LIBRARY_PATH"] = str(LIB) + (
    (":" + os.environ["LD_LIBRARY_PATH"]) if os.environ.get("LD_LIBRARY_PATH") else ""
)

if not SO.is_file():
    raise FileNotFoundError(
        f"missing {SO} — put Drive files in lib/cpu/ "
        "(export copies SDK lib/ → App lib/cpu/)"
    )

_dll = ctypes.CDLL(str(SO), mode=os.RTLD_GLOBAL)

_dll.FaceSDK_initSDK.restype = ctypes.c_int
_dll.FaceSDK_initSDK.argtypes = []
_dll.FaceSDK_activate.restype = ctypes.c_int
_dll.FaceSDK_activate.argtypes = [ctypes.c_char_p]
_dll.FaceSDK_getMachineCode.restype = ctypes.c_int
_dll.FaceSDK_getMachineCode.argtypes = [ctypes.c_char_p]
_dll.FaceSDK_liveness_all.restype = ctypes.c_int
_dll.FaceSDK_liveness_all.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

_MC_BUF = 768
_OUT = 2 * 1024 * 1024
_MAX_IMG = 8 * 1024 * 1024


def _b(v) -> bytes:
    if isinstance(v, bytes):
        return v
    return str(v).encode("utf-8")


def _jpeg_bytes(image_b64: str) -> bytes:
    text = image_b64.strip()
    if text.startswith("data:") and "base64," in text:
        text = text.split("base64,", 1)[1]
    data = base64.b64decode(text, validate=False)
    if len(data) <= _MAX_IMG and data[:2] == b"\xff\xd8":
        return data
    from PIL import Image

    img = Image.open(io.BytesIO(data))
    img.load()
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    out = buf.getvalue()
    while len(out) > _MAX_IMG and img.width > 32:
        img = img.resize((max(1, int(img.width * 0.75)), max(1, int(img.height * 0.75))))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        out = buf.getvalue()
    return out


def get_machine_code() -> str:
    buf = ctypes.create_string_buffer(_MC_BUF)
    _dll.FaceSDK_getMachineCode(buf)
    return buf.value.decode("utf-8", errors="replace")


def activate(license_path: str) -> int:
    return int(_dll.FaceSDK_activate(_b(license_path)))


def init_sdk() -> int:
    return int(_dll.FaceSDK_initSDK())


def liveness(image: str) -> str:
    jpeg = _jpeg_bytes(image)
    out = ctypes.create_string_buffer(_OUT)
    _dll.FaceSDK_liveness_all(jpeg, len(jpeg), out)
    return out.value.decode("utf-8", errors="replace")
