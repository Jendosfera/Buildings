from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class KotlovanApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        label = Label(text='Котлован', font_size=48)
        btn1 = Button(text='Загрузить массив', size_hint=(1, 0.3))
        btn2 = Button(text='Создать массив', size_hint=(1, 0.3))
        layout.add_widget(label)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        return layout
        
if __name__ == '__main__':
    KotlovanApp().run()