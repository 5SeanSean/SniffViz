# components/visualizations.py
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime
import random

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
}

class Visualizations:
    def update_protocol_chart(self, packets, ax):
        ax.clear()
        
        if not packets:
            ax.text(0.5, 0.5, 'No data available', 
                    horizontalalignment='center', verticalalignment='center',
                    color=COLORS["text_secondary"], fontsize=12)
            ax.set_frame_on(False)
            return
        
        protocols = [p.get('protocol', 'Unknown') for p in packets]
        protocol_counts = Counter(protocols)
        
        if protocol_counts:
            labels, values = zip(*protocol_counts.items())
            
            # Create a color palette
            colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
            
            # Explode the largest slice
            max_idx = values.index(max(values))
            explode = [0.1 if i == max_idx else 0 for i in range(len(labels))]
            
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=labels, 
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                explode=explode,
                shadow=True
            )
            
            # Style the text
            for text in texts:
                text.set_color(COLORS["text"])
                text.set_fontweight('bold')
                
            for autotext in autotexts:
                autotext.set_color(COLORS["bg_dark"])
                autotext.set_fontweight('bold')
            
            ax.set_title('Protocol Distribution', color=COLORS["accent"], fontweight='bold', fontsize=12)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            
    def update_traffic_chart(self, packets, ax, fig):
        ax.clear()
        
        if not packets:
            ax.text(0.5, 0.5, 'No data available', 
                    horizontalalignment='center', verticalalignment='center',
                    color=COLORS["text_secondary"], fontsize=12)
            ax.set_frame_on(False)
            return
            
        # Group packets by 10-second intervals
        time_groups = defaultdict(int)
        for packet in packets:
            # Group by 10-second intervals
            time_key = int(packet.get('timestamp', 0) / 10) * 10
            time_groups[time_key] += 1
            
        if time_groups:
            times, counts = zip(*sorted(time_groups.items()))
            
            # Convert timestamps to datetime for better x-axis labels
            time_labels = [datetime.fromtimestamp(t).strftime('%H:%M:%S') for t in times]
            
            # Create a gradient color based on packet count
            max_count = max(counts) if counts else 1
            colors = [plt.cm.viridis(count / max_count) for count in counts]
            
            # Create bar chart
            x_pos = np.arange(len(time_labels))
            bars = ax.bar(x_pos, counts, align='center', alpha=0.8, color=colors, edgecolor=COLORS["accent"], linewidth=1)
            
            # Add a line plot over the bars
            ax.plot(x_pos, counts, color=COLORS["accent"], linewidth=2, marker='o', markersize=4)
            
            # Set x-axis labels with rotation to prevent overlap
            ax.set_xticks(x_pos)
            ax.set_xticklabels(time_labels, rotation=45, ha='right', color=COLORS["text_secondary"])
            
            # Customize y-axis
            ax.tick_params(axis='y', colors=COLORS["text_secondary"])
            ax.set_ylabel('Packets per 10 seconds', color=COLORS["text_secondary"], fontweight='bold')
            
            # Set title
            ax.set_title('Network Traffic Over Time', color=COLORS["accent"], fontweight='bold', fontsize=12)
            
            # Add grid
            ax.grid(True, alpha=0.3, color=COLORS["border"])
            
            # Set facecolor
            ax.set_facecolor(COLORS["bg_light"])
            
            # Add a border
            for spine in ax.spines.values():
                spine.set_color(COLORS["border"])
                
            # Adjust layout to prevent label cutoff
            fig.tight_layout()