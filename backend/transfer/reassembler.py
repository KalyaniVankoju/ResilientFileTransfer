def find_missing_packets(packets, total_packets):
    received_numbers = {
        packet["sequence_number"]
        for packet in packets
    }

    missing_packets = []

    for sequence_number in range(1, total_packets + 1):
        if sequence_number not in received_numbers:
            missing_packets.append(sequence_number)

    return missing_packets


def reassemble_file(packets, output_path):
    # Arrange packets according to sequence number
    packets = sorted(
        packets,
        key=lambda packet: packet["sequence_number"]
    )

    with open(output_path, "wb") as file:
        for packet in packets:
            file.write(packet["data"])