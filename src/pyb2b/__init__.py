from __future__ import annotations

import configparser
from pathlib import Path
from typing import Literal

from appdirs import user_config_dir

from .main import B2B

__all__ = ["b2b"]

b2b: B2B

config_dir = Path(user_config_dir("b2b"))
config_file = config_dir / "b2b.conf"

if not config_dir.exists():  # coverage: ignore
    config_template = """
[global]
pkcs12_filename =
pkcs12_password =
# mode =  # pick one of PREOPS (default) or OPS
# version =  # 26.0.0 (default)
    """
    config_dir.mkdir(parents=True)
    config_file.write_text(config_template)

config = configparser.ConfigParser()
config.read(config_file.as_posix())

http_proxy = config.get("network", "http.proxy", fallback="<>")
https_proxy = config.get("network", "https.proxy", fallback="<>")

pkcs12_filename = config.get("global", "pkcs12_filename", fallback="")
pkcs12_password = config.get("global", "pkcs12_password", fallback="")
b2b_mode: Literal["OPS", "PREOPS"]
b2b_mode = config.get("global", "mode", fallback="PREOPS")  # type: ignore
if b2b_mode not in ["OPS", "PREOPS"]:
    raise ImportError("mode must be one of OPS or PREOPS")
b2b_version = config.get("global", "version", fallback="26.0.0")

if pkcs12_filename != "" and pkcs12_password != "":
    b2b = B2B(b2b_mode, b2b_version, pkcs12_filename, pkcs12_password)
else:
    raise ImportError(f"Provide credentials in {config_file}")
