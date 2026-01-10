import pygame
def process_img(sprite_sheet, data):
    """
    Extracts sprite frames from a sprite sheet
    
    Args:
        sprite_sheet (pygame.Surface): An image 
        containing all sprite frames for an animation

        data (dict): A dictionary containing data on 
        coordinates and dimensions of all sprite frames
        in the sprite sheet

    Returns:
        list: A list of sprite frames from the sprite 
        sheet extracted in the order of animation order
    """
    frames = []
    for item in data["frames"]:
        frame_data = item["frame"]
        x = frame_data["x"]
        y = frame_data["y"]
        w = frame_data["w"]
        h = frame_data["h"]
        img_frame = sprite_sheet.subsurface(pygame.Rect(x, y, w, h))
        frames.append(img_frame)
    return frames