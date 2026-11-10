# HTB & TryHackMe Lab Tools

Scripts for learning and practicing security testing **only on authorized Hack The Box (HTB) and TryHackMe (THM) lab boxes**. Each script is specific to the box documented in its folder; these are not general-purpose tools for testing arbitrary systems.

## Authorized use only

This repository is provided for educational purposes only. Use its contents only on HTB or THM boxes that you are authorized to access, and follow the platform's rules and scope. Do not use these scripts against public services, other users, or any system without explicit authorization.

You are responsible for your actions and for complying with applicable laws and platform terms. The author does not authorize or endorse misuse. The code is provided as-is, without warranties; to the extent permitted by law, the author disclaims liability for its use. This notice is not a guarantee of legal protection.

## Repository structure

Folders are organized by platform, then by box name. These are directories, not Git branches.

```text
.
├── README.md
└── thm/                     # TryHackMe
    └── dreaming/            # Dreaming box
        ├── README.md        # Requirements and usage
        └── webshell.py
```

Future Hack The Box scripts should go under `htb/<box-name>/`; future TryHackMe scripts should go under `thm/<box-name>/`. Only boxes with available scripts are included. Read the box's README before running anything.
