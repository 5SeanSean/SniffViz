# components/ui_builder.py
import tkinter as tk
from tkinter import ttk, scrolledtext, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import time

# Custom color scheme
COLORS = {
    "bg_dark": "#0a0a14",
    "bg_medium": "#121220",
    "bg_light": "#1a1a2e",
    "accent": "#00ff88",
    "accent_dark": "#00cc66",
    "text": "#ffffff",
    "text_secondary": "#aaaaaa",
    "border": "#2a2a4a",
    "success": "#00ff88",
    "warning": "#ffaa00",
    "error": "#ff5555",
    "info": "#00aaff"
}

class UIBuilder:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.buttons = {}
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        
        # Configure theme
        self.root.configure(bg=COLORS["bg_dark"])
        
        # Create custom styles
        style.configure("TFrame", background=COLORS["bg_dark"])
        style.configure("TLabel", background=COLORS["bg_dark"], foreground=COLORS["text"])
        style.configure("TButton", 
                        background=COLORS["bg_light"], 
                        foreground=COLORS["text"],
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor=COLORS["accent"])
        style.map("TButton",
                 background=[("active", COLORS["accent_dark"]), ("pressed", COLORS["accent"])],
                 foreground=[("active", COLORS["bg_dark"]), ("pressed", COLORS["bg_dark"])])
        
        style.configure("Accent.TButton", 
                        background=COLORS["accent"], 
                        foreground=COLORS["bg_dark"],
                        borderwidth=0,
                        font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                 background=[("active", COLORS["accent_dark"]), ("pressed", COLORS["accent"])],
                 foreground=[("active", COLORS["bg_dark"]), ("pressed", COLORS["bg_dark"])])
        
        style.configure("Title.TLabel", 
                        background=COLORS["bg_dark"], 
                        foreground=COLORS["accent"],
                        font=("Segoe UI", 12, "bold"))
        
        style.configure("Header.TFrame", background=COLORS["bg_medium"])
        style.configure("Card.TFrame", background=COLORS["bg_light"], relief="raised", borderwidth=1)
        
        # Configure treeview
        style.configure("Treeview",
                        background=COLORS["bg_light"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["bg_light"],
                        borderwidth=0,
                        font=("Consolas", 9))
        style.configure("Treeview.Heading",
                        background=COLORS["bg_medium"],
                        foreground=COLORS["accent"],
                        borderwidth=0,
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", COLORS["accent"])])
        
        # Configure scrollbars
        style.configure("Vertical.TScrollbar", 
                        background=COLORS["bg_medium"],
                        troughcolor=COLORS["bg_dark"],
                        borderwidth=0,
                        arrowsize=14)
        style.configure("Horizontal.TScrollbar", 
                        background=COLORS["bg_medium"],
                        troughcolor=COLORS["bg_dark"],
                        borderwidth=0,
                        arrowsize=14)
        
        # Configure notebook
        style.configure("TNotebook", background=COLORS["bg_dark"], borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=COLORS["bg_medium"],
                        foreground=COLORS["text_secondary"],
                        padding=[10, 4],
                        font=("Segoe UI", 9))
        style.map("TNotebook.Tab", 
                 background=[("selected", COLORS["bg_light"]), ("active", COLORS["bg_light"])],
                 foreground=[("selected", COLORS["accent"]), ("active", COLORS["accent"])])
        
    def create_main_panels(self):
        # Create header
        header = ttk.Frame(self.root, style="Header.TFrame", height=50)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = ttk.Label(header, text="CYBERSEC PACKET ANALYZER", style="Title.TLabel")
        title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Create main panels
        self.main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls and stats
        self.left_panel = ttk.Frame(self.main_panel, width=300, style="Card.TFrame")
        self.main_panel.add(self.left_panel, weight=1)
        
        # Right panel for packet list and visualizations
        self.right_panel = ttk.PanedWindow(self.main_panel, orient=tk.VERTICAL)
        self.main_panel.add(self.right_panel, weight=3)
        
    def create_controls_frame(self):
        # Controls
        control_frame = ttk.LabelFrame(self.left_panel, text="CAPTURE CONTROLS", padding=15)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Configure label frame style
        style = ttk.Style()
        style.configure("TLabelframe", background=COLORS["bg_light"], foreground=COLORS["accent"])
        style.configure("TLabelframe.Label", background=COLORS["bg_light"], foreground=COLORS["accent"])
        
        # Combined start/stop button
        self.capture_button = ttk.Button(control_frame, text="▶ Start Capture", width=20)
        self.capture_button.pack(fill=tk.X, pady=5)
        
        # Button container
        btn_container = ttk.Frame(control_frame)
        btn_container.pack(fill=tk.X, pady=5)
        
        self.buttons["load_sample"] = ttk.Button(btn_container, text="Load Sample")
        self.buttons["load_sample"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.buttons["clear_data"] = ttk.Button(btn_container, text="Clear Data")
        self.buttons["clear_data"].pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        self.buttons["export_report"] = ttk.Button(control_frame, text="Export Report")
        self.buttons["export_report"].pack(fill=tk.X, pady=5)
        
    def create_stats_frame(self):
        # Statistics
        stats_frame = ttk.LabelFrame(self.left_panel, text="STATISTICS", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame, 
            height=15, 
            width=35,
            bg=COLORS["bg_light"],
            fg=COLORS["text"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["bg_dark"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 9)
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
    def create_packet_list_frame(self):
        # Top right panel for packet list
        packet_list_panel = ttk.Frame(self.right_panel)
        self.right_panel.add(packet_list_panel, weight=2)
        
        # Packet list area
        packet_frame = ttk.LabelFrame(packet_list_panel, text="CAPTURED PACKETS", padding=15)
        packet_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for packet list
        columns = ("No", "Time", "Source", "Destination", "Protocol", "Length", "Info")
        self.packet_tree = ttk.Treeview(packet_frame, columns=columns, show="headings", height=15)
        
        # Define column headings and widths
        column_widths = [40, 80, 120, 120, 70, 60, 250]
        for col, width in zip(columns, column_widths):
            self.packet_tree.heading(col, text=col)
            self.packet_tree.column(col, width=width, minwidth=40)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(packet_frame, orient=tk.VERTICAL, command=self.packet_tree.yview)
        h_scrollbar = ttk.Scrollbar(packet_frame, orient=tk.HORIZONTAL, command=self.packet_tree.xview)
        self.packet_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.packet_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        packet_frame.grid_rowconfigure(0, weight=1)
        packet_frame.grid_columnconfigure(0, weight=1)
        
    def create_details_frame(self):
        # Bottom right panel for details
        details_panel = ttk.Frame(self.right_panel)
        self.right_panel.add(details_panel, weight=1)
        
        # Packet details area
        details_frame = ttk.LabelFrame(details_panel, text="PACKET DETAILS", padding=15)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.details_text = scrolledtext.ScrolledText(
            details_frame, 
            height=10,
            bg=COLORS["bg_light"],
            fg=COLORS["text"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["bg_dark"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 9)
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
    def create_visualizations_frame(self):
        # Visualization area
        viz_panel = ttk.Frame(self.right_panel)
        self.right_panel.add(viz_panel, weight=1)
        
        viz_frame = ttk.LabelFrame(viz_panel, text="VISUALIZATIONS", padding=15)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create notebook for different visualizations
        self.viz_notebook = ttk.Notebook(viz_frame)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.protocol_tab = ttk.Frame(self.viz_notebook)
        self.traffic_tab = ttk.Frame(self.viz_notebook)
        
        self.viz_notebook.add(self.protocol_tab, text="Protocol Distribution")
        self.viz_notebook.add(self.traffic_tab, text="Traffic Over Time")
        
        # Create figures for each tab
        self.setup_protocol_tab()
        self.setup_traffic_tab()
        
    def setup_protocol_tab(self):
        # Set dark theme for matplotlib
        plt.style.use('dark_background')
        
        self.protocol_fig, self.protocol_ax = plt.subplots(figsize=(8, 4), facecolor=COLORS["bg_light"])
        self.protocol_fig.patch.set_alpha(0.0)
        self.protocol_ax.set_facecolor(COLORS["bg_light"])
        
        # Customize colors
        self.protocol_ax.title.set_color(COLORS["accent"])
        self.protocol_ax.xaxis.label.set_color(COLORS["text_secondary"])
        self.protocol_ax.yaxis.label.set_color(COLORS["text_secondary"])
        self.protocol_ax.tick_params(colors=COLORS["text_secondary"])
        
        self.protocol_canvas = FigureCanvasTkAgg(self.protocol_fig, self.protocol_tab)
        self.protocol_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_traffic_tab(self):
        # Set dark theme for matplotlib
        plt.style.use('dark_background')
        
        self.traffic_fig, self.traffic_ax = plt.subplots(figsize=(8, 4), facecolor=COLORS["bg_light"])
        self.traffic_fig.patch.set_alpha(0.0)
        self.traffic_ax.set_facecolor(COLORS["bg_light"])
        
        # Customize colors
        self.traffic_ax.title.set_color(COLORS["accent"])
        self.traffic_ax.xaxis.label.set_color(COLORS["text_secondary"])
        self.traffic_ax.yaxis.label.set_color(COLORS["text_secondary"])
        self.traffic_ax.tick_params(colors=COLORS["text_secondary"])
        
        self.traffic_canvas = FigureCanvasTkAgg(self.traffic_fig, self.traffic_tab)
        self.traffic_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_status_bar(self):
        self.status_label = ttk.Label(
            self.root, 
            text="Status: Ready", 
            relief="flat", 
            anchor=tk.W,
            background=COLORS["bg_medium"],
            foreground=COLORS["text_secondary"],
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
    def bind_button(self, button_name, command):
        if button_name in self.buttons:
            self.buttons[button_name].config(command=command)
            
    def update_packet_list(self, packets, data_processor):
        """Update the packet list view"""
        # Clear existing items but keep the last few to avoid complete refresh
        current_items = self.packet_tree.get_children()
        if len(current_items) > 0:
            # Only update with new packets
            start_idx = len(current_items)
        else:
            start_idx = 0
            self.packet_tree.delete(*self.packet_tree.get_children())
        
        # Add new packets to the list
        for i in range(start_idx, len(packets)):
            packet = packets[i]
            time_str = datetime.fromtimestamp(packet['timestamp']).strftime('%H:%M:%S.%f')[:-3]
            src = packet.get('src_ip', 'N/A')
            dst = packet.get('dst_ip', 'N/A')
            protocol = packet.get('protocol', 'Unknown')
            length = packet.get('size', 0)
            info = data_processor.get_packet_info(packet)
            
            # Color code based on protocol
            tags = ()
            if protocol == 'TCP':
                tags = ('tcp',)
            elif protocol == 'UDP':
                tags = ('udp',)
            elif protocol == 'ICMP':
                tags = ('icmp',)
            elif protocol in ['HTTP', 'HTTPS']:
                tags = ('http',)
            elif protocol == 'DNS':
                tags = ('dns',)
                
            self.packet_tree.insert("", "end", values=(
                i+1, time_str, src, dst, protocol, length, info
            ), tags=tags)
            
        # Auto-scroll to the bottom
        if len(packets) > 0:
            self.packet_tree.see(self.packet_tree.get_children()[-1])
            
    def show_packet_details(self, packet, is_real_capture):
        """Display detailed information about the selected packet"""
        details = f"Packet Details:\n"
        details += "=" * 50 + "\n\n"
        
        details += f"Time: {datetime.fromtimestamp(packet['timestamp']).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}\n"
        details += f"Source: {packet.get('src_ip', 'N/A')}:{packet.get('src_port', 'N/A')}\n"
        details += f"Destination: {packet.get('dst_ip', 'N/A')}:{packet.get('dst_port', 'N/A')}\n"
        details += f"Protocol: {packet.get('protocol', 'Unknown')}\n"
        details += f"Length: {packet.get('size', 0)} bytes\n"
        
        # Add protocol-specific details
        protocol = packet.get('protocol', '')
        if protocol in ['TCP', 'UDP']:
            details += f"Source Port: {packet.get('src_port', 'N/A')}\n"
            details += f"Destination Port: {packet.get('dst_port', 'N/A')}\n"
            
        if protocol == 'TCP' and 'tcp_flags' in packet:
            flags = []
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
            details += f"TCP Flags: {', '.join(flags)}\n"
            
        # Add capture type info
        details += f"Capture Type: {'Real packets' if is_real_capture else 'Sample data'}\n"
            
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
        
    def update_statistics(self, packets, data_processor, is_real_capture):
        try:
            stats = data_processor.calculate_statistics(packets, is_real_capture)
            
            stats_text = "📊 REAL-TIME STATISTICS\n"
            stats_text += "=" * 30 + "\n\n"
            
            for key, value in stats.items():
                if isinstance(value, dict):
                    stats_text += f"🔹 {key}:\n"
                    for k, v in value.items():
                        stats_text += f"   {k}: {v}\n"
                    stats_text += "\n"
                else:
                    stats_text += f"🔹 {key}: {value}\n"
                    
            if not packets:
                stats_text = "📡 No packets captured yet.\n\nClick 'Start Capture' or 'Load Sample Data'"
                
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
        except Exception as e:
            print(f"Error updating statistics: {e}")
            
    def update_protocol_chart(self, packets, visualizations):
        try:
            visualizations.update_protocol_chart(packets, self.protocol_ax)
            self.protocol_canvas.draw()
        except Exception as e:
            print(f"Error updating protocol chart: {e}")
            
    def update_traffic_chart(self, packets, visualizations):
        try:
            visualizations.update_traffic_chart(packets, self.traffic_ax, self.traffic_fig)
            self.traffic_canvas.draw()
        except Exception as e:
            print(f"Error updating traffic chart: {e}")
            
    def clear_ui(self):
        self.packet_tree.delete(*self.packet_tree.get_children())
        self.details_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        
        # Clear charts
        self.protocol_ax.clear()
        self.protocol_ax.text(0.5, 0.5, 'No data available', 
                            horizontalalignment='center', verticalalignment='center',
                            color=COLORS["text_secondary"])
        self.protocol_canvas.draw()
        
        self.traffic_ax.clear()
        self.traffic_ax.text(0.5, 0.5, 'No data available', 
                            horizontalalignment='center', verticalalignment='center',
                            color=COLORS["text_secondary"])
        self.traffic_canvas.draw()