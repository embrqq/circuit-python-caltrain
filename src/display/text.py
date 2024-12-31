import terminalio
from adafruit_display_text import label

def create_text(
    text: str,
    font = terminalio.FONT,
    anchor_point: tuple = (0,0),
    anchored_position: tuple = (0,0),
    color: int = 0XFFFFFF,
    background_color: int = 0X000000,
) -> label.Label:
    return label.Label(
        font=font,
        text=text,
        color=color,
        line_spacing=1,
        base_alignment=True,
        background_color=background_color,
        anchor_point=anchor_point,
        anchored_position=anchored_position,
    )
       
def create_scrolling_text(
    text: str,
    font = terminalio.FONT,
    anchor_point: tuple = (0,0),
    color: int = 0XFFFFFF,
    background_color: int = 0X000000,
) -> label.Label:
    return label.Label(
        font=terminalio.FONT,
        text=text,
        color=color,
        line_spacing=1,
        base_alignment=True,
        background_color=background_color,
    )
       