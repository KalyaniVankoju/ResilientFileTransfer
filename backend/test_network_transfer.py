from transfer.file_splitter import split_file
from transfer.reassembler import find_missing_packets, reassemble_file
from simulation.network import Network
original_file = "sample.txt"
reconstructed_file = "reconstructed.txt"
# Split file into packets
packets = split_file(
    original_file,
    packet_size=30
)

print("Total packets:", len(packets))


# Create unreliable network
network = Network(loss_rate=0.2)


received_packets = []
lost_packets = []


# Send every packet through the network
for packet in packets:

    result = network.send_packet(packet)

    if result is None:
        lost_packets.append(packet["sequence_number"])
    else:
        received_packets.append(result)


print("\nReceived packets:")

for packet in received_packets:
    print(packet["sequence_number"], end=" ")


print("\n\nLost packets:")

for sequence_number in lost_packets:
    print(sequence_number, end=" ")


print("\n\nPackets sent:", len(packets))
print("Packets received:", len(received_packets))
print("Packets lost:", len(lost_packets))
missing_packets = find_missing_packets(
    received_packets,
    len(packets)
)

print("\nMissing packets detected by receiver:")

for sequence_number in missing_packets:
    print(sequence_number, end=" ")

# Retransmit missing packets
print("\n\nRetransmitting missing packets...")

for sequence_number in missing_packets:

    # Find the original packet
    for packet in packets:

        if packet["sequence_number"] == sequence_number:

            result = network.send_packet(packet)

            if result is not None:
                received_packets.append(result)

                print(
                    "Packet",
                    sequence_number,
                    "retransmitted successfully"
                )

            else:
                print(
                    "Packet",
                    sequence_number,
                    "was lost again"
                )

            break
# Check again for missing packets
missing_packets = find_missing_packets(
    received_packets,
    len(packets)
)

print("\nMissing packets after retransmission:")

if not missing_packets:
    print("None")
else:
    for sequence_number in missing_packets:
        print(sequence_number, end=" ")


# Reassemble the file
reassemble_file(
    received_packets,
    reconstructed_file
)

print("\n\nFile reconstructed.")


# Verify file integrity
with open(original_file, "rb") as original:
    original_data = original.read()

with open(reconstructed_file, "rb") as reconstructed:
    reconstructed_data = reconstructed.read()


if original_data == reconstructed_data:
    print("FILE INTEGRITY: PASS ✓")
else:
    print("FILE INTEGRITY: FAIL ✗")