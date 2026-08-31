# Notes from Discord Call

## Services

SMB - anonymous -> "null"
Maybe: Window Event - Diagnoses
Maybe: Different operating event file (Linux, Windows + Maybe MAC)

## Report

Reading through the log -> detect if the server (version) is outdated / detect for any known exploit (even if it fails)

### SSH

Port forwarding -> target machine. Website hosted on target machine (not accessible publicly) -> make the port public. SSH local port forwarding:
https://www.digitalocean.com/community/tutorials/ssh-port-forwarding
Uploaded / copy files -> weird / exec / .ssh / .php / .bash_history file -> linpeas.ssh:
https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS (potential priv esc attempt)

### FTP

Anonymous login followed by file activity (php / html): Anonymous FTP user downloaded/uploaded files
CVE-2011-2523 -> check for other known exploits!:
https://access.redhat.com/security/cve/cve-2011-2523

### HTTP

SQL Injection
Directory / subdomain enumeration
Cross-Write Scripting (XSS)
XML Injection
SSTI ->
Service Side Request Forgery -> provide web service with a URL
File Inclusion Vulnerabilities (similiar to SSRF)
Maybe: Race conditions -> very similar to brute-force


## WebUI

Splunk (filtering)

TypeScript vs JavaScript
HTML + CSS
