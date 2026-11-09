# Task 9: Linux Server Hardening

Hardening of a fresh Ubuntu 26.04 LTS server (AWS EC2). The state before and after is saved in `before-state.txt` and `after-state.txt`, and the config files are in `configs/`.

## Checklist

| Item | Result |
|------|--------|
| Disable root SSH | `PermitRootLogin no`; root login is rejected with `Permission denied (publickey)` |
| Key-based auth | `PubkeyAuthentication yes`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `MaxAuthTries 3` |
| ufw firewall | enabled; default deny incoming, allow outgoing; ports 22 and 9000 allowed |
| fail2ban | `sshd` jail enabled; 5 failures in 10 minutes ban an IP for 1 hour |
| Unattended security updates | enabled; security origins allowed; daily; no automatic reboot |

## Steps

1. Opened a second SSH session as a safety net before changing anything.
2. Recorded the current state (`before-state.txt`).
3. SSH: wrote `/etc/ssh/sshd_config.d/00-hardening.conf` (the `00-` prefix makes it win over other files), checked it with `sshd -t`, confirmed it with `sshd -T`, reloaded with `systemctl reload ssh`, then tested a fresh key login and a refused root login.
4. Firewall: set the default policies, allowed `22/tcp` first, then `9000/tcp`, checked with `ufw show added`, then ran `ufw enable` and tested a fresh login.

        sudo ufw default deny incoming
        sudo ufw default allow outgoing
        sudo ufw allow 22/tcp comment 'SSH'
        sudo ufw allow 9000/tcp comment 'proxy container'
        sudo ufw enable

5. fail2ban: installed `fail2ban` and `python3-systemd`, wrote `/etc/fail2ban/jail.local` with the systemd backend, then ran `systemctl enable --now fail2ban`.
6. Unattended updates: wrote `/etc/apt/apt.conf.d/20auto-upgrades` and checked it with `unattended-upgrade --dry-run --debug`.
7. Recorded the final state (`after-state.txt`).

## Notes

- Published Docker container ports are not filtered by ufw, so the AWS security group stays the main control for those.
- Automatic reboot is left off, so updates never restart the server unexpectedly.
