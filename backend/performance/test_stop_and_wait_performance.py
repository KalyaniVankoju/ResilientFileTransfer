import time
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from transfer.file_splitter import split_file
from transfer.reassembler import reassemble_file
from simulation.network import Network
from simulation.ack import Ack


original_file = "sample.txt"
reconstructed_file = "performance_reconstructed.txt"

PACKET_SIZE = 30
TIMEOUT = 0.01


def run_stop_and_wait(loss_rate):

    packets = split_file(
        original_file,
        packet_size=PACKET_SIZE
    )

    network = Network(
        loss_rate=loss_rate
    )

    received_packets = []

    expected_sequence_number = 1

    total_transmissions = 0
    retransmissions = 0
    duplicate_packets = 0

    start_time = time.time()

    # Stop-and-Wait ARQ
    for packet in packets:

        acknowledged = False

        while not acknowledged:

            total_transmissions += 1

            sequence_number = packet["sequence_number"]

            # DATA travels through unreliable network
            result = network.send_packet(packet)

            if result is not None:

                # Receiver checks expected sequence number
                if sequence_number == expected_sequence_number:

                    received_packets.append(result)

                    expected_sequence_number += 1

                else:

                    duplicate_packets += 1

                # Receiver generates ACK
                ack = Ack(sequence_number)

                # ACK travels through unreliable network
                ack_result = network.send_packet(ack)

                if ack_result is not None:

                    acknowledged = True

                else:

                    time.sleep(TIMEOUT)

                    retransmissions += 1

            else:

                time.sleep(TIMEOUT)

                retransmissions += 1

    end_time = time.time()

    completion_time = end_time - start_time

    # Reassemble received packets
    reassemble_file(
        received_packets,
        reconstructed_file
    )

    # Verify file integrity
    with open(original_file, "rb") as original:
        original_data = original.read()

    with open(reconstructed_file, "rb") as reconstructed:
        reconstructed_data = reconstructed.read()

    integrity = original_data == reconstructed_data

    return {
        "loss_rate": loss_rate,
        "packets": len(packets),
        "transmissions": total_transmissions,
        "retransmissions": retransmissions,
        "duplicates": duplicate_packets,
        "completion_time": completion_time,
        "integrity": integrity
    }


# Test different loss rates
loss_rates = [
    0.0,
    0.1,
    0.2,
    0.3,
    0.5
]


print("\nSTOP-AND-WAIT PERFORMANCE TEST")
print("=" * 70)


for loss_rate in loss_rates:

    result = run_stop_and_wait(loss_rate)

    print(
        f"\nLoss Rate: {result['loss_rate'] * 100:.0f}%"
    )

    print(
        f"Packets: {result['packets']}"
    )

    print(
        f"Total Transmissions: {result['transmissions']}"
    )

    print(
        f"Retransmissions: {result['retransmissions']}"
    )

    print(
        f"Duplicate Packets: {result['duplicates']}"
    )

    print(
        f"Completion Time: "
        f"{result['completion_time']:.4f} seconds"
    )

    print(
        f"File Integrity: "
        f"{'PASS' if result['integrity'] else 'FAIL'}"
    )