from transfer.file_splitter import split_file
from transfer.stop_and_wait import stop_and_wait_transfer
from transfer.reassembler import reassemble_file


original_file = "sample.txt"
reconstructed_file = "protocol_test_reconstructed.txt"


# Split the file into packets
packets = split_file(
    original_file,
    packet_size=30
)

print("Total packets:", len(packets))


# Run Stop-and-Wait protocol
result = stop_and_wait_transfer(
    packets,
    loss_rate=0.2,
    timeout=0.01
)


# Get received packets
received_packets = result["received_packets"]


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
print("STOP-AND-WAIT TEST")
print("-----------------------------")

print(
    "Total transmissions:",
    result["total_transmissions"]
)

print(
    "Retransmissions:",
    result["retransmissions"]
)

print(
    "Duplicate packets:",
    result["duplicate_packets"]
)

print(
    "Completion time:",
    round(result["completion_time"], 4),
    "seconds"
)


if original_data == reconstructed_data:
    print("FILE INTEGRITY: PASS ✓")
else:
    print("FILE INTEGRITY: FAIL ✗")