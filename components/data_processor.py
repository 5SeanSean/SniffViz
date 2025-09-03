# components/data_processor.py
from collections import Counter, defaultdict
from datetime import datetime

class DataProcessor:
    def calculate_statistics(self, packets, is_real_capture):
        if not packets:
            return {"Total packets": 0}
            
        stats = {}
        stats["Total packets"] = len(packets)
        stats["Total data"] = f"{sum(p.get('size', 0) for p in packets) / 1024:.2f} KB"
        
        if packets:
            first_packet = min(p['timestamp'] for p in packets)
            last_packet = max(p['timestamp'] for p in packets)
            duration = last_packet - first_packet
            stats["Capture duration"] = f"{duration:.1f} seconds"
            stats["Packets/second"] = f"{len(packets) / duration:.1f}" if duration > 0 else "0"
        
        # Protocol distribution
        protocols = [p.get('protocol', 'Unknown') for p in packets]
        protocol_counts = Counter(protocols)
        stats["Protocol distribution"] = {k: f"{v} ({v/len(packets)*100:.1f}%)" 
                                         for k, v in protocol_counts.most_common()}
        
        # Top source IPs
        src_ips = [p.get('src_ip', '') for p in packets]
        src_ip_counts = Counter(src_ips)
        stats["Top source IPs"] = dict(src_ip_counts.most_common(5))
        
        # Top destination ports
        dst_ports = [str(p.get('dst_port', '')) for p in packets if p.get('dst_port')]
        dst_port_counts = Counter(dst_ports)
        stats["Top destination ports"] = dict(dst_port_counts.most_common(5))
        
        # Add capture type info
        stats["Capture type"] = "Real packets" if is_real_capture else "Sample data"
        
        return stats
        
    def get_packet_info(self, packet):
        """Generate info string for a packet"""
        protocol = packet.get('protocol', '')
        src_port = packet.get('src_port', '')
        dst_port = packet.get('dst_port', '')
        
        if protocol == 'TCP':
            flags = []
            if packet.get('tcp_flags'):
                if packet['tcp_flags'] & 0x02:  # SYN flag
                    flags.append("SYN")
                if packet['tcp_flags'] & 0x10:  # ACK flag
                    flags.append("ACK")
                if packet['tcp_flags'] & 0x01:  # FIN flag
                    flags.append("FIN")
                if packet['tcp_flags'] & 0x08:  # PSH flag
                    flags.append("PSH")
                if packet['tcp_flags'] & 0x04:  # RST flag
                    flags.append("RST")
            flag_str = "[" + " ".join(flags) + "]" if flags else ""
            return f"TCP {src_port} → {dst_port} {flag_str}"
        elif protocol == 'UDP':
            return f"UDP {src_port} → {dst_port}"
        elif protocol == 'ICMP':
            return f"ICMP {packet.get('icmp_type', '')}"
        elif protocol == 'HTTP':
            return "HTTP GET /"
        elif protocol == 'HTTPS':
            return "TLS Client Hello"
        elif protocol == 'DNS':
            return "DNS Standard query"
        else:
            return f"{protocol} packet"