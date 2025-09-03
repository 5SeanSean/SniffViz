# models/packet.py
class Packet:
    def __init__(self, timestamp, size, src_ip, dst_ip, protocol, 
                 src_port=None, dst_port=None, tcp_flags=None, icmp_type=None):
        self.timestamp = timestamp
        self.size = size
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.protocol = protocol
        self.src_port = src_port
        self.dst_port = dst_port
        self.tcp_flags = tcp_flags
        self.icmp_type = icmp_type
        
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'size': self.size,
            'src_ip': self.src_ip,
            'dst_ip': self.dst_ip,
            'protocol': self.protocol,
            'src_port': self.src_port,
            'dst_port': self.dst_port,
            'tcp_flags': self.tcp_flags,
            'icmp_type': self.icmp_type
        }