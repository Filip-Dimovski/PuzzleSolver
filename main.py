import config_file_read as parameters
import puzzleSolver
from kivy.core.text import LabelBase


LabelBase.register(name='Rubik', fn_regular='files/fonts/Rubik/Rubik-Regular.ttf')
LabelBase.register(name='Andatino', fn_regular='files/fonts/Andatino/andantino.ttf')




if __name__ == "__main__":
	puzzleSolver.PuzzleSolver().run()
	

