from traits.api import Array

from .checker_board_model import CheckerBoardModel


class ColoredCheckerBoardModel(CheckerBoardModel):

    colors = Array
