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
```

### ACK Flow

```text
Sender                         Receiver
  |                               |
  | -------- DATA --------------> |
  |                               |
  | <--------- ACK -------------- |
  |                               |
```

If the DATA packet or ACK is lost, the sender waits for a timeout and retransmits the packet.

---

## Stop-and-Wait ARQ

The project uses **Stop-and-Wait ARQ** as its reliability mechanism.

For every packet:

1. Sender transmits one DATA packet.
2. Receiver checks the sequence number.
3. Receiver accepts the packet if it is the expected packet.
4. Receiver sends an ACK.
5. Sender waits for the ACK.
6. If the ACK is received, the sender transmits the next packet.
7. If the DATA packet or ACK is lost, the sender waits until timeout.
8. The sender retransmits the packet.
9. Duplicate packets are detected by the receiver.

This continues until the complete file has been transferred.

---

## Packet Structure

Each data packet contains:

```text
Sequence Number
Data
```

The sequence number allows the receiver to determine:

- Which packet is expected
- Whether a packet is a duplicate
- The correct order for file reconstruction

---

## File Transfer Process

```text
Original File
      |
      v
+------------------+
| File Packetizer  |
+------------------+
      |
      v
 Packet 1
 Packet 2
 Packet 3
   ...
 Packet N
      |
      v
Stop-and-Wait ARQ
      |
      v
Unreliable Network
      |
      +---- Packet Lost
      |         |
      |         v
      |     Timeout
      |         |
      |         v
      |    Retransmission
      |
      v
   Receiver
      |
      v
Packet Reassembly
      |
      v
Integrity Check
      |
      v
Reconstructed File
```

---

## Reliability Features

### Sequence Numbers

Every packet is assigned a sequence number beginning from `1`.

### Acknowledgements

The receiver sends an ACK after successfully receiving a packet.

### Timeout

If the sender does not receive an ACK within the configured timeout period, the packet is retransmitted.

### Retransmission

Lost DATA packets and packets whose ACKs are lost are retransmitted.

### Duplicate Detection

If a retransmitted packet reaches the receiver after the original packet was already received, it is identified as a duplicate.

### File Reassembly

Packets are sorted according to their sequence numbers and combined to reconstruct the original file.

### File Integrity

The reconstructed file is compared with the original file to verify that the transfer was successful.

---

## Performance Evaluation

The protocol was tested with different packet-loss rates.

### Test Configuration

- **Packet size:** `30 bytes`
- **Timeout:** `0.01 seconds`
- **Number of packets:** `21`

| Loss Rate | Packets | Total Transmissions | Retransmissions | Duplicate Packets | Completion Time | Integrity |
|:---------:|:-------:|:-------------------:|:---------------:|:-----------------:|:---------------:|:---------:|
| 0%  | 21 | 21  | 0  | 0  | 0.0000 s | PASS |
| 10% | 21 | 24  | 3  | 2  | 0.0316 s | PASS |
| 20% | 21 | 31  | 10 | 7  | 0.1047 s | PASS |
| 30% | 21 | 46  | 25 | 12 | 0.2647 s | PASS |
| 50% | 21 | 109 | 88 | 30 | 0.9133 s | PASS |

### Observation

As the packet-loss rate increases:

- The number of retransmissions increases.
- The number of duplicate packets increases.
- The completion time increases.
- More network transmissions are required.
- File integrity remains **PASS** because Stop-and-Wait ARQ provides reliable delivery.

---

## Example

For a `611 byte` file with a packet size of `30 bytes`:

```text
Number of packets = ceil(611 / 30)

                  = 21 packets
```

Therefore, the file is divided into **21 packets**.

The final packet contains the remaining **11 bytes**.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn

### Frontend

- React
- JavaScript
- Vite
- CSS

### Networking Concepts

- Packetization
- Sequence Numbers
- Acknowledgements
- Stop-and-Wait ARQ
- Timeout
- Retransmission
- Packet Loss
- Duplicate Detection
- File Reassembly
- Data Integrity

### Deployment

- Vercel — Frontend
- Render — Backend

---

## Project Structure

```text
ResilientFileTransfer/
│
├── backend/
│   │
│   ├── performance/
│   │   └── test_stop_and_wait_performance.py
│   │
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── ack.py
│   │   ├── network.py
│   │   └── packet.py
│   │
│   ├── transfer/
│   │   ├── __init__.py
│   │   ├── file_splitter.py
│   │   ├── reassembler.py
│   │   └── stop_and_wait.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── sample.txt
│   ├── test_network_transfer.py
│   ├── test_protocol.py
│   ├── test_reassembly.py
│   ├── test_splitter.py
│   └── test_stop_and_wait.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## Running the Backend Locally

Navigate to the backend directory:

```powershell
cd backend
```

### Create and Activate a Virtual Environment

For Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Start the FastAPI Server

```powershell
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend Locally

Navigate to the frontend directory:

```powershell
cd frontend
```

### Install Dependencies

```powershell
npm install
```

### Start the Development Server

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## API Endpoint

### Stop-and-Wait File Transfer

```text
POST /transfer/stop-and-wait
```

The endpoint accepts:

- File
- Loss rate
- Packet size
- Timeout

### Example Parameters

```text
loss_rate = 0.2
packet_size = 30
timeout = 0.01
```

The API returns information including:

- Filename
- File size
- Number of packets
- Loss rate
- Total transmissions
- Retransmissions
- Duplicate packets
- Completion time
- File integrity
- Transfer log

---

## Web Visualization

The frontend visually represents:

```text
Sender
   |
   | DATA
   v
Unreliable Network
   |
   v
Receiver
   |
   | ACK
   v
Sender
```

The interface displays:

- DATA packet movement
- ACK movement
- Lost packets
- Retransmissions
- Packet numbers
- Network status
- Transfer statistics
- File integrity result

This allows the reliability mechanism to be observed instead of only viewing numerical results.

---

## Testing

The project includes tests for major components such as:

- File splitting
- Packet reassembly
- Network transfer
- Stop-and-Wait protocol
- Protocol performance

### Example

From the `backend` directory:

```powershell
python test_protocol.py
```

Expected result includes:

```text
FILE INTEGRITY: PASS
```

---

## Limitations

This project is a **controlled simulation and implementation of reliable file transfer**, rather than a replacement for a real transport-layer protocol such as TCP.

The unreliable network is simulated in software using a configurable packet-loss rate.

The current implementation focuses on:

```text
Stop-and-Wait ARQ
```

rather than implementing a complete production-grade transport protocol.

---

## Future Enhancements

Possible future improvements include:

- Go-Back-N ARQ
- Selective Repeat ARQ
- Packet delay simulation
- Packet reordering simulation
- Congestion control
- Throughput analysis
- Bandwidth-delay analysis
- Real socket-based communication
- Wireshark traffic analysis
- More detailed performance graphs

---

## Project Outcome

The project demonstrates how reliability can be introduced over an unreliable packet-switched network using fundamental computer networking mechanisms.

Despite packet and ACK losses, the protocol successfully retransmits missing data and reconstructs the original file with verified integrity.

---

## Author

**Kalyani Vankoju**

Computer Science and Engineering  
GRIET

---

## License

This project is developed for academic and educational purposes.
