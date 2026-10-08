import time

from simulation.network import Network
from simulation.ack import Ack


def stop_and_wait_transfer(
    packets,
    loss_rate=0.2,
    timeout=1
):
    """
    Perform reliable file transfer using Stop-and-Wait ARQ.
    """

    network = Network(
        loss_rate=loss_rate
    )

    received_packets = []

    expected_sequence_number = 1

    total_transmissions = 0
    retransmissions = 0
    duplicate_packets = 0

    transfer_log = []

    start_time = time.time()

    # Stop-and-Wait ARQ
    for packet in packets:

        acknowledged = False

        while not acknowledged:

            total_transmissions += 1

            sequence_number = packet["sequence_number"]

            # Record DATA transmission
            transfer_log.append({
                "sequence_number": sequence_number,
                "event": "DATA_SENT"
            })

            # DATA travels through unreliable network
            result = network.send_packet(packet)

            if result is not None:

                # Receiver checks expected sequence number
                if sequence_number == expected_sequence_number:

                    received_packets.append(result)

                    expected_sequence_number += 1

                    transfer_log.append({
                        "sequence_number": sequence_number,
                        "event": "DATA_RECEIVED"
                    })

                else:

                    duplicate_packets += 1

                    transfer_log.append({
                        "sequence_number": sequence_number,
                        "event": "DUPLICATE_RECEIVED"
                    })

                # Receiver generates ACK
                ack = Ack(sequence_number)

                transfer_log.append({
                    "sequence_number": sequence_number,
                    "event": "ACK_GENERATED"
                })

                # ACK travels through unreliable network
                ack_result = network.send_packet(ack)

                if ack_result is not None:

                    transfer_log.append({
                        "sequence_number": sequence_number,
                        "event": "ACK_RECEIVED"
                    })

                    acknowledged = True

                else:

                    transfer_log.append({
                        "sequence_number": sequence_number,
                        "event": "ACK_LOST"
                    })

                    time.sleep(timeout)

                    retransmissions += 1

                    transfer_log.append({
                        "sequence_number": sequence_number,
                        "event": "TIMEOUT"
                    })

                    transfer_log.append({
                        "sequence_number": sequence_number,
                        "event": "RETRANSMISSION"
                    })

            else:

                transfer_log.append({
                    "sequence_number": sequence_number,
                    "event": "DATA_LOST"
                })

                time.sleep(timeout)

                retransmissions += 1

                transfer_log.append({
                    "sequence_number": sequence_number,
                    "event": "TIMEOUT"
                })

                transfer_log.append({
                    "sequence_number": sequence_number,
                    "event": "RETRANSMISSION"
                })

    end_time = time.time()

    completion_time = end_time - start_time

    return {
        "received_packets": received_packets,
        "total_transmissions": total_transmissions,
        "retransmissions": retransmissions,
        "duplicate_packets": duplicate_packets,
        "completion_time": completion_time,
        "transfer_log": transfer_log
    }