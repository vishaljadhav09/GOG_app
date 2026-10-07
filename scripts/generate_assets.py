import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs("resources", exist_ok=True)

# Colors from Guardians of Gaia Design System
CREAM = (245, 239, 224)
CREAM_DK = (234, 224, 200)
INK = (26, 26, 26)
LIME = (201, 242, 61)
PINK = (255, 61, 138)
TANGERINE = (255, 138, 61)
COBALT = (46, 94, 232)
LAVENDER = (182, 166, 255)
WHITE = (255, 253, 248)

def draw_neo_owl(draw, cx, cy, scale):
    """Draws a cute, neo-brutalist cartoon owl."""
    r = int(180 * scale)
    shadow_offset = int(16 * scale)
    
    # 1. Hard Drop Shadow for Owl Body
    draw.ellipse([cx - r + shadow_offset, cy - r + shadow_offset, cx + r + shadow_offset, cy + r + shadow_offset], fill=INK)
    
    # 2. Owl Body
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TANGERINE, outline=INK, width=int(12 * scale))
    
    # 3. Owl Belly (Cream patch)
    belly_r = int(120 * scale)
    belly_cy = cy + int(40 * scale)
    draw.ellipse([cx - belly_r, belly_cy - belly_r, cx + belly_r, belly_cy + belly_r], fill=CREAM, outline=INK, width=int(8 * scale))
    
    # Feather V-patterns on belly
    for dx, dy in [(-30, 20), (30, 20), (0, 60)]:
        px, py = cx + int(dx * scale), belly_cy + int(dy * scale)
        s = int(15 * scale)
        draw.line([px - s, py - s, px, py], fill=INK, width=int(6 * scale))
        draw.line([px, py, px + s, py - s], fill=INK, width=int(6 * scale))
        
    # 4. Owl Ear Tufts (Left & Right)
    tuft_l = [(cx - int(130 * scale), cy - int(110 * scale)), (cx - int(170 * scale), cy - int(210 * scale)), (cx - int(70 * scale), cy - int(150 * scale))]
    tuft_r = [(cx + int(130 * scale), cy - int(110 * scale)), (cx + int(170 * scale), cy - int(210 * scale)), (cx + int(70 * scale), cy - int(150 * scale))]
    draw.polygon(tuft_l, fill=TANGERINE, outline=INK)
    draw.polygon(tuft_r, fill=TANGERINE, outline=INK)
    
    # 5. Big Eyes
    eye_r = int(65 * scale)
    eye_lx, eye_rx = cx - int(65 * scale), cx + int(65 * scale)
    eye_y = cy - int(35 * scale)
    
    # Eye shadows & white backgrounds
    for ex in [eye_lx, eye_rx]:
        draw.ellipse([ex - eye_r, eye_y - eye_r, ex + eye_r, eye_y + eye_r], fill=WHITE, outline=INK, width=int(10 * scale))
        # Large Pupil
        pupil_r = int(35 * scale)
        draw.ellipse([ex - pupil_r, eye_y - pupil_r, ex + pupil_r, eye_y + pupil_r], fill=INK)
        # Catchlight / Shine
        shine_r = int(12 * scale)
        draw.ellipse([ex - pupil_r + int(10 * scale), eye_y - pupil_r + int(10 * scale), ex - pupil_r + int(10 * scale) + shine_r * 2, eye_y - pupil_r + int(10 * scale) + shine_r * 2], fill=WHITE)

    # 6. Beak
    beak = [(cx, cy + int(35 * scale)), (cx - int(25 * scale), cy - int(5 * scale)), (cx + int(25 * scale), cy - int(5 * scale))]
    draw.polygon(beak, fill=LIME, outline=INK)

def generate_icon():
    size = 1024
    img = Image.new("RGBA", (size, size), CREAM)
    draw = ImageDraw.Draw(img)
    
    # Background Badge (Neo-brutalist squircle/circle)
    bg_r = 460
    bg_cx, bg_cy = 512, 512
    sh = 24
    draw.ellipse([bg_cx - bg_r + sh, bg_cy - bg_r + sh, bg_cx + bg_r + sh, bg_cy + bg_r + sh], fill=INK)
    draw.ellipse([bg_cx - bg_r, bg_cy - bg_r, bg_cx + bg_r, bg_cy + bg_r], fill=LIME, outline=INK, width=16)
    
    # Draw Owl in center
    draw_neo_owl(draw, 512, 512, scale=1.8)
    
    img.save("resources/icon.png")
    print("Generated resources/icon.png (1024x1024)")

def generate_splash():
    size = 2732
    img = Image.new("RGBA", (size, size), CREAM)
    draw = ImageDraw.Draw(img)
    
    # Background dots pattern
    for x in range(50, size, 120):
        for y in range(50, size, 120):
            draw.ellipse([x, y, x + 8, y + 8], fill=(26, 26, 26, 30))
            
    # Center neo-brutalist card
    cw, ch = 1800, 1800
    cx, cy = size // 2, size // 2
    sh = 40
    
    # Card shadow & background
    draw.rectangle([cx - cw//2 + sh, cy - ch//2 + sh, cx + cw//2 + sh, cy + ch//2 + sh], fill=INK)
    draw.rectangle([cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], fill=WHITE, outline=INK, width=24)
    
    # Inner badge
    b_r = 550
    draw.ellipse([cx - b_r + 20, cy - b_r + 20, cx + b_r + 20, cy + b_r + 20], fill=INK)
    draw.ellipse([cx - b_r, cy - b_r, cx + b_r, cy + b_r], fill=LAVENDER, outline=INK, width=20)
    
    # Owl Character
    draw_neo_owl(draw, cx, cy, scale=2.3)
    
    img.save("resources/splash.png")
    print("Generated resources/splash.png (2732x2732)")

if __name__ == "__main__":
    generate_icon()
    generate_splash()
