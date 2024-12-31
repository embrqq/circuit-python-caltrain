from adafruit_matrixportal.matrix import Matrix
import terminalio
import displayio
from adafruit_display_text import label


class Display:
    """
    A class wrapping the display matrix.
    """
    def __init__(
        self,
        width: int = 64,
        height: int = 32,
        bit_depth: int = 6,
        serpentine: bool = True,
        tile_rows: int = 1,
    ):
        self._width = width
        self._height = height  
        self.matrix = Matrix(
            width=width,
            height=height,
            bit_depth=bit_depth,
            serpentine=serpentine,
            tile_rows=tile_rows,
        )
        self.root_group = displayio.Group()
        self.matrix.display.root_group = self.root_group


    def __check_coordinates(
        self,
        x: int,
        y: int,
    ):
        if x < 0 or x >= self._width:
            raise Exception(f"'x' must be within [0, {self._width})")
        if y < 0 or y >= self._height:
            raise Exception(f"'y' must be within [0, {self._height})")


    def add_group(
        self,
        x: int = 0,
        y: int = 0,
    ) -> displayio.Group:
        """
        Creates a new display group at the given anchor points and
        appends it to the primary display.

        :param int x: the x coordinate of the anchor point
        :param int y: the y coordinate of the anchor point
        :raises Exception: if x or y are outside the matrix bounds
        """
        self.__check_coordinates(x, y)
        group = displayio.Group(
            x=x,
            y=y,
        )

        self.root_group.append(group)
        return group
         