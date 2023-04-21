import kivy
from kivy.app import App
import PuzzleSolverGrid as Grid
from kivy.uix.floatlayout import FloatLayout 
import RootScreen as Root 
import LanguageScreen as ls
import WelcomeScreen as Welcome
import SignInScreen as signin
import SignUpScreen as signup
import HomeBoardScreen as hbs
import MyPuzzlesScreen as mps
import NewPuzzleScreen as nps
import ManageUserScreen as mus
import ChangePasswordScreen as cps
import CameraScreen as cs
import PictureViewScreen as pvs
import PictureScreen as ps
import ChooseFileScreen as cfs
from kivy.config import Config
import config_file_read as parameters

class PuzzleSolver(App):



	def build(self):
		return Root.RootScreen()