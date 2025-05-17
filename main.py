import kivy
kivy.require('2.0.0')

from gdataprocessor import loadGoogleData

import logging

import asyncio
from threading import Thread

# asyncio.ensure_future(loadGoogleData(self, NUMBER_OF_FIRST_VALUES_DT))

# This modifies the console output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger("kivy").setLevel(logging.WARNING)
logging.getLogger("kivymd").setLevel(logging.WARNING)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivymd.app import MDApp

# data table
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen


# app window size
# from kivy.core.window import Window
# Window.size = (390, 710)

loop = asyncio.new_event_loop()

# declare .kv file as class to access it
class MainWidget(Widget):
    pass

NUMBER_OF_FIRST_VALUES_DT = 3
ROW_COUNTER = 1


# loads .kv file with monitor### name
class Monitor(MDApp):

    def loadMorePressed(self, instance):
        print("[ARDUINO PROJECT] --Кнопка натиснута--")

    def build(self):

        self.data_tables = MDDataTable(
            use_pagination=True,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            # check=True,
            column_data=[
                ("Teм.", dp(20)),
                ("Вологість", dp(20)),
                # self.sort_on_signal
                ("Час", dp(14)),
                ("Дата", dp(18)),
            ],
            row_data=[
                (
                    "24",
                    "55%",
                    "-",
                    "2024",
                ),
                (
                    "24",
                    "55%",
                    "-",
                    "2024",
                ),
                (
                    "24",
                    "55%",
                    "-",
                    "2024",
                ),
            ],
            elevation=2,
        )
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)

        rootWidget = MainWidget()
        rootWidget.ids.table_container.add_widget(self.data_tables)

        print('[ARDUINO PROJECT] Launch async loadGoogleData()')

        # Start asyncio event loop in background thread
        self.async_loop = asyncio.new_event_loop()
        Thread(target=self.start_loop, daemon=True).start()

        # Викликаємо асинхронну функцію через asyncio.create_task
        asyncio.run_coroutine_threadsafe(loadGoogleData(self, NUMBER_OF_FIRST_VALUES_DT), self.async_loop)
        print('[ARDUINO PROJECT] Return rootWidget')

        button = MDRaisedButton(
            text="Завантажити ще",
            size_hint=(1, 0.15),
            pos_hint = {"center_x": 0.5},
            font_style="H5",  # Більший і жирний текст
        )
        button.bind(on_release=self.loadMorePressed)

        rootWidget.ids.table_container.add_widget(button)

        return rootWidget

    def start_loop(self):
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_forever()

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)


    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

    # Sorting Methods:
    # since the https://github.com/kivymd/KivyMD/pull/914 request, the
    # sorting method requires you to sort out the indexes of each data value
    # for the support of selections.
    #
    # The most common method to do this is with the use of the builtin function
    # zip and enumerate, see the example below for more info.
    #
    # The result given by these funcitons must be a list in the format of
    # [Indexes, Sorted_Row_Data]


    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][2]))


    def sort_on_schedule(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: sum(
                    [
                        int(l[1][-2].split(":")[0]) * 60,
                        int(l[1][-2].split(":")[1]),
                    ]
                ),
            )
        )


    def sort_on_team(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][-1]))

# run application
if __name__ == '__main__':
    Monitor().run()