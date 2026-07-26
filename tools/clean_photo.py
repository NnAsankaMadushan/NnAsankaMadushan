import sys
import os
import cv2
import numpy as np

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_photo.py <path_to_photo>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)
        
    print(f"Processing {input_path}...")
    
    # 1. Try background removal with rembg
    try:
        from rembg import remove
        from PIL import Image
        
        print("Removing background using rembg...")
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        
        # Convert to numpy array
        img_np = np.array(output_image)
        # Separate alpha channel
        if img_np.shape[2] == 4:
            alpha = img_np[:, :, 3]
            rgb = img_np[:, :, :3]
            # Replace background with white where alpha is 0
            white_bg = np.ones_like(rgb) * 255
            mask = alpha[:, :, np.newaxis] / 255.0
            img_cleaned = (rgb * mask + white_bg * (1 - mask)).astype(np.uint8)
        else:
            img_cleaned = rgb
    except Exception as e:
        print(f"Note: rembg failed or not installed ({e}). Proceeding with standard grayscale conversion.")
        img_cleaned = cv2.imread(input_path)

    # 2. Convert to Grayscale
    if len(img_cleaned.shape) == 3:
        gray = cv2.cvtColor(img_cleaned, cv2.cvtColor_to_code if 'cvtColor_to_code' in dir(cv2) else cv2.COLOR_BGR2GRAY)
    else:
        gray = img_cleaned

    # 3. Even out lighting using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray_equalized = clahe.apply(gray)

    # 4. Save output
    os.makedirs("assets", exist_ok=True)
    output_path = "assets/photo-ready.png"
    cv2.imwrite(output_path, gray_equalized)
    print(f"Successfully saved cleaned photo to {output_path}")

if __name__ == "__main__":
    main()
