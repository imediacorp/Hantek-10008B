# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report vulnerabilities by emailing **security@imediacorp.com** with:

- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

You will receive an acknowledgement within 48 hours and a resolution timeline
within 5 business days.

## Scope

This library communicates exclusively over local USB. There is no network
component. The primary attack surface is USB device spoofing (BadUSB) and
malformed USB data from a compromised or counterfeit device.
