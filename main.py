import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Путь к файлу сохранения (в папке проекта)
SAVE_FILE = 'kotlovan_save.json'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        title = Label(text='Котлован', font_size=48, size_hint=(1, 0.3))
        btn_load = Button(text='Загрузить массив', size_hint=(1, 0.35))
        btn_create = Button(text='Создать массив', size_hint=(1, 0.35))
        
        btn_load.bind(on_press=self.load_array)
        btn_create.bind(on_press=self.create_array)
        
        layout.add_widget(title)
        layout.add_widget(btn_load)
        layout.add_widget(btn_create)
        self.add_widget(layout)
    
    def create_array(self, instance):
        # Пока просто переходим на экран-заглушку, чтобы не ломать сборку
        app = App.get_running_app()
        app.sm.current = 'grid_screen'
        # Здесь позже будет экран выбора строк/столбцов
    
    def load_array(self, instance):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Здесь можно восстановить массив, пока просто показываем успех
                print('Массив загружен:', data)
                App.get_running_app().root.ids.status_label.text = 'Массив загружен из файла'
            except Exception as e:
                App.get_running_app().root.ids.status_label.text = f'Ошибка загрузки: {e}'
        else:
            App.get_running_app().root.ids.status_label.text = 'Файл сохранения не найден'

class GridScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Верхняя панель с кнопкой «Назад»
        top_bar = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='← Назад', size_hint=(0.2, 1))
        back_btn.bind(on_press=lambda x: setattr(App.get_running_app().sm, 'current', 'main_menu'))
        top_bar.add_widget(back_btn)
        layout.add_widget(top_bar)
        
        # Основная область сетки (заглушка)
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        info = Label(text='Здесь будет сетка массива\n(строки/столбцы выбираются позже)', halign='center')
        content.add_widget(info)
        
        # Кнопка «Сохранить массив»
        save_btn = Button(text='Сохранить массив', size_hint=(1, 0.2), background_color=(0, 0.6, 0, 1))
        save_btn.bind(on_press=self.save_array)
        content.add_widget(save_btn)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def save_array(self, instance):
        # Пример данных массива (позже заменим на реальные данные ячеек)
        array_data = {
            'rows': 3,
            'cols': 4,
            'cells': [
                {'row': 0, 'col': 0, 'title': 'План отопления', 'image': None, 'comment': 'Проверить узел'},
                {'row': 0, 'col': 1, 'title': 'План вентиляции', 'image': None, 'comment': None},
            ]
        }
        
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(array_data, f, ensure_ascii=False, indent=2)
            App.get_running_app().root.ids.status_label.text = 'Массив сохранён в kotlovan_save.json'
            print('Массив сохранён:', array_data)
        except Exception as e:
            App.get_running_app().root.ids.status_label.text = f'Ошибка сохранения: {e}'

class KotlovanApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(GridScreen(name='grid_screen'))
        
        # Панель статуса (чтобы видеть сообщения о сохранении/загрузке)
        status_layout = BoxLayout(size_hint=(1, 0.05))
        self.status_label = Label(text='Готов к работе', size_hint=(1, 1), halign='left')
        self.status_label.bind(size=self.status_label.setter('text_size'))
        status_layout.add_widget(self.status_label)
        
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.sm)
        root.add_widget(status_layout)
        return root

if __name__ == '__main__':
    KotlovanApp().run()
