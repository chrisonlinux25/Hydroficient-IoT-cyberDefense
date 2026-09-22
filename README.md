# Hydroficient-IoT-cyberDefense
IoT Cybersecurity; Building IoT water defense Pipeline.

# An 8-Week IoT Security Externship — Securing the Grand Marina Hotel's Water Infrastructure

![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)
![Duration](https://img.shields.io/badge/Duration-8%20Weeks-blue?style=flat-square)
![Role](https://img.shields.io/badge/Role-Junior%20Security%20Engineer-orange?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20MQTT%20%7C%20TLS%2FmTLS%20%7C%20AI-informational?style=flat-square)
![Outcome](https://img.shields.io/badge/Outcome-Passed%20Insurance%20Audit-success?style=flat-square)

## 📖 Overview
This repository documents an 8-week hands-on cybersecurity externship at Hydroficient, a company specializing in IoT-based water management systems for commercial properties.

I joined the project as a Junior Security Engineer, working under Maya Chen, Senior Security Engineer. My first assignment was The Grand Marina Hotel, a 500-room luxury resort operating three HYDROLOGIC flow-management devices across its water infrastructure.

The General Manager, Marcus Webb, had one question:

“Is our system secure?”

Over the course of eight weeks, I answered that question by building and securing the entire IoT security stack from the ground up. Rather than simply studying the concepts, I implemented a real MQTT pipeline, analyzed it from an attacker’s perspective, identified its weaknesses, and progressively strengthened the system through TLS encryption, device authentication, mutual TLS (mTLS), replay-attack protection, real-time security monitoring, and AI-powered anomaly detection.

By the end of the project, the Grand Marina's water-management system had a layered security architecture designed to protect both its data and its physical infrastructure. The resulting architecture became the baseline security specification for Hydroficient’s next hotel expansion, covering an additional 42 rooms.

## 🏨 The Client: The Grand Marina Hotel

| Property | Details |
|---|---|
| Guest rooms | 500 |
| Floors | 15 |
| Restaurants | 12 |
| Facilities | Olympic pool & spa, conference center |
| Guests on-site | 2,000+ on any given night |
| Water cost before Hydroficient | ~$300,000/month |
| Savings after Hydroficient | 15–20% reduction in consumption |
| Incoming water pressure | 85 PSI (vs. 40 PSI code minimum) |

### The Three HYDROLOGIC Devices

| Device | Location | Serves |
|---|---|---|
| Device 01 | Main Building Mechanical Room | Guest rooms, lobbies, restaurants |
| Device 02 | Pool/Spa Wing | Pool, spa, fitness center |
| Device 03 | Kitchen/Laundry Wing | Commercial kitchen, laundry facilities |

Each HYDROLOGIC device continuously sends upstream and downstream pressure, gate position, flow rate, and cumulative water consumption data to the cloud. Operators can also remotely adjust the gates or trigger an emergency water shutoff through a centralized dashboard.

This combination of real-time monitoring and remote physical control makes the system an IoT security challenge, not simply a data-security issue. A compromised device or dashboard could do more than expose sensitive information—it could disrupt the hotel’s water supply and potentially shut off water to all 500 guest rooms.

## System Architecture


## 🎥 Video Demos
   1. The Attack Simulation and Live Security Dashboard
      
   2. AI Detection and Replay-Attack Dashboard
      
   3. Live Water Security Dashboard
      
## 📑 Capstone Presentation

## 🛡️ Defense-in-Depth: The Complete Security Stack

Each project added one independent layer of protection. No single layer is sufficient on its own — together, they provide multiple lines of defense and close different security gaps.

| Security Layer | Project | Defends Against |
|---|---:|---|
| **Threat Modeling (STRIDE + CIA)** | 1 | Unknown and unmapped risks |
| **TLS Encryption** | 4 | Network eavesdropping |
| **Mutual TLS (Device Identity)** | 5 | Rogue or unauthorized devices connecting |
| **Timestamp Validation** | 6 | Stale replayed messages |
| **Sequence Counters** | 6 | Duplicate or recently replayed messages |
| **HMAC Message Signing** | 6 | Tampered message content |
| **Live Dashboard Monitoring** | 7 | Slow human detection and response |
| **AI Anomaly Detection (Isolation Forest)** | 8 | Gradual drift and abnormal patterns that bypass rule-based defenses |


## 📁 Folder Structure


## 🧩 Project-by-Project Breakdown
  
  ##  Project 1 — Mapping the Hydroficient IoT System & Identifying Security Risks

**Threat modeling before writing a single line of code.**

• Mapped the complete IoT device-to-cloud architecture and identified critical assets across the HYDROLOGIC devices, cloud API, remote controls, and operator dashboard.

• Applied the CIA Triad to evaluate risks to Confidentiality, Integrity, and Availability.

• Developed an attacker mindset by identifying valuable targets, exposed components, potential weaknesses, and possible attack paths.

• Built a STRIDE threat model covering Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.

• Deliverable: A professional threat model documenting the system architecture, attack surface, threats, and key security risks.

---

## Project 2 — Learn Python Basics to Work With Sensor Data

**Building the language skills needed to simulate a real IoT device.**

* **Python fundamentals:** data structures, control flow, and functions
* Working with **JSON** and **nested JSON** using Pandas
* Data cleaning and preparation concepts
* Built a `WaterSensor` class — a **mock sensor log generator** that simulates realistic pressure/flow readings, including timestamps and sequence counters, laying the groundwork for replay-attack defenses later in the project

---

## Project 3 — Build a Fake Sensor & Send Data in an Insecure Way

**Standing up the real pipeline — then attacking it.**

* Installed and configured **Mosquitto** (MQTT broker) and the **paho-mqtt** Python library
* Learned MQTT fundamentals: topics, QoS levels, and publish/subscribe message flow
* Designed the full MQTT topic hierarchy for The Grand Marina:
  `hydroficient/grandmarina/sensors/...`
  `hydroficient/grandmarina/commands/...`
  `hydroficient/grandmarina/alerts/...`
  `hydroficient/grandmarina/status/...`
* Built `sensor_publisher.py` and `dashboard_subscriber.py` — a working three-terminal pipeline: **sensor → broker → live dashboard**
* **The uncomfortable experiment:** opened a fourth terminal, subscribed with zero authentication, and watched every device ID, pressure reading, and timestamp scroll past in plain text — demonstrating the exact vulnerability an attacker could exploit

---

## Project 4 — Add Encryption & Test How It Affects Performance

**Closing the confidentiality gap with TLS.**

- Learned how **TLS and digital certificates** work, including why HTTPS matters and what a Certificate Authority (CA) does
- Wrote `generate_certs.py` to create a private **Certificate Authority** and issue a server certificate for the Mosquitto broker
- Configured **Mosquitto for TLS** and updated the Python MQTT client accordingly
- Ran four controlled experiments — **Speed Test, Stress Test, Eavesdropper Test, and Certificate Test** — comparing TLS vs. no-TLS under normal, moderate-load, and emergency-mode conditions
- **Deliverable:** A professional **Security Assessment Report** quantifying encryption overhead with real experimental evidence

---

## Project 5 — Control Which Devices Are Allowed to Connect

**Closing the device identity gap with Mutual TLS (mTLS).**

- Learned the difference between **one-way TLS**, where only the server proves its identity, and **mutual TLS (mTLS)**, where both the server and client authenticate each other.
- Identified the security gap in one-way TLS: a rogue device with network access and the public CA certificate could connect to the broker because the client itself was not authenticated.
- Generated a unique client certificate for each of the three **HYDROLOGIC** devices and configured Mosquitto to require valid client certificates.
- Verified that legitimate devices could connect successfully while unauthorized devices without valid certificates were rejected.
- Tested different certificate scenarios, including **valid certificates, missing certificates, expired certificates, and certificates signed by the wrong CA**, and documented the results.
- Evaluated the performance impact of mTLS and confirmed that the added authentication introduced **negligible latency** in the tested environment.
- **Deliverable:** Created a **Device Provisioning Policy** covering device onboarding, certificate management, device retirement, and response to compromised devices.

  ---
  

## 📊 Outcome
The Grand Marina passed its insurance audit on the first attempt in three years — the auditor specifically called the live dashboard "the clearest security posture view she's reviewed at a property this size"
The security architecture built in this externship became the baseline spec for Hydroficient's next expansion — a new 42-room wing at the same property
Invited to help scope the threat model for that next phase

## 🎓 Skills Demonstrated

`Threat Modeling` `STRIDE` `CIA Triad` `Python` `MQTT` `TLS/mTLS` `PKI & Certificate Management` `HMAC` `Replay Attack Defense` `WebSockets` `Real-Time Dashboards` `Anomaly Detection` `Isolation Forest` `Security Assessment Reporting` `Technical Documentation` `Incident Simulation`




