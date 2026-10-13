import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

# Путь к файлу сохранения
SAVE_FILE = 'kotlovan_save.json'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        title = Label(text='Котлован', font_size=48, size_hint=(1, 0.3), halign='center')
        title.bind(size=title.setter('text_size'))
        
        btn_load = Button(text='Загрузить массив', size_hint=(1, 0.25), background_color=(0.2, 0.6, 0.9, 1))
        btn_create = Button(text='Создать массив', size_hint=(1, 0.25), background_color=(0.2, 0.8, 0.4, 1))
        
        # Статусная строка для главного меню (на случай загрузки)
        self.status_lbl = Label(text='Готов к работе', size_hint=(1, 0.1), color=(0, 0, 0, 1), halign='center')
        self.status_lbl.bind(size=self.status_lbl.setter('text_size'))

        btn_load.bind(on_press=self.load_array)
        btn_create.bind(on_press=self.goto_grid)
        
        layout.add_widget(title)
        layout.add_widget(btn_load)
        layout.add_widget(btn_create)
        layout.add_widget(self.status_lbl)
        self.add_widget(layout)
    
    def goto_grid(self, instance):
        App.get_running_app().sm.current = 'grid_screen'
    
    def load_array(self, instance):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.status_lbl.text = f'Массив загружен! Строк: {data.get("rows", 0)}, Ячеек: {len(data.get("cells", []))}'
            except Exception as e:
                self.status_lbl.text = f'Ошибка чтения файла: {e}'
        else:
            self.status_lbl.text = 'Файл сохранения не найден.'

class GridScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Верхняя панель: кнопка назад
        top_bar = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='← Назад', size_hint=(0.3, 1), background_color=(0.8, 0.2, 0.2, 1))
        back_btn.bind(on_press=lambda x: setattr(App.get_running_app().sm, 'current', 'main_menu'))
        top_bar.add_widget(back_btn)
        layout.add_widget(top_bar)
        
        # Центральная часть
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        info = Label(text='Экран сетки массива\n(Логика ячеек будет добавлена позже)', halign='center', valign='middle')
        info.bind(size=info.setter('text_size'))
        content.add_widget(info)
        
        # Кнопка сохранения
        save_btn = Button(text='Сохранить массив', size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
        save_btn.bind(on_press=self.save_array)
        content.add_widget(save_btn)
        
        # Статусное сообщение прямо под кнопкой (чтобы не ломать код)
        self.status_lbl = Label(text='Нажмите "Сохранить", чтобы создать файл', size_hint=(1, 0.15), color=(0, 0, 0, 1), halign='center')
        self.status_lbl.bind(size=self.status_lbl.setter('text_size'))
        content.add_widget(self.status_lbl)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def save_array(self, instance):
        # Данные, которые мы сохраняем (заглушка, потом заменим на реальные данные ячеек)
        array_data = {
            'rows': 3,
            'cols': 4,
            'cells': [
                {'row': 0, 'col': 0, 'title': 'План отопления', 'image_path': None, 'comment': 'Проверить узел'},
                {'row': 1, 'col': 1, 'title': 'План вентиляции', 'image_path': None, 'comment': None},
            ],
            'last_saved': '2023-10-27'
        }
        
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(array_data, f, ensure_ascii=False, indent=2)
            
            self.status_lbl.text = '[b]МАССИВ СОХРАНЁН![/b]\nФайл: kotlovan_save.json создан.'
            self.status_lbl.markup = True
            print(f"Файл сохранён в: {os.path.abspath(SAVE_FILE)}")
            
        except Exception as e:
            error_msg = str(e)
            self.status_lbl.text = f'[b]ОШИБКА СОХРАНЕНИЯ:[/b]\n{error_msg}'
            self.status_lbl.markup = True
            print(f"Ошибка: {error_msg}")

class KotlovanApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(GridScreen(name='grid_screen'))
        return self.sm

if __name__ == '__main__':
    KotlovanApp().run()
