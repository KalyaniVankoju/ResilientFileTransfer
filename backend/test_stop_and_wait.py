import time

from transfer.file_splitter import split_file
from transfer.reassembler import reassemble_file
from simulation.network import Network
from simulation.ack import Ack


original_file = "sample.txt"
reconstructed_file = "reconstructed.txt"

LOSS_RATE = 0.2
TIMEOUT = 1


# Split the file into packets
packets = split_file(
    original_file,
    packet_size=30
)

print("Total packets:", len(packets))


# Create unreliable network
network = Network(
    loss_rate=LOSS_RATE
)


received_packets = []
expected_sequence_number = 1
total_transmissions = 0
retransmissions = 0
duplicate_packets = 0

# Start transfer timer
start_time = time.time()
# Stop-and-Wait ARQ
for packet in packets:

    acknowledged = False

    while not acknowledged:

        total_transmissions += 1

        sequence_number = packet["sequence_number"]

        print(
            f"\nSending Packet {sequence_number}..."
        )

        # DATA travels through unreliable network
        result = network.send_packet(packet)

        # Packet reached receiver
        if result is not None:

            print(
                f"Packet {sequence_number} received."
            )

            # Receiver checks the expected sequence number
            if sequence_number == expected_sequence_number:

                received_packets.append(result)

                print(
                    f"Packet {sequence_number} accepted by receiver."
                )

                # Move to the next expected packet
                expected_sequence_number += 1

            else:

                duplicate_packets += 1

                print(
                    f"Duplicate Packet {sequence_number} detected."
                )

            # Receiver creates ACK
            ack = Ack(sequence_number)

            print(
                f"Receiver generated ACK {sequence_number}."
            )

            # ACK travels through unreliable network
            ack_result = network.send_packet(ack)

            if ack_result is not None:

                print(
                    f"ACK {sequence_number} received by sender."
                )

                acknowledged = True

            else:

                print(
                    f"ACK {sequence_number} was lost."
                )

                print(
                    f"Waiting for ACK {sequence_number}..."
                )

                time.sleep(TIMEOUT)

                print(
                    f"TIMEOUT for Packet {sequence_number}."
                )

                retransmissions += 1

                print(
                    f"Retransmitting Packet {sequence_number}..."
                )

        # DATA packet was lost
        else:

            print(
                f"Packet {sequence_number} lost."
            )

            print(
                f"Waiting for ACK {sequence_number}..."
            )

            time.sleep(TIMEOUT)

            print(
                f"TIMEOUT for Packet {sequence_number}."
            )

            retransmissions += 1

            print(
                f"Retransmitting Packet {sequence_number}..."
            )

# End transfer timer
end_time = time.time()

completion_time = end_time - start_time
# Reassemble the file
reassemble_file(
    received_packets,
    reconstructed_file
)


# Verify file integrity
with open(original_file, "rb") as original:
    original_data = original.read()

with open(reconstructed_file, "rb") as reconstructed:
    reconstructed_data = reconstructed.read()


print("\n-----------------------------")
print("TRANSFER COMPLETE")
print("-----------------------------")

print(
    "Total transmissions:",
    total_transmissions
)

print(
    "Retransmissions:",
    retransmissions
)

print(
    "Duplicate packets:",
    duplicate_packets
)
print(
    "Completion time:",
    round(completion_time, 4),
    "seconds"
)


if original_data == reconstructed_data:
    print("FILE INTEGRITY: PASS ✓")
else:
    print("FILE INTEGRITY: FAIL ✗")