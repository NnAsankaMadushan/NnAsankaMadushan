import os
import sys

def main():
    preview = os.environ.get("PREVIEW") == "1"

    ROWS = [
        ("user", "nnamadushan@gmail.com"),
        ("role", "Full Stack / Mobile Developer"),
        ("focus", "Frontend, Mobile & Systems"),
        ("stack", "React · Flutter · Node · PHP"),
        ("now", "Building clean-architecture apps"),
        ("school", "BSc Eng - University of Ruhuna"),
        ("loc", "Sri Lanka"),
    ]

    width = 460
    row_height = 30
    padding = 20
    header_height = 40
    height = header_height + (len(ROWS) * row_height) + padding + 10

    svg = []
    svg.append('<?xml version="1.0" encoding="utf-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append('  <style>')
    svg.append('    .panel { font-family: "JetBrains Mono", Consolas, "Liberation Mono", monospace; font-size: 13px; }')
    svg.append('    .title { fill: #8892B0; font-weight: bold; }')
    svg.append('    .key { fill: #00FFD1; font-weight: bold; }')
    svg.append('    .val { fill: #E4F0FB; }')
    svg.append('    .chrome { fill: #1E1E2E; }')
    svg.append('    .dot { rx: 5; ry: 5; width: 10px; height: 10px; }')
    if not preview:
        # Typing animations for each row
        svg.append('    .row { opacity: 0; animation: fade-in 0.5s ease forwards; }')
        svg.append('    @keyframes fade-in { to { opacity: 1; } }')
    svg.append('  </style>')
    
    # Background card
    svg.append(f'  <rect width="{width}" height="{height}" fill="#0D0D0D" rx="8" stroke="#1E1E2E" stroke-width="1.5" />')
    
    # Terminal Header (Chrome)
    svg.append(f'  <path d="M 0,8 A 8,8 0 0,1 8,0 L {width-8},0 A 8,8 0 0,1 {width},8 L {width},{header_height} L 0,{header_height} Z" fill="#16161E" />')
    
    # Window controls (red, yellow, green dots)
    svg.append('  <circle cx="20" cy="20" r="6" fill="#FF5F56" />')
    svg.append('  <circle cx="40" cy="20" r="6" fill="#FFBD2E" />')
    svg.append('  <circle cx="60" cy="20" r="6" fill="#27C93F" />')
    
    # Terminal Title
    title_text = "NnAsankaMadushan ~ whoami"
    svg.append(f'  <text x="{width/2}" y="25" class="panel title" text-anchor="middle">{title_text}</text>')
    
    # Render rows
    for idx, (k, v) in enumerate(ROWS):
        y_pos = header_height + padding + (idx * row_height)
        delay = idx * 200
        style_attr = f' class="row" style="animation-delay: {delay}ms;"' if not preview else ''
        
        svg.append(f'  <g{style_attr}>')
        # Prompt character
        svg.append(f'    <text x="20" y="{y_pos}" class="panel key">◈ {k}:</text>')
        # Value
        svg.append(f'    <text x="130" y="{y_pos}" class="panel val">{v}</text>')
        svg.append('  </g>')
        
    svg.append('</svg>')

    with open("sysinfo.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print("Successfully rendered sysinfo.svg")

if __name__ == "__main__":
    main()
