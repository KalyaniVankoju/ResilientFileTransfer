from transfer.file_splitter import split_file
from transfer.reassembler import find_missing_packets, reassemble_file


original_file = "sample.txt"
reconstructed_file = "reconstructed.txt"


# Sender: split the file
packets = split_file(
    original_file,
    packet_size=30
)

total_packets = len(packets)

print("Total packets:", total_packets)


# TODO:
# Send packets through the unreliable network
# and store only the packets that were delivered.


# Receiver: detect missing packets
missing_packets = find_missing_packets(
    packets,
    total_packets
)

print("Missing packets:", missing_packets)