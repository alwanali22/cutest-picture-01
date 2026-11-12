# Teacup Red Panda - tiny red panda cub in a teacup (final)
import struct
import zlib
import math
import os

# Colors (R, G, B)
COLOR_BG = (255, 241, 230)
COLOR_GLOW = (255, 218, 185)
COLOR_CUP = (168, 213, 186)
COLOR_CUP_DARK = (137, 184, 157)
COLOR_RUSSET = (199, 91, 42)
COLOR_RUSSET_DARK = (161, 74, 34)
COLOR_CREAM = (255, 248, 225)
COLOR_CREAM_DARK = (224, 216, 193)
COLOR_EYE = (62, 39, 35)
COLOR_PINK = (255, 182, 193)
COLOR_YELLOW = (255, 215, 0)
COLOR_ORANGE = (255, 165, 0)

WIDTH, HEIGHT = 1024, 1024
SS = 2
SS_WIDTH, SS_HEIGHT = WIDTH * SS, HEIGHT * SS

buffer = bytearray(SS_WIDTH * SS_HEIGHT * 4)

def set_pixel(x, y, r, g, b):
    if 0 <= x < SS_WIDTH and 0 <= y < SS_HEIGHT:
        idx = (y * SS_WIDTH + x) * 4
        buffer[idx] = r
        buffer[idx + 1] = g
        buffer[idx + 2] = b
        buffer[idx + 3] = 255

def draw_circle(cx, cy, r, color, outline_color=None, thickness=2):
    if outline_color:
        for y in range(cy - r - thickness, cy + r + thickness + 1):
            for x in range(cx - r - thickness, cx + r + thickness + 1):
                if (x - cx)**2 + (y - cy)**2 <= (r + thickness)**2:
                    set_pixel(x, y, *outline_color)
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx)**2 + (y - cy)**2 <= r**2:
                set_pixel(x, y, *color)

def draw_ellipse(cx, cy, rx, ry, color, outline_color=None, thickness=2):
    if outline_color:
        for y in range(cy - ry - thickness, cy + ry + thickness + 1):
            for x in range(cx - rx - thickness, cx + rx + thickness + 1):
                if ((x - cx)**2 / (rx + thickness)**2) + ((y - cy)**2 / (ry + thickness)**2) <= 1:
                    set_pixel(x, y, *outline_color)
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx)**2 / rx**2) + ((y - cy)**2 / ry**2) <= 1:
                set_pixel(x, y, *color)

def draw_line(x1, y1, x2, y2, color, thickness=1):
    steps = max(abs(x2 - x1), abs(y2 - y1))
    for i in range(steps + 1):
        x = x1 + (x2 - x1) * i // steps
        y = y1 + (y2 - y1) * i // steps
        for dx in range(-thickness, thickness+1):
            for dy in range(-thickness, thickness+1):
                set_pixel(x+dx, y+dy, *color)

def draw_background():
    for y in range(SS_HEIGHT):
        for x in range(SS_WIDTH):
            dist = math.sqrt((x - SS_WIDTH/2)**2 + (y - SS_HEIGHT/2)**2)
            alpha = max(0, 1 - dist / (SS_WIDTH/2))
            r = int(COLOR_BG[0] + (COLOR_GLOW[0] - COLOR_BG[0]) * alpha)
            g = int(COLOR_BG[1] + (COLOR_GLOW[1] - COLOR_BG[1]) * alpha)
            b = int(COLOR_BG[2] + (COLOR_GLOW[2] - COLOR_BG[2]) * alpha)
            set_pixel(x, y, r, g, b)

def save_png(filename):
    final_buffer = bytearray(WIDTH * HEIGHT * 4)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = 0, 0, 0
            for sy in range(SS):
                for sx in range(SS):
                    idx = ((y * SS + sy) * SS_WIDTH + (x * SS + sx)) * 4
                    r += buffer[idx]
                    g += buffer[idx + 1]
                    b += buffer[idx + 2]
            
            idx = (y * WIDTH + x) * 4
            final_buffer[idx] = r // (SS * SS)
            final_buffer[idx + 1] = g // (SS * SS)
            final_buffer[idx + 2] = b // (SS * SS)
            final_buffer[idx + 3] = 255

    png = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', WIDTH, HEIGHT, 8, 6, 0, 0, 0)
    png += struct.pack('>I4s', len(ihdr), b'IHDR') + ihdr + struct.pack('>I', zlib.crc32(b'IHDR' + ihdr) & 0xffffffff)
    
    raw_data = bytearray()
    for y in range(HEIGHT):
        raw_data.append(0)
        raw_data.extend(final_buffer[y * WIDTH * 4 : (y + 1) * WIDTH * 4])
    
    compressed_data = zlib.compress(raw_data)
    png += struct.pack('>I4s', len(compressed_data), b'IDAT') + compressed_data + struct.pack('>I', zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff)
    png += struct.pack('>I4s', 0, b'IEND') + struct.pack('>I', zlib.crc32(b'IEND') & 0xffffffff)
    
    with open(filename, 'wb') as f: f.write(png)

def main():
    draw_background()
    
    # Stars
    draw_circle(200, 200, 15, COLOR_CREAM)
    draw_circle(1700, 300, 15, COLOR_YELLOW)
    
    # Sauce & Cup
    draw_ellipse(SS_WIDTH//2, 1750, 400, 100, COLOR_CUP, COLOR_CUP_DARK)
    draw_ellipse(SS_WIDTH//2, 1450, 300, 250, COLOR_CUP, COLOR_CUP_DARK)
    # Cup handle
    draw_ellipse(1400, 1460, 55, 90, COLOR_CUP, COLOR_CUP_DARK, thickness=5)
    draw_ellipse(1400, 1460, 35, 70, COLOR_BG)
    
    # Panda
    draw_circle(SS_WIDTH//2, 860, 320, COLOR_RUSSET, COLOR_RUSSET_DARK)
    draw_circle(SS_WIDTH//2 - 200, 650, 80, COLOR_RUSSET, COLOR_RUSSET_DARK)
    draw_circle(SS_WIDTH//2 + 200, 650, 80, COLOR_RUSSET, COLOR_RUSSET_DARK)
    draw_circle(SS_WIDTH//2 - 200, 650, 40, COLOR_CREAM)
    draw_circle(SS_WIDTH//2 + 200, 650, 40, COLOR_CREAM)
    
    # Flower
    draw_circle(SS_WIDTH//2 - 280, 550, 40, COLOR_PINK)
    draw_circle(SS_WIDTH//2 - 320, 580, 40, COLOR_PINK)
    draw_circle(SS_WIDTH//2 - 300, 500, 40, COLOR_PINK)
    draw_circle(SS_WIDTH//2 - 230, 500, 40, COLOR_PINK)
    draw_circle(SS_WIDTH//2 - 250, 550, 20, COLOR_YELLOW)
    
    # Face
    draw_ellipse(SS_WIDTH//2, 950, 220, 180, COLOR_CREAM) 
    draw_circle(SS_WIDTH//2 - 120, 850, 88, COLOR_EYE)
    draw_circle(SS_WIDTH//2 + 120, 850, 88, COLOR_EYE)
    draw_circle(SS_WIDTH//2 - 140, 820, 20, (255, 255, 255))
    draw_circle(SS_WIDTH//2 + 100, 820, 20, (255, 255, 255))
    # Nose (triangle-ish)
    for y in range(950, 1000):
        for x in range(SS_WIDTH//2 - (1000-y)//2, SS_WIDTH//2 + (1000-y)//2):
            set_pixel(x, y, *COLOR_EYE)
    # Smile
    draw_line(SS_WIDTH//2 - 50, 1050, SS_WIDTH//2, 1080, COLOR_EYE, 5)
    draw_line(SS_WIDTH//2, 1080, SS_WIDTH//2 + 50, 1050, COLOR_EYE, 5)
    # Blush
    draw_circle(SS_WIDTH//2 - 150, 1050, 40, COLOR_PINK)
    draw_circle(SS_WIDTH//2 + 150, 1050, 40, COLOR_PINK)
    # Whiskers
    for i in range(3):
        draw_line(SS_WIDTH//2 - 180, 1000 + i*30, SS_WIDTH//2 - 300, 950 + i*40, COLOR_CREAM_DARK, 3)
        draw_line(SS_WIDTH//2 + 180, 1000 + i*30, SS_WIDTH//2 + 300, 950 + i*40, COLOR_CREAM_DARK, 3)
    
    # Paws
    draw_circle(SS_WIDTH//2 - 100, 1300, 80, COLOR_RUSSET, COLOR_RUSSET_DARK)
    draw_circle(SS_WIDTH//2 + 100, 1300, 80, COLOR_RUSSET, COLOR_RUSSET_DARK)
    
    # Butterfly
    # upper wings
    draw_ellipse(1720-40, 300-30, 50, 30, COLOR_ORANGE, COLOR_EYE, thickness=2)
    draw_ellipse(1720+40, 300-30, 50, 30, COLOR_ORANGE, COLOR_EYE, thickness=2)
    # lower wings
    draw_ellipse(1720-30, 300+20, 40, 25, COLOR_ORANGE, COLOR_EYE, thickness=2)
    draw_ellipse(1720+30, 300+20, 40, 25, COLOR_ORANGE, COLOR_EYE, thickness=2)
    # body
    draw_ellipse(1720, 300, 10, 30, COLOR_EYE, COLOR_EYE, thickness=1)
    
    # Save
    if not os.path.exists('output'): os.makedirs('output')
    save_png('output/entry.png')
    if not os.path.exists('/output'): os.makedirs('/output')
    save_png('/output/entry.png')

if __name__ == '__main__':
    main()
