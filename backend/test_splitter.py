from transfer.file_splitter import split_file


file_path = "sample.txt"

packets = split_file(
    file_path,
    packet_size=30
)

print("Total packets:", len(packets))

for packet in packets:
    print(
        "Packet",
        packet["sequence_number"],
        "→",
        packet["data"]
    )