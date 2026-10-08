class Ack:
    def __init__(self, sequence_number):
        self.sequence_number = sequence_number

    def to_dict(self):
        return {
            "type": "ACK",
            "sequence_number": self.sequence_number
        }