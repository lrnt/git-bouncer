# Git Bouncer

Manage git repository access for users. It uses the SSH authorized_keys file to
determine the user with their public key.

```
command="/path/to/bouncer.py <username>",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty <key_type> <key> <key_comment>
```
