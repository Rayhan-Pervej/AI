from calcudoku.game import Calcudoku
from calcudoku.visualize import save_figure

game = Calcudoku.generate(4)

save_figure(game, 'puzzle.png', solution=False)
save_figure(game, 'puzzle_solution.png', solution=True)