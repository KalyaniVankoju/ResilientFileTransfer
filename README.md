# Resilient File Transfer over Unreliable Networks

A computer networks project that demonstrates how reliable file transfer can be achieved over an unreliable packet-switched network using the **Stop-and-Wait ARQ protocol**.

The system simulates packet loss and ACK loss, detects duplicate packets, performs retransmissions after timeouts, reassembles the transferred file, and verifies file integrity.

A web-based interface provides a visual representation of the packet transmission and retransmission process.

---

## Live Demo

### Frontend
https://resilient-file-transfer.vercel.app/

### Backend API
https://resilientfiletransfer.onrender.com/

### API Documentation
https://resilientfiletransfer.onrender.com/docs

---

## Project Overview

In a real network, data transmitted between two hosts is divided into smaller packets.

Packets may be:

- Lost during transmission
- Delayed
- Re-transmitted
- Received more than once

A reliable communication mechanism is therefore required to ensure that the complete file reaches the receiver correctly.

This project implements a simplified reliable file-transfer system using **Stop-and-Wait ARQ** over a controlled unreliable network simulation.

---

## Objectives

- Divide a file into smaller packets.
- Assign sequence numbers to packets.
- Simulate an unreliable network.
- Simulate DATA packet loss.
- Simulate ACK packet loss.
- Detect duplicate packets.
- Use acknowledgements to confirm successful delivery.
- Use timeouts to detect failed transmissions.
- Retransmit packets when necessary.
- Reassemble the packets at the receiver.
- Verify that the reconstructed file matches the original file.
- Evaluate protocol performance under different packet-loss rates.
- Visualize the transfer process through a web interface.

---

## System Architecture

```text
                    RESILIENT FILE TRANSFER

                           USER
                            |
                            v
                    +---------------+
                    |    SENDER     |
                    +---------------+
                            |
                            v
                    File Packetization
                            |
                            v
                 +-----------------------+
                 |   Stop-and-Wait ARQ   |
                 |                       |
                 | Sequence Number       |
                 | ACK                   |
                 | Timeout               |
                 | Retransmission        |
                 +-----------------------+
                            |
                            | DATA
                            v
                +-------------------------+
                |   UNRELIABLE NETWORK    |
                |                         |
                | Packet Loss             |
                | ACK Loss                |
                +-------------------------+
                            |
                            v
                    +---------------+
                    |   RECEIVER    |
                    +---------------+
                            |
                            v
                    Packet Reassembly
                            |
                            v
                   Integrity Verification
                            |
                            v
                    Reconstructed File
