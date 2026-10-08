class Packet:
    def __init__(self, packet_id, source, destination, data):
        self.packet_id = packet_id
        self.source = source
        self.destination = destination
        self.data = data
        self.path = []
        self.status = "created"

    def add_hop(self, node):
        self.path.append(node)

    def to_dict(self):
        return {
            "packet_id": self.packet_id,
            "source": self.source,
            "destination": self.destination,
            "data": self.data,
            "path": self.path,
            "status": self.status
        }