import random


class Network:
    def __init__(self, loss_rate=0.0):
        self.loss_rate = loss_rate

        self.topology = {
            "H1": ["R1"],
            "R1": ["H1", "R2"],
            "R2": ["R1", "R3"],
            "R3": ["R2", "H2"],
            "H2": ["R3"]
        }

    def send_packet(self, packet):
        # Decide whether the packet is lost
        if random.random() < self.loss_rate:
            return None

        # Packet successfully passes through the network
        return packet