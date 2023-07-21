from __future__ import annotations

import configparser
from pathlib import Path

import requests
from appdirs import user_config_dir

from .main import B2B

__all__ = ["b2b"]

b2b: None | B2B = None

config_dir = Path(user_config_dir("traffic"))
config_file = config_dir / "traffic.conf"

if not config_dir.exists():  # coverage: ignore
    config_template = (Path(__file__).parent / "traffic.conf").read_text()
    config_dir.mkdir(parents=True)
    config_file.write_text(config_template)

config = configparser.ConfigParser()
config.read(config_file.as_posix())

session = requests.Session()

http_proxy = config.get("network", "http.proxy", fallback="<>")
https_proxy = config.get("network", "https.proxy", fallback="<>")
paramiko_proxy = config.get("network", "ssh.proxycommand", fallback="")

proxy_values = dict(
    (key, value)
    for key, value in [("http", http_proxy), ("https", https_proxy)]
    if value != "<>"
)

if len(proxy_values) > 0:
    session.proxies.update(proxy_values)
    session.trust_env = False

pkcs12_filename = config.get("nmb2b", "pkcs12_filename", fallback="")
pkcs12_password = config.get("nmb2b", "pkcs12_password", fallback="")
nmb2b_mode = config.get("nmb2b", "mode", fallback="PREOPS")
if nmb2b_mode not in ["OPS", "PREOPS"]:
    raise RuntimeError("mode must be one of OPS or PREOPS")
nmb2b_version = config.get("nmb2b", "version", fallback="26.0.0")

if pkcs12_filename != "" and pkcs12_password != "":
    b2b = B2B(
        getattr(B2B, nmb2b_mode),
        nmb2b_version,
        session,
        pkcs12_filename,
        pkcs12_password,
    )
