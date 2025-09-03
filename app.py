# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
import threading

from components.ui_builder import UIBuilder
from components.capture_manager import CaptureManager
from components.data_processor import DataProcessor
from components.visualizations import Visualizations

class PacketCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberSec Packet Analyzer")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a14")
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Initialize components
        self.ui_builder = UIBuilder(self.root, self)
        self.capture_manager = CaptureManager(self)
        self.data_processor = DataProcessor()
        self.visualizations = Visualizations()
        
        # Packet storage
        self.packets = []
        self.capture_active = False
        self.is_real_capture = False
        self.last_ui_update = 0
        self.ui_update_interval = 1.0
        self.last_graph_update = 0
        self.graph_update_interval = 10.0
        
        # Create GUI
        self.setup_ui()
        self.bind_events()
        
        # Display scapy status
        if not self.capture_manager.SCAPY_AVAILABLE:
            self.ui_builder.status_label.config(
                text="Status: Scapy not available - using simulation mode", 
                foreground="#ffaa00"
            )
        
    def setup_ui(self):
        """Set up the user interface"""
        self.ui_builder.create_main_panels()
        self.ui_builder.create_controls_frame()
        self.ui_builder.create_stats_frame()
        self.ui_builder.create_packet_list_frame()
        self.ui_builder.create_details_frame()
        self.ui_builder.create_visualizations_frame()
        self.ui_builder.create_status_bar()
        
    def bind_events(self):
        """Bind UI events to handlers"""
        self.ui_builder.capture_button.config(command=self.toggle_capture)
        self.ui_builder.packet_tree.bind('<<TreeviewSelect>>', self.on_packet_select)
        
        # Bind menu buttons
        self.ui_builder.bind_button("load_sample", self.load_sample_data)
        self.ui_builder.bind_button("clear_data", self.clear_data)
        self.ui_builder.bind_button("export_report", self.export_report)
        
    def toggle_capture(self):
        """Toggle between start and stop capture"""
        if not self.capture_active:
            self.start_capture()
        else:
            self.stop_capture()
            
    def start_capture(self):
        self.capture_active = True
        self.is_real_capture = True
        self.ui_builder.capture_button.config(text="■ Stop Capture", style="Accent.TButton")
        self.ui_builder.status_label.config(
            text="Status: Capturing real packets..." if self.capture_manager.SCAPY_AVAILABLE 
            else "Status: Capturing simulated packets...", 
            foreground="#00ff88"
        )
        
        self.capture_manager.start_capture()
        
    def stop_capture(self):
        if self.capture_active:
            self.capture_active = False
            self.ui_builder.capture_button.config(text="▶ Start Capture", style="TButton")
            self.ui_builder.status_label.config(text="Status: Capture stopped", foreground="#00aaff")
            
    def load_sample_data(self):
        self.packets = self.capture_manager.load_sample_data()
        self.is_real_capture = False
        self.safe_update_ui()
        self.ui_builder.status_label.config(text="Status: Sample data loaded", foreground="#00ff88")
        
    def clear_data(self):
        self.packets = []
        self.ui_builder.packet_tree.delete(*self.ui_builder.packet_tree.get_children())
        self.ui_builder.details_text.delete(1.0, tk.END)
        self.safe_update_ui()
        self.is_real_capture = False
        self.ui_builder.status_label.config(text="Status: Data cleared", foreground="#00aaff")
        
    def export_report(self):
        if not self.packets:
            messagebox.showwarning("No Data", "No packets to export")
            return
            
        filename = f"packet_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w') as f:
                capture_type = "Real Packet Capture" if self.is_real_capture else "Sample Data"
                f.write(f"Packet Capture Report - {capture_type}\n")
                f.write("====================\n\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Total packets: {len(self.packets)}\n\n")
                
                # Add statistics
                stats = self.data_processor.calculate_statistics(self.packets, self.is_real_capture)
                for key, value in stats.items():
                    if isinstance(value, dict):
                        f.write(f"{key}:\n")
                        for k, v in value.items():
                            f.write(f"  {k}: {v}\n")
                    else:
                        f.write(f"{key}: {value}\n")
                        
                # Add packet list
                f.write("\n\nPacket List:\n")
                f.write("No.\tTime\tSource\tDestination\tProtocol\tLength\tInfo\n")
                for i, packet in enumerate(self.packets, 1):
                    time_str = datetime.fromtimestamp(packet['timestamp']).strftime('%H:%M:%S.%f')[:-3]
                    src = packet.get('src_ip', 'N/A')
                    dst = packet.get('dst_ip', 'N/A')
                    protocol = packet.get('protocol', 'Unknown')
                    length = packet.get('size', 0)
                    info = self.data_processor.get_packet_info(packet)
                    
                    f.write(f"{i}\t{time_str}\t{src}\t{dst}\t{protocol}\t{length}\t{info}\n")
                        
            self.ui_builder.status_label.config(text=f"Status: Report exported to {filename}", foreground="#00ff88")
            messagebox.showinfo("Export Successful", f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export report: {str(e)}")
            
    def on_packet_select(self, event):
        selection = self.ui_builder.packet_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        index = self.ui_builder.packet_tree.index(item)
        
        if 0 <= index < len(self.packets):
            packet = self.packets[index]
            self.ui_builder.show_packet_details(packet, self.is_real_capture)
            
    def safe_update_ui(self):
        """Safely update UI from any thread"""
        self.root.after(0, self.update_ui)
        
    def update_ui(self):
        """Update UI elements - must be called from main thread"""
        try:
            # Update packet list
            self.ui_builder.update_packet_list(self.packets, self.data_processor)
            
            # Update statistics
            self.ui_builder.update_statistics(self.packets, self.data_processor, self.is_real_capture)
            
            # Update visualizations only every 10 seconds
            current_time = time.time()
            if current_time - self.last_graph_update >= self.graph_update_interval:
                self.ui_builder.update_protocol_chart(self.packets, self.visualizations)
                self.ui_builder.update_traffic_chart(self.packets, self.visualizations)
                self.last_graph_update = current_time
        except Exception as e:
            print(f"Error updating UI: {e}")
            
    def add_packet(self, packet):
        """Add a packet to the storage and update UI if needed"""
        self.packets.append(packet)
        
        # Update UI at most once per second
        current_time = time.time()
        if current_time - self.last_ui_update >= self.ui_update_interval:
            self.safe_update_ui()
            self.last_ui_update = current_time