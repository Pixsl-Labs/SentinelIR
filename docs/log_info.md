# Info on Log Files

Log files are records created by operating systems, services, applications, network devices, cloud platforms, and security tools. They are used for troubleshooting, monitoring, auditing, incident response, and threat detection.

For SentinelIR, log files are important because they provide evidence of authentication activity, suspicious access attempts, brute-force behaviour, service misuse, and possible compromise.

---

# Why Log Files Matter in Cyber Security

* They show what happened on a system or service.

* They help analysts investigate suspicious activity.

* They can reveal brute-force attacks, account compromise, privilege misuse, and scanning.

* They support incident response by giving timestamps, source IPs, usernames, actions, and outcomes.

* They provide evidence for audits, compliance, and forensic investigation.

---

# Common Log File Locations

## Linux

* `/var/log/auth.log`
* `/var/log/syslog`
* `/var/log/kern.log`
* `/var/log/apache2/access.log`
* `/var/log/apache2/error.log`
* `/var/log/nginx/access.log`
* `/var/log/nginx/error.log`
* `/var/log/vsftpd.log`

## Windows

* Windows Event Viewer
* Security logs
* System logs
* Application logs
* PowerShell logs
* Sysmon logs

## Cloud / Containers

* AWS CloudTrail
* AWS CloudWatch Logs
* Azure Monitor Logs
* Google Cloud Logging
* Docker container logs
* Kubernetes pod logs
* Kubernetes audit logs

---

# Authentication Logs

Authentication logs record login attempts, failed passwords, successful sessions, privilege escalation, and user access events.

These are one of the most useful log types for SentinelIR because they directly support brute-force, suspicious success, and account-targeting detections.

## Linux SSH Authentication Logs

Common file:

```text
/var/log/auth.log
```

Useful for detecting:

* Failed SSH login attempts
* Successful SSH logins
* Invalid usernames
* Root login attempts
* Brute-force attacks
* Suspicious success after failures

### Successful SSH Login Example

```text
Apr 12 2026 12:00:01 server sshd[1201]: Accepted password for sam from 192.168.1.25 port 55231 ssh2
```

### Failed SSH Login Example

```text
Apr 12 2026 12:00:04 server sshd[1202]: Failed password for admin from 192.168.1.30 port 55232 ssh2
```

### Invalid User SSH Example

```text
Apr 12 2026 12:00:07 server sshd[1203]: Failed password for invalid user oracle from 203.0.113.50 port 55233 ssh2
```

### Malformed SSH Log Example

```text
BROKEN SSH LINE missing timestamp user root from unknown
```

### SentinelIR Detection Ideas

* Brute-force detection from repeated failed SSH logins.
* Suspicious success when an IP fails first, then successfully logs in.
* User-targeting detection when many IPs attack the same username.
* Root login monitoring.
* Invalid username tracking.

---

# FTP Logs

FTP logs record file transfer authentication activity and client connections.

FTP is useful for SentinelIR because anonymous FTP access can be risky if exposed publicly or misconfigured.

Common files:

```text
/var/log/vsftpd.log
/var/log/auth.log
```

Example FTP services:

* vsftpd
* ProFTPD
* Pure-FTPd

## Defined SentinelIR FTP Format

SentinelIR currently supports a defined FTP authentication log format:

```text
Apr 12 2026 12:00:01 server vsftpd[2101]: FTP LOGIN SUCCESS user=sam ip=192.168.1.25
```

Required fields:

* Timestamp
* FTP login status
* Username
* Source IP address

### Successful FTP Login Example

```text
Apr 12 2026 12:00:01 server vsftpd[2101]: FTP LOGIN SUCCESS user=sam ip=192.168.1.25
```

### Failed FTP Login Example

```text
Apr 12 2026 12:00:04 server vsftpd[2102]: FTP LOGIN FAILED user=admin ip=192.168.1.30
```

### Anonymous FTP Login Example

```text
Apr 12 2026 12:00:08 server vsftpd[2103]: FTP LOGIN SUCCESS user=anonymous ip=203.0.113.50
```

### Malformed FTP Log Example

```text
BROKEN FTP LINE missing timestamp user anonymous ip unknown
```

### Real vsftpd Style Examples

```text
Mon Aug 21 14:37:23 2006 [pid 20293] [dcid] OK LOGIN: Client "127.0.0.1"
```

```text
Mon Aug 21 14:33:24 2006 [pid 20175] [dcid] FAIL LOGIN: Client "127.0.0.1"
```

### SentinelIR Detection Ideas

* Anonymous FTP login detection.
* Failed FTP brute-force detection.
* Suspicious FTP success after failed attempts.
* External IPs using anonymous FTP.
* Repeated FTP failed login attempts from one IP.

---

# Web Server Access Logs

Web access logs record HTTP requests made to a web server.

They are useful for detecting scanning, broken pages, suspicious user agents, admin panel probing, and possible web attacks.

Common files:

```text
/var/log/apache2/access.log
/var/log/nginx/access.log
```

Useful fields:

* Source IP
* Timestamp
* HTTP method
* Requested path
* HTTP status code
* Response size
* Referrer
* User agent

## Apache / Nginx Access Log Examples

### Successful HTTP Request Example

```text
192.168.1.20 - - [12/Apr/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 532 "-" "Mozilla/5.0"
```

### Failed / Not Found HTTP Request Example

```text
203.0.113.44 - - [12/Apr/2026:12:00:05 +0000] "GET /admin.php HTTP/1.1" 404 162 "-" "curl/8.0"
```

### Suspicious HTTP Request Example

```text
198.51.100.10 - - [12/Apr/2026:12:00:08 +0000] "GET /.env HTTP/1.1" 404 162 "-" "python-requests/2.31"
```

### Malformed HTTP Log Example

```text
BROKEN HTTP REQUEST missing method path status
```

### SentinelIR Detection Ideas

* High number of 404 responses from one IP.
* Requests for sensitive paths such as `/admin`, `/.env`, `/wp-login.php`.
* Suspicious user agents such as curl, sqlmap, nikto, python-requests.
* Request spikes from one IP.
* Possible directory brute-forcing.

---

# Web Server Error Logs

Error logs record server-side problems, application errors, permission issues, and backend failures.

Common files:

```text
/var/log/apache2/error.log
/var/log/nginx/error.log
```

### Nginx Error Example

```text
2026/04/12 12:00:01 [error] 1200#1200: *10 open() "/var/www/html/admin.php" failed (2: No such file or directory), client: 203.0.113.44, server: example.com, request: "GET /admin.php HTTP/1.1"
```

### Apache Error Example

```text
[Sun Apr 12 12:00:02.123456 2026] [authz_core:error] [pid 1301] [client 192.168.1.30:55231] AH01630: client denied by server configuration: /var/www/html/private
```

### Malformed Error Log Example

```text
ERROR missing timestamp missing client missing request
```

### SentinelIR Detection Ideas

* Repeated access denied errors.
* Repeated missing file probes.
* Suspicious client IPs causing many errors.
* Possible scanning or exploitation attempts.

---

# Windows Security Logs

Windows Security logs record logon events, failed authentication, privilege use, account changes, and other security-relevant activity.

Common tool:

```text
Windows Event Viewer
```

Important Event IDs:

* `4624`: Successful logon
* `4625`: Failed logon
* `4634`: Logoff
* `4648`: Logon using explicit credentials
* `4672`: Special privileges assigned
* `4688`: Process creation
* `4720`: User account created
* `4726`: User account deleted

## Windows Logon Examples

### Successful Windows Logon Example

```text
EventID=4624 AccountName=sam WorkstationName=DESKTOP-01 IpAddress=192.168.1.25 LogonType=10
```

### Failed Windows Logon Example

```text
EventID=4625 AccountName=admin WorkstationName=DESKTOP-01 IpAddress=203.0.113.50 FailureReason=Unknown user name or bad password
```

### Privileged Logon Example

```text
EventID=4672 AccountName=Administrator Privileges=SeDebugPrivilege,SeBackupPrivilege
```

### Malformed Windows Event Example

```text
EventID=4625 AccountName= IpAddress= FailureReason=
```

### SentinelIR Detection Ideas

* Failed Windows logon brute-force.
* RDP brute-force using LogonType 10.
* Successful logon after repeated failures.
* Privileged account activity.
* Account creation or deletion during suspicious time windows.

---

# Firewall Logs

Firewall logs record allowed and blocked traffic.

They are useful for network investigation because they show source IPs, destination IPs, ports, protocols, and rule actions.

Example sources:

* UFW
* iptables
* Windows Defender Firewall
* pfSense
* Palo Alto
* Fortinet
* Cisco ASA

## Firewall Log Examples

### Allowed Connection Example

```text
Apr 12 12:00:01 firewall kernel: [UFW ALLOW] SRC=192.168.1.25 DST=192.168.1.10 PROTO=TCP SPT=55231 DPT=22
```

### Blocked Connection Example

```text
Apr 12 12:00:04 firewall kernel: [UFW BLOCK] SRC=203.0.113.50 DST=192.168.1.10 PROTO=TCP SPT=44321 DPT=3389
```

### Suspicious Port Scan Example

```text
Apr 12 12:00:08 firewall kernel: [UFW BLOCK] SRC=198.51.100.20 DST=192.168.1.10 PROTO=TCP SPT=40000 DPT=23
```

### Malformed Firewall Log Example

```text
UFW BLOCK missing src dst proto ports
```

### SentinelIR Detection Ideas

* Repeated blocked traffic from one IP.
* Port scanning across many destination ports.
* Attempts against risky ports such as 22, 23, 3389, 445, 8080.
* External access attempts to internal services.

---

# System Logs

System logs record operating system events, service failures, kernel messages, restarts, crashes, and hardware issues.

Common files:

```text
/var/log/syslog
/var/log/messages
/var/log/kern.log
```

### Successful Service Start Example

```text
Apr 12 12:00:01 server systemd[1]: Started OpenSSH server daemon.
```

### Failed Service Example

```text
Apr 12 12:00:04 server systemd[1]: nginx.service: Failed with result 'exit-code'.
```

### Kernel Warning Example

```text
Apr 12 12:00:08 server kernel: [12345.678901] TCP: Possible SYN flooding on port 80.
```

### Malformed System Log Example

```text
SYSTEM EVENT missing timestamp missing service
```

### SentinelIR Detection Ideas

* Security service stopped.
* Repeated service crashes.
* Firewall or SSH service restarts.
* Kernel warnings linked to network activity.

---

# Application Logs

Application logs are generated by software applications and usually record user actions, errors, API requests, exceptions, and business events.

Common formats:

* Plain text
* JSON
* CSV
* Structured key-value logs

### Successful Application Login Example

```text
2026-04-12T12:00:01Z INFO user=sam action=login status=success ip=192.168.1.25
```

### Failed Application Login Example

```text
2026-04-12T12:00:04Z WARN user=admin action=login status=failed ip=203.0.113.50 reason=bad_password
```

### Application Error Example

```text
2026-04-12T12:00:08Z ERROR service=api message="Database connection timeout" request_id=abc123
```

### Malformed Application Log Example

```text
LOGIN FAILED missing user missing ip missing timestamp
```

### SentinelIR Detection Ideas

* Failed application login brute-force.
* Suspicious success after failed application logins.
* API errors linked to attack attempts.
* Repeated failed login from one IP.

---

# Database Logs

Database logs record connections, authentication failures, queries, errors, slow queries, and transaction events.

Example database systems:

* PostgreSQL
* MySQL
* MariaDB
* MongoDB
* Microsoft SQL Server

## PostgreSQL Log Examples

### Successful Database Connection Example

```text
2026-04-12 12:00:01 UTC [2201] LOG: connection authorized: user=sam database=prod application_name=psql
```

### Failed Database Login Example

```text
2026-04-12 12:00:04 UTC [2202] FATAL: password authentication failed for user "admin"
```

### Missing Access Rule Example

```text
2026-04-12 12:00:08 UTC [2203] FATAL: no pg_hba.conf entry for host "203.0.113.50", user "admin", database "prod"
```

### Malformed Database Log Example

```text
DATABASE ERROR missing user missing host missing timestamp
```

### SentinelIR Detection Ideas

* Database brute-force attempts.
* Failed authentication from external IPs.
* Access attempts to sensitive databases.
* Repeated failed login for admin or privileged accounts.

---

# Cloud Logs

Cloud logs record activity across cloud accounts, services, users, API calls, storage, networking, and identity systems.

Examples:

* AWS CloudTrail
* AWS CloudWatch
* Azure Monitor
* Microsoft Entra ID sign-in logs
* Google Cloud Logging

## AWS CloudTrail Examples

### Successful Console Login Example

```json
{
  "eventTime": "2026-04-12T12:00:01Z",
  "eventName": "ConsoleLogin",
  "sourceIPAddress": "192.168.1.25",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "sam"
  },
  "responseElements": {
    "ConsoleLogin": "Success"
  }
}
```

### Failed Console Login Example

```json
{
  "eventTime": "2026-04-12T12:00:04Z",
  "eventName": "ConsoleLogin",
  "sourceIPAddress": "203.0.113.50",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "admin"
  },
  "responseElements": {
    "ConsoleLogin": "Failure"
  },
  "errorMessage": "Failed authentication"
}
```

### Suspicious Cloud API Example

```json
{
  "eventTime": "2026-04-12T12:00:08Z",
  "eventName": "DeleteTrail",
  "sourceIPAddress": "198.51.100.20",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "admin"
  }
}
```

### Malformed Cloud Log Example

```json
{
  "eventName": "ConsoleLogin",
  "sourceIPAddress": "",
  "userIdentity": {}
}
```

### SentinelIR Detection Ideas

* Failed cloud console logins.
* Successful login after failures.
* Root account usage.
* CloudTrail deletion or logging changes.
* Suspicious API calls from unusual IPs.
* IAM user creation or privilege changes.

---

# Container Logs

Container logs are generated by containerised applications running through Docker or container runtimes.

Common locations:

```text
/var/lib/docker/containers/<container_id>/<container_id>-json.log
```

Container logs are often JSON-formatted and usually contain application stdout and stderr.

### Successful Container Log Example

```json
{
  "log": "2026-04-12T12:00:01Z INFO Started API server on port 8000\n",
  "stream": "stdout",
  "time": "2026-04-12T12:00:01.000000000Z"
}
```

### Failed Container Log Example

```json
{
  "log": "2026-04-12T12:00:04Z ERROR Failed to connect to database\n",
  "stream": "stderr",
  "time": "2026-04-12T12:00:04.000000000Z"
}
```

### Suspicious Container Log Example

```json
{
  "log": "2026-04-12T12:00:08Z WARN Failed login user=admin ip=203.0.113.50\n",
  "stream": "stdout",
  "time": "2026-04-12T12:00:08.000000000Z"
}
```

### Malformed Container Log Example

```json
{
  "log": "",
  "stream": "stdout"
}
```

### SentinelIR Detection Ideas

* Failed login attempts inside containerised applications.
* Application crashes.
* Repeated stderr errors.
* Suspicious API behaviour from app logs.

---

# Kubernetes Logs

Kubernetes logs include container logs, pod logs, node logs, system component logs, and audit logs.

Useful commands:

```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
```

Kubernetes logs are useful for investigating container crashes, pod restarts, API server activity, and suspicious cluster actions.

## Kubernetes Pod Log Examples

### Successful Pod Log Example

```text
2026-04-12T12:00:01Z INFO pod=auth-api message="User login successful" user=sam ip=192.168.1.25
```

### Failed Pod Log Example

```text
2026-04-12T12:00:04Z WARN pod=auth-api message="Login failed" user=admin ip=203.0.113.50
```

### Kubernetes Error Example

```text
2026-04-12T12:00:08Z ERROR pod=auth-api message="CrashLoopBackOff detected"
```

### Malformed Kubernetes Log Example

```text
K8S LOG missing timestamp missing pod missing message
```

## Kubernetes Audit Log Example

```json
{
  "kind": "Event",
  "verb": "create",
  "user": {
    "username": "admin"
  },
  "sourceIPs": ["203.0.113.50"],
  "objectRef": {
    "resource": "pods",
    "namespace": "default"
  },
  "stage": "ResponseComplete"
}
```

### SentinelIR Detection Ideas

* Suspicious API actions.
* Pod creation by unusual users.
* Access from unusual source IPs.
* CrashLoopBackOff patterns.
* Privileged pod creation.
* Secrets accessed by unexpected users.

---

# Audit Logs

Audit logs record security-relevant actions, administrative changes, privilege use, policy changes, and configuration modifications.

Examples:

* Linux auditd logs
* Windows Security logs
* CloudTrail audit logs
* Kubernetes audit logs
* Database audit logs

### Successful Admin Action Example

```text
type=USER_CMD msg=audit(1776000001.123:100): user=sam command="sudo systemctl restart ssh"
```

### Failed Privileged Action Example

```text
type=USER_AUTH msg=audit(1776000004.123:101): user=admin result=failed
```

### Suspicious Audit Event Example

```text
type=USER_MGMT msg=audit(1776000008.123:102): user=root action="created new user backdoor"
```

### Malformed Audit Log Example

```text
AUDIT EVENT missing user missing action missing result
```

### SentinelIR Detection Ideas

* Suspicious user creation.
* Failed sudo attempts.
* Privilege escalation.
* Security config changes.
* Audit logging disabled.

---

# IDS / IPS Logs

Intrusion detection and prevention system logs record detected threats, signatures, alerts, and suspicious traffic.

Examples:

* Snort
* Suricata
* Zeek
* Wazuh
* OSSEC

### IDS Alert Example

```text
04/12/2026-12:00:01 [**] [1:1000001:1] Possible SSH Brute Force [**] [Priority: 2] {TCP} 203.0.113.50:55231 -> 192.168.1.10:22
```

### IDS Malware Alert Example

```text
04/12/2026-12:00:04 [**] [1:2000001:1] Malware Callback Detected [**] [Priority: 1] {TCP} 192.168.1.10:4444 -> 198.51.100.20:443
```

### Malformed IDS Log Example

```text
IDS ALERT missing signature missing src missing dst
```

### SentinelIR Detection Ideas

* Correlate IDS alerts with authentication logs.
* Highlight attacker IPs seen across multiple log sources.
* Show priority-based alerts.
* Link brute-force IDS alerts to SSH failed logins.

---

# DNS Logs

DNS logs record domain lookups made by clients.

They are useful for detecting malware callbacks, DNS tunnelling, suspicious domains, and unusual lookup volume.

### Normal DNS Query Example

```text
2026-04-12T12:00:01Z client=192.168.1.25 query=example.com type=A status=NOERROR
```

### Failed DNS Query Example

```text
2026-04-12T12:00:04Z client=192.168.1.30 query=randombad-domain.test type=A status=NXDOMAIN
```

### Suspicious DNS Query Example

```text
2026-04-12T12:00:08Z client=192.168.1.50 query=a8d9s7f6s5d4.example.net type=TXT status=NOERROR
```

### Malformed DNS Log Example

```text
DNS QUERY missing client missing domain missing status
```

### SentinelIR Detection Ideas

* Repeated NXDOMAIN responses.
* Long random-looking domains.
* Suspicious TXT queries.
* Internal host making unusual DNS requests.

---

# VPN Logs

VPN logs record remote access sessions, authentication attempts, IP assignment, and connection duration.

Examples:

* OpenVPN
* WireGuard
* Cisco AnyConnect
* Palo Alto GlobalProtect
* Fortinet SSL VPN

### Successful VPN Login Example

```text
2026-04-12 12:00:01 OpenVPN AUTH_SUCCESS user=sam source_ip=192.168.1.25 assigned_ip=10.8.0.5
```

### Failed VPN Login Example

```text
2026-04-12 12:00:04 OpenVPN AUTH_FAILED user=admin source_ip=203.0.113.50 reason=bad_password
```

### Suspicious VPN Login Example

```text
2026-04-12 03:12:08 OpenVPN AUTH_SUCCESS user=admin source_ip=198.51.100.20 assigned_ip=10.8.0.9
```

### Malformed VPN Log Example

```text
VPN AUTH missing user missing source ip
```

### SentinelIR Detection Ideas

* VPN brute-force attempts.
* Suspicious VPN success after failures.
* Admin VPN login outside normal hours.
* Login from unusual countries or IP ranges.

---

# Email Logs

Email logs record message delivery, authentication attempts, spam filtering, and mail server activity.

Examples:

* Postfix
* Exim
* Microsoft Exchange
* Microsoft 365 audit logs
* Google Workspace logs

### Successful Email Delivery Example

```text
Apr 12 12:00:01 mail postfix/smtp[2201]: ABC123: to=<user@example.com>, status=sent
```

### Failed Email Delivery Example

```text
Apr 12 12:00:04 mail postfix/smtp[2202]: DEF456: to=<user@example.com>, status=bounced
```

### Suspicious Email Auth Example

```text
Apr 12 12:00:08 mail postfix/smtpd[2203]: warning: unknown[203.0.113.50]: SASL LOGIN authentication failed
```

### Malformed Email Log Example

```text
MAIL LOG missing sender missing recipient missing status
```

### SentinelIR Detection Ideas

* Failed SMTP authentication.
* Suspicious email login attempts.
* High bounce volume.
* Possible phishing infrastructure activity.

---

# Endpoint / EDR Logs

Endpoint logs record process execution, file changes, network connections, registry activity, malware detections, and security alerts.

Examples:

* Sysmon
* Windows Defender
* CrowdStrike
* Microsoft Defender for Endpoint
* SentinelOne

### Process Creation Example

```text
EventID=4688 User=sam NewProcessName=C:\Windows\System32\cmd.exe ParentProcessName=explorer.exe
```

### Suspicious PowerShell Example

```text
EventID=4688 User=sam NewProcessName=powershell.exe CommandLine="-EncodedCommand SQBFAFgA..."
```

### Malware Detection Example

```text
2026-04-12T12:00:08Z Defender ThreatName=Trojan:Win32/Example Action=Quarantined User=sam
```

### Malformed Endpoint Log Example

```text
ENDPOINT EVENT missing process missing user missing timestamp
```

### SentinelIR Detection Ideas

* Suspicious PowerShell commands.
* New process spawned by Office applications.
* Malware detection events.
* Lateral movement commands.
* Unknown executable execution.

---

# Common Log File Formats

## Plain Text

Simple human-readable logs.

```text
Apr 12 12:00:01 server sshd[1201]: Accepted password for sam from 192.168.1.25 port 55231 ssh2
```

## Syslog

Common Linux/network format containing timestamp, host, service, process ID, and message.

```text
Apr 12 12:00:01 server sshd[1201]: Failed password for admin from 203.0.113.50 port 55231 ssh2
```

## JSON

Structured format often used in cloud, container, and modern application logs.

```json
{
  "timestamp": "2026-04-12T12:00:01Z",
  "event": "login",
  "user": "sam",
  "ip": "192.168.1.25",
  "status": "success"
}
```

## CSV

Comma-separated format often used for exports.

```csv
timestamp,event,user,ip,status
2026-04-12T12:00:01Z,login,sam,192.168.1.25,success
```

## Key-Value

Common in security and application logs.

```text
timestamp=2026-04-12T12:00:01Z event=login user=sam ip=192.168.1.25 status=success
```

## XML

Common in Windows Event Logs and some enterprise tools.

```xml
<Event>
  <System>
    <EventID>4624</EventID>
  </System>
  <EventData>
    <Data Name="TargetUserName">sam</Data>
    <Data Name="IpAddress">192.168.1.25</Data>
  </EventData>
</Event>
```

---

# Specialized Log Types

* Audit logs: Track admin actions, policy changes, privileged activity, and configuration changes.

* Access logs: Show who accessed what, when, and from where.

* Authentication logs: Record login success, login failure, session start, session end, and account access.

* Error logs: Record service errors, crashes, warnings, missing files, and failed operations.

* Transaction logs: Used in databases and financial systems to trace query history, payment events, or state changes.

* Network logs: Record traffic flow, blocked connections, DNS queries, proxy requests, and firewall decisions.

* Cloud logs: Record cloud API calls, console logins, storage access, identity activity, and infrastructure changes.

* Container logs: Record stdout and stderr from containerised applications.

* Kubernetes logs: Record pod logs, cluster events, API server actions, audit events, and system component activity.

* IDS / IPS logs: Record threat signatures, suspicious traffic, and alert priority.

* EDR logs: Record endpoint process execution, malware detections, file changes, and suspicious behaviour.

* Machine learning logs: Record model training runs, inference outputs, failures, drift, and performance metrics.

---

# Where Do Log Files Come From?

* Servers: OS events, crashes, restarts, authentication activity.

* Applications: User activity, performance errors, API calls.

* Security infrastructure: Access attempts, firewall matches, IDS alerts, EDR detections.

* Databases: Queries, errors, connections, failed authentication, transactions.

* Endpoints: Laptops, desktops, mobile devices, and BYOD assets.

* Cloud services: API usage, autoscaling events, storage access, identity activity.

* Network devices: Switches, routers, firewalls, VPNs, and proxies.

* Containers: Docker and container runtime logs.

* Kubernetes clusters: Pod logs, audit logs, node logs, API server logs.

* IoT devices: Sensor readings, connection attempts, firmware errors, and device health.

---

# Log Storage

* Local log storage: Logs are stored on the system that generated them.

* Centralised logging: Logs are forwarded to a central platform such as Splunk, Elastic, Wazuh, Graylog, Sentinel, or CloudWatch.

* Cloud-native logging: Cloud services store logs in systems such as AWS CloudWatch, AWS CloudTrail, Azure Monitor, or Google Cloud Logging.

* Long-term archive storage: Logs can be stored in cheaper archive storage for compliance and forensic review.

* SIEM storage: Security logs are ingested into SIEM platforms for correlation, alerting, dashboards, and investigation.

---

# SentinelIR Supported Log Sources

Current / planned support:

* SSH authentication logs
* FTP authentication logs
* Anonymous FTP login detection
* Future HTTP access log support
* Future Windows Event Log support
* Future cloud log support
* Future container and Kubernetes log support

Current project statement:

```text
SentinelIR currently supports Linux SSH-style authentication logs and a defined FTP authentication log format. Future versions may expand support to HTTP access logs, Windows Security logs, cloud audit logs, and container logs.
```

---

# Sources

# Sources

- LogicMonitor: Log Files Explained
  https://www.logicmonitor.com/blog/log-files-explained-types-uses-best-practices

- Elastic: Grokking Linux Authorization Logs
  https://www.elastic.co/blog/grokking-the-linux-authorization-logs

- OSSEC: SSH / Linux Log Samples
  https://www.ossec.net/docs/log_samples/

- OSSEC: FTP Log Samples
  https://www.ossec.net/docs/log_samples/ftp/index.html

- OSSEC: vsftpd Log Samples
  https://www.ossec.net/docs/log_samples/ftp/vsftpd.html

- Loggly: Access and Error Logs Guide
  https://www.loggly.com/ultimate-guide/access-and-error-logs/

- DigitalOcean: NGINX Access and Error Logs
  https://www.digitalocean.com/community/tutorials/nginx-access-logs-error-logs

- Microsoft Learn: Windows Security Event ID 4624 - Successful Logon
  https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624

- Microsoft Learn: Windows Security Event ID 4625 - Failed Logon
  https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625

- AWS Documentation: CloudTrail Log File Examples
  https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-examples.html

- AWS Documentation: Console Sign-In Events
  https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-aws-console-sign-in-events.html

- Kubernetes Documentation: Logging Architecture
  https://kubernetes.io/docs/concepts/cluster-administration/logging/

- Kubernetes Documentation: System Logs
  https://kubernetes.io/docs/concepts/cluster-administration/system-logs/

- Docker Documentation: JSON File Logging Driver
  https://docs.docker.com/engine/logging/drivers/json-file/

- PostgreSQL Documentation: Authentication Problems
  https://www.postgresql.org/docs/current/client-authentication-problems.html

- Suricata Documentation: EVE JSON Output
  https://docs.suricata.io/en/latest/output/eve/eve-json-output.html

- Zeek Documentation: conn.log
  https://docs.zeek.org/en/master/reference/logs/conn.html

- Zeek Documentation: dns.log
  https://docs.zeek.org/en/current/logs/dns.html

- Zeek Documentation: http.log
  https://docs.zeek.org/en/current/reference/logs/http.html
