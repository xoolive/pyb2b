# Python API to EUROCONTROL NM B2B services

## Installation

```sh
poetry install
```

## Get started

> [!IMPORTANT]  
> You have to own a B2B certificate granted by EUROCONTROL to get access to this data.

You must provide a config file with your key and password to use pyb2b.

```text
[global]
pkcs12_filename = path/to/your/p12/file
pkcs12_password = your_password
mode = OPS/PREOPS
version = 26.0.0
```

This file must be placed in the user_config_dir.

- on linux: `~/.config/b2b/b2b.conf`
- on mac: `~/Library/Application Support/b2b/b2b.conf`
- on windows: `C:\\Users\\<username>\\AppData\\Local\\<AppAuthor>\\<AppName>`

Then you may run a text-user interface:

```sh
poetry run b2b
```

The client is also available programmatically (Python):

```python
from pyb2b import b2b
```

> [!WARNING]  
> Documentation is still very limited:
>
> - Functions are self documented, listed through autocompletion
> - Most functions return a structure with a JSON object fully typed (for autocompletion in modern editors)
> - All functions have an asynchronous version (with the `async_` prefix)

Asynchronous functions take a `httpx.AsyncClient` as a first argument, to be called as follows:

```python
import httpx
import b2b

async with httpx.AsyncClient(verify=b2b.context) as client:
    result = await b2b.async_...(
        client, # and extra arguments
    )
```
