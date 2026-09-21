# Automated Network Traffic Sampler (`pcap-auto-sampler`)

An automated Python tool designed to collect periodic, lightweight PCAP samples from a designated network interface for offline traffic analysis and threat hunting.

## SOC Use Case
Continuous PCAP logging on high-bandwidth links can quickly overwhelm storage infrastructure. This tool demonstrates a sampling-based ingestion pipeline designed for SOC environments where light baseline samples are routinely archived for:
- Protocol baseline analysis and bandwidth anomaly checking.
- Validation of detection engineering rules (e.g., Snort/Zeek rules) against network noise.
- Maintaining an audit trail of network traffic for security research and training.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
