import os
import sys
from PIL import Image

def main():
    # Check if a custom path was passed as an argument
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        src_path = sys.argv[1]
        print(f"Using custom image: {src_path}")
    else:
        # Fallback paths for profile picture
        src_path = "assets/photo-ready.png"
        if not os.path.exists(src_path):
            if os.path.exists("Profile.png"):
                src_path = "Profile.png"
                print("assets/photo-ready.png not found, using Profile.png instead.")
            else:
                print("Error: source image not found.")
                sys.exit(1)

    # Open image
    img = Image.open(src_path).convert("L")
    
    # Calculate target dimensions
    # ASCII portrait dimensions (e.g. 50 cols, height adjusted for font aspect ratio ~ 0.5)
    cols = 65
    width, height = img.size
    aspect_ratio = height / width
    # 0.55 corrects the vertical stretch of typical monospace fonts
    rows = int(cols * aspect_ratio * 0.55)
    
    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
    
    GLYPHS = " '.,:;~+*xXO#"
    max_val = 255
    
    ascii_rows = []
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            val = img_resized.getpixel((c, r))
            # Invert so white background becomes empty space (GLYPHS[0] = ' ')
            # If val is 255, we want index 0. If val is 0, we want index len(GLYPHS)-1
            idx = int((255 - val) / 255.0 * (len(GLYPHS) - 1))
            row_str += GLYPHS[idx]
        # Replace spaces with non-breaking spaces for XML/SVG rendering safety
        row_str = row_str.replace(" ", "&#160;")
        ascii_rows.append(row_str)
        
    # Generate SVG content
    # Monospace font styling, terminal look
    font_size = 11
    line_height = 13
    svg_width = cols * 7
    svg_height = rows * line_height + 20
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">')
    svg.append('  <style>')
    svg.append('    .ascii {')
    svg.append('      font-family: "Courier New", Courier, monospace;')
    svg.append('      font-size: 11px;')
    svg.append('      font-weight: bold;')
    svg.append('      fill: #00FFD1;')
    svg.append('    }')
    svg.append('    .reveal {')
    svg.append('      animation: draw 0.8s steps(10, end) forwards;')
    svg.append('      opacity: 0;')
    svg.append('    }')
    svg.append('    @keyframes draw {')
    svg.append('      to { opacity: 1; }')
    svg.append('    }')
    svg.append('  </style>')
    svg.append('  <rect width="100%" height="100%" fill="#0D0D0D" rx="8" />')
    svg.append('  <text x="15" y="20" class="ascii">')
    
    for idx, row in enumerate(ascii_rows):
        # Stagger the lines by 35ms each
        delay = idx * 35
        y_pos = 35 + (idx * line_height)
        svg.append(f'    <tspan x="15" y="{y_pos}" class="reveal" style="animation-delay: {delay}ms;">{row}</tspan>')
        
    svg.append('  </text>')
    svg.append('</svg>')
    
    os.makedirs("assets", exist_ok=True)
    with open("portrait.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print("Successfully rendered portrait.svg")

if __name__ == "__main__":
    main()
