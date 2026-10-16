import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
os.environ.setdefault("DATABASE_URL", "sqlite://")  # engine is created at import; no real DB needed
for p in (ROOT.parent / "ClearOps_App", ROOT / "services", ROOT / "services" / "gateway"):
    sys.path.insert(0, str(p))
