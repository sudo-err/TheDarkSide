# TheDarkSide

Dark web scraper and crawler written in python with highly customizable settings.

## Installation

Make sure you have TOR installed and running
```bash
sudo apt install tor &&
sudo systemctl start tor
```

Edit its settings in ```/etc/tor/torrc``` and decomment and set the lines:
- ```ControlPort 9051``` (or any other available port)
- ```CookieAuthentication 0```

Create a virtual environment (optional but recommended)
```bash
python3 -m venv .venv &&
source .venv/bin/activate
```

Install dependencies
```bash
pip install --upgrade pip &&
pip install -r requirements.txt
```

## Running

```bash
python3 TheDarkSide
```

Use option ```-h``` to list all possible arguments.
