# Python API to EUROCONTROL NM B2B services

## Get started

You must provide a config file with your key and password to use pyb2b.

```text
[network]
http.proxy = <>
https.proxy = <>
ssh.proxycommand = ""

[nmb2b]
pkcs12_filename = path/to/your/p12/file
pkcs12_password = your_password
mode = OPS/PREOPS
version = 26.0.0
```

This file must be placed in the user_config_dir.

- on linux: `~/.config/traffic/traffic.conf`
- on mac: `~/Library/Application Support/traffic/traffic.conf`
- on windows: `C:\\Users\\<username>\\AppData\\Local\\<AppAuthor>\\<AppName>`

Then you start using pyb2b:

```python:
import pandas as pd
from pyb2b import b2b

today = pd.Timestamp("now")

res = b2b.flight_list(today, origin="LFBO")
print(res)
```
