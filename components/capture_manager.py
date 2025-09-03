# components/capture_manager.py
import threading
import time
import random
from datetime import datetime

# Try to import scapy, but provide fallback if not available
SCAPY_AVAILABLE = False
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Ether
    SCAPY_AVAILABLE = True
except ImportError:
    print("Scapy not available. Using simulated packet capture.")

class CaptureManager:
    def __init__(self, app):
        self.app = app
        self.SCAPY_AVAILABLE = SCAPY_AVAILABLE
        self.capture_thread = None
        
    def start_capture(self):
        if SCAPY_AVAILABLE:
            self.capture_thread = threading.Thread(target=self.capture_packets_scapy)
        else:
            self.capture_thread = threading.Thread(target=self.simulate_capture)
            
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
    def capture_packets_scapy(self):
        """Capture packets using Scapy"""
        def process_packet(packet):
            if self.app.capture_active:
                packet_info = {
                    'timestamp': time.time(),
                    'size': len(packet),
                    'src_ip': packet[IP].src if IP in packet else 'N/A',
                    'dst_ip': packet[IP].dst if IP in packet else 'N/A',
                }
                
                # Determine protocol
                if TCP in packet:
                    packet_info['protocol'] = 'TCP'
                    packet_info['src_port'] = packet[TCP].sport
                    packet_info['dst_port'] = packet[TCP].dport
                    packet_info['tcp_flags'] = packet[TCP].flags
                elif UDP in packet:
                    packet_info['protocol'] = 'UDP'
                    packet_info['src_port'] = packet[UDP].sport
                    packet_info['dst_port'] = packet[UDP].dport
                elif ICMP in packet:
                    packet_info['protocol'] = 'ICMP'
                    packet_info['icmp_type'] = packet[ICMP].type
                else:
                    packet_info['protocol'] = 'Other'
                    
                self.app.add_packet(packet_info)
                    
        try:
            sniff(prn=process_packet, store=0, stop_filter=lambda x: not self.app.capture_active)
        except Exception as e:
            self.app.root.after(0, lambda: self.app.ui_builder.status_label.config(
                text=f"Error: {str(e)}", foreground="red"))
            
    def simulate_capture(self):
        """Simulate packet capture for demonstration purposes"""
        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'SSH', 'FTP']
        sizes = [64, 128, 256, 512, 1024, 1280, 1500]
        src_ips = [f"192.168.1.{i}" for i in range(1, 50)]
        dst_ips = [f"10.0.0.{i}" for i in range(1, 50)] + ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
        
        while self.app.capture_active:
            # Create a mock packet
            mock_packet = {
                'protocol': random.choice(protocols),
                'size': random.choice(sizes),
                'timestamp': time.time(),
                'src_ip': random.choice(src_ips),
                'dst_ip': random.choice(dst_ips),
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([80, 443, 53, 22, 21, 25, 110])
            }
            
            # Add TCP flags for TCP packets
            if mock_packet['protocol'] == 'TCP':
                mock_packet['tcp_flags'] = random.choice([0x02, 0x10, 0x12, 0x18])  # SYN, ACK, SYN-ACK, PSH-ACK
            
            # Occasionally add some anomalous packets
            if random.random() < 0.05:  # 5% chance of anomaly
                mock_packet['size'] = random.randint(2000, 5000)  # Oversized packet
                
            self.app.add_packet(mock_packet)
            time.sleep(0.1)  # Simulate network delay
            
    def load_sample_data(self):
        """Generate sample data for demonstration"""
        packets = []
        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'SSH']
        sizes = [64, 128, 256, 512, 1024, 1500]
        src_ips = [f"192.168.1.{i}" for i in range(1, 20)]
        dst_ips = [f"10.0.0.{i}" for i in range(1, 20)] + ["8.8.8.8", "1.1.1.1"]
        
        base_time = time.time() - 3600  # Start from 1 hour ago
        
        for i in range(200):
            # Create a mock packet with various attributes
            mock_packet = {
                'protocol': random.choice(protocols),
                'size': random.choice(sizes),
                'timestamp': base_time + i * 18,  # Spread over 1 hour
                'src_ip': random.choice(src_ips),
                'dst_ip': random.choice(dst_ips),
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([80, 443, 53, 22, 21])
            }
            
            # Add TCP flags for TCP packets
            if mock_packet['protocol'] == 'TCP':
                mock_packet['tcp_flags'] = random.choice([0x02, 0x10, 0x12, 0x18])  # SYN, ACK, SYN-ACK, PSH-ACK
                
            packets.append(mock_packet)
            
        # Add some anomalies
        for i in range(5):
            anomaly_idx = random.randint(0, len(packets)-1)
            packets[anomaly_idx]['size'] = random.randint(2000, 5000)
            
        return packets