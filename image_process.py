import pygame
def process_img(sprite_sheet, data):
    frames = []
    for item in data["frames"]:
        frame_data = item["frame"]
        x, y, w, h = frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]
        img_frame = sprite_sheet.subsurface(pygame.Rect(x, y, w, h))
        frames.append(img_frame)
    return frames