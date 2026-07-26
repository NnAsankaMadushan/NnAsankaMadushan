import os
import sys
import json
from datetime import datetime

def main():
    json_path = "assets/contributions.json"
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist. Run pull_contributions.py first.")
        sys.exit(1)
        
    with open(json_path, "r") as f:
        data = json.load(f)
        
    contributions = data["contributions"]
    total = data["total"]
    current_streak = data["current_streak"]
    longest_streak = data["longest_streak"]
    busiest_day = data["busiest_day"]
    
    # Grid settings
    box_size = 10
    gap = 3
    padding_top = 30
    padding_left = 35
    padding_bottom = 45
    
    # Group contributions into weeks (columns)
    # Each contribution needs to be mapped to the correct grid position
    # The contribution HTML list usually starts on a Sunday/Monday and ends on a Saturday/Sunday
    # Let's chunk the list into lists of up to 7 items.
    # Note: GitHub calendar has columns representing weeks.
    weeks = []
    current_week = []
    
    # We want to align the days by weekday. 
    # Let's group them sequentially into chunks of 7.
    for d in contributions:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)
        
    # Cap to max 53 weeks to fit in the panel cleanly
    weeks = weeks[-53:]
    
    width = padding_left + (len(weeks) * (box_size + gap)) + 20
    height = padding_top + (7 * (box_size + gap)) + padding_bottom
    
    # Custom color ramp (neon theme matching Asanka's profile)
    LEVELS = ["#16161E", "#004F4D", "#008F87", "#00BFB2", "#00FFD1"]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append('  <style>')
    svg.append('    .text { font-family: "JetBrains Mono", Consolas, monospace; font-size: 9px; fill: #8892B0; }')
    svg.append('    .stat-text { font-family: "JetBrains Mono", Consolas, monospace; font-size: 11px; fill: #E4F0FB; font-weight: bold; }')
    svg.append('    .stat-label { fill: #8892B0; }')
    svg.append('    .rect { rx: 2; ry: 2; opacity: 0; animation: scale-up 0.5s ease forwards; transform-origin: center; }')
    svg.append('    @keyframes scale-up { to { opacity: 1; } }')
    svg.append('  </style>')
    
    # Background
    svg.append(f'  <rect width="{width}" height="{height}" fill="#0D0D0D" rx="8" stroke="#1E1E2E" stroke-width="1.5" />')
    
    # Weekday labels (Mon, Wed, Fri)
    labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for label, day_idx in labels:
        y_pos = padding_top + day_idx * (box_size + gap) + 8
        svg.append(f'  <text x="10" y="{y_pos}" class="text">{label}</text>')
        
    # Render contributions grid
    for w_idx, week in enumerate(weeks):
        # Stagger by column (week) - 25ms per week
        delay = w_idx * 25
        for d_idx, day in enumerate(week):
            level = min(max(day["level"], 0), 4)
            color = LEVELS[level]
            
            x = padding_left + w_idx * (box_size + gap)
            y = padding_top + d_idx * (box_size + gap)
            
            # Use SVG inline transform-origin logic or simplified coordinates for safety
            cx = x + box_size / 2
            cy = y + box_size / 2
            
            svg.append(
                f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
                f'fill="{color}" class="rect" '
                f'style="animation-delay: {delay}ms; transform-origin: {cx}px {cy}px;" />'
            )
            
    # Bottom Stats Bar
    stats_y = height - 20
    # Legend
    legend_start_x = width - 110
    svg.append(f'  <text x="{legend_start_x - 30}" y="{stats_y + 8}" class="text">Less</text>')
    for l_idx, color in enumerate(LEVELS):
        lx = legend_start_x + l_idx * 14
        ly = stats_y
        svg.append(f'  <rect x="{lx}" y="{ly}" width="10" height="10" fill="{color}" rx="1.5" />')
    svg.append(f'  <text x="{legend_start_x + 5 * 14}" y="{stats_y + 8}" class="text">More</text>')
    
    # Stats Summary
    svg.append(f'  <text x="15" y="{stats_y + 8}" class="stat-text">')
    svg.append(f'    <tspan class="stat-label">Total: </tspan>{total}')
    svg.append(f'    <tspan class="stat-label">  Streak: </tspan>{current_streak} days')
    svg.append(f'    <tspan class="stat-label">  Max Streak: </tspan>{longest_streak} days')
    svg.append(f'    <tspan class="stat-label">  Busiest: </tspan>{busiest_day}')
    svg.append('  </text>')
    
    svg.append('</svg>')
    
    with open("graph.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print("Successfully rendered graph.svg")

if __name__ == "__main__":
    main()
