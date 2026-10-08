def split_file(file_path, packet_size=1024):
    packets = []

    with open(file_path, "rb") as file:
        sequence_number = 1

        while True:
            data = file.read(packet_size)

            if not data:
                break

            packet = {
                "sequence_number": sequence_number,
                "data": data
            }

            packets.append(packet)

            sequence_number += 1

    return packets