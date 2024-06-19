import os
import shutil
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.welcome import WelcomeScreen
from screens.game import GameScreen
from kivy.lang import Builder
from screens.buttons1.subscreen1 import SubScreen1
from screens.buttons2.subscreen2 import SubScreen2
from screens.buttons3.subscreen3 import SubScreen3
from screens.buttons4.subscreen4 import SubScreen4
from screens.buttons5.subscreen5 import SubScreen5

class MyApp(App):
    def build(self):
        self.cleanup_run_folder()  # Clean up "run" folder before adding screens
        Builder.load_file('screens/buttons4/subscreen4.kv')
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SubScreen1(name='subscreen1'))
        sm.add_widget(SubScreen2(name='subscreen2'))
        sm.add_widget(SubScreen3(name='subscreen3'))
        sm.add_widget(SubScreen4(name='subscreen4'))
        sm.add_widget(SubScreen5(name='subscreen5'))
        return sm

    def cleanup_run_folder(self):
        run_folder = os.path.join(os.getcwd(), 'run')
        for filename in os.listdir(run_folder):
            file_path = os.path.join(run_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == '__main__':
    MyApp().run()
