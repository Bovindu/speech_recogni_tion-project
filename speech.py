import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import threading
import speech_recognition as sr

class SpeechRecognitionApp(App):
    def build(self):
        self.is_recording = False
        self.recognizer = sr.Recognizer()

        layout = BoxLayout(orientation='vertical')

        self.display = TextInput(readonly=True, multiline=True)
        layout.add_widget(self.display)

        self.start_button = Button(text='Start Speak', on_press=self.toggle_speech)
        layout.add_widget(self.start_button)

        self.clear_button = Button(text='Clear', on_press=self.clear_display)
        layout.add_widget(self.clear_button)

        return layout

    def toggle_speech(self, instance):
        if not self.is_recording:
            self.start_button.text = "Stop Speak"
            self.is_recording = True
            threading.Thread(target=self.record_speech).start()
        else:
            self.start_button.text = "Start Speak"
            self.is_recording = False

    def record_speech(self):
        with sr.Microphone() as mic:
            self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    Clock.schedule_once(lambda dt: self.update_display(f" {text}\n"))

                except sr.UnknownValueError:
                    continue

    def update_display(self, text):
        self.display.text += text

    def clear_display(self, instance):
        self.display.text = ''

if __name__ == '__main__':
    SpeechRecognitionApp().run()
