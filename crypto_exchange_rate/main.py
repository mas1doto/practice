import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import json
import requests
from requests_cache import CachedSession
import os


class FindCurrency(ttk.Frame):
    API_URL = "https://api.coingecko.com/api/v3/simple/price"
    GRID_SIZE_ROW = 1
    GRID_SIZE_COLUMN = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._session = CachedSession()

        # команда для валидации ввода
        validate_command = (self.register(self.validate_input), '%P')

        # загружаем данные о валютах
        self._currency_data = self.load_data("currencies.json")
        self._exchange_currency_data = self.load_data("exchange_currency.json")

        # переменные для хранения текущих значений
        self._price = tk.StringVar()
        self._coin_quantity = tk.StringVar()

        # настройка сетки
        self.config_grid(self.GRID_SIZE_ROW, self.GRID_SIZE_COLUMN)

        # комбобоксы для выбора валют
        self._currency_select_data = ttk.Combobox(self,
                                                  width=4,
                                                  justify=tk.RIGHT,
                                                  state="readonly"
                                                  )
        self.config_combobox(self._currency_select_data, self._currency_data, 2)

        self._vs_currency_select_data = ttk.Combobox(self,
                                                     width=4,
                                                     justify=tk.RIGHT,
                                                     state="readonly"
                                                     )
        self.config_combobox(self._vs_currency_select_data, self._exchange_currency_data, 5)

        # поля ввода
        self._currency_field = ttk.Entry(self,
                                         width=10,
                                         justify=tk.RIGHT,
                                         textvariable=self._coin_quantity,
                                         validate='key',
                                         validatecommand=validate_command
                                         )
        self._currency_field.grid(row=0, column=1, sticky='news')

        self._vs_currency_field = ttk.Entry(self, width=10, justify=tk.RIGHT, textvariable=self._price)
        self._vs_currency_field.grid(row=0, column=4, sticky='news')

        self._swap_button = tk.Button(self, text="⇄")
        self._swap_button.grid(row=0, column=3, sticky='news')

        self._coin_quantity.trace('w', self.get_currency_value)


    def config_grid(self, r, c):
        """
        Sets up a grid with given number of rows and columns.

        This method sets up a grid with the given number of rows and columns,
        and then configures each row and column to have a weight of 1 and to
        be uniform with the name "fred".

        Parameters:
            r (int): The number of rows in the grid.
            c (int): The number of columns in the grid.
        """
        for column in range(c):
            self.columnconfigure(column, weight=1, uniform="fred")
        for row in range(r):
            self.rowconfigure(row, weight=1, uniform="fred")

    @staticmethod
    def validate_input(new_value):

        """
        Validates that the input string is either empty or consists entirely of digits.

        Args:
            new_value (str): The string to be validated.

        Returns:
            True if the input string is valid, False otherwise.
        """
        return new_value == "" or new_value.isnumeric()

    @staticmethod
    def load_data(file_name):

        """
        Loads data from a given file.

        This method loads data from a given file name, and then returns the loaded data.
        If the file does not exist, a message box with an error message is shown and None is returned.
        If a JSONDecodeError occurs while loading the data, a message box with an error message is shown and None is returned.

        Parameters:
            file_name (str): The name of the file to load data from.

        Returns:
            dict or None: The loaded data, or None if an error occurred.
        """
        if  os.path.exists(file_name):
            try:
                with open(file_name, "r") as file:
                    data = json.load(file)
                    return data
            except json.JSONDecodeError as e:
                mb.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                return None
        else:
            mb.showerror("Ошибка", f"Файл {file_name} не найден")
            return None

    def config_combobox(self, combox, data, pos_x):


        """
        Configures a combobox for selecting a currency.

        This method configures a combobox with the given data and binds it to the get_currency_value method.

        Args:
            combox (ttk.Combobox): The combobox to be configured.
            data (dict): The data to be used for the combobox.
            pos_x (int): The column position for the combobox.

        Returns:
            None
        """
        combox['values'] = [i for i in data.keys()]
        combox.current(0)
        combox.bind("<<ComboboxSelected>>", lambda x:self.get_currency_value())
        combox.grid(row=0, column=pos_x, sticky='news')


    def get_api_data(self, coin, currency):

        """
        Loads data from the CoinGecko API.

        This method loads data about the given coin in the given currency from the CoinGecko API.

        Args:
            coin (str): The ID of the coin to load data for.
            currency (str): The ID of the currency to load data for.

        Returns:
            dict or None: The loaded data, or None if an error occurred.

        Raises:
            requests.RequestException: If an error occurred while loading data.
        """
        try:
            headers = {
                "accept": "application/json"}
            response = self._session.get(f"{self.API_URL}?ids={coin}&vs_currencies={currency}",
                                          headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
                mb.showerror("Ошибка", f"Произошла ошибка: {e}")
                return None

    def get_currency_value(self, *args):

        """
        Loads the value of the selected currency in the selected coin.

        This method is bound to the Combobox widget and is called when a new value is selected.

        Args:
            *args: Additional arguments passed to the method.
        Returns:
            None

        Raises:
            requests.RequestException: If an error occurred while loading data.
        """

        coin = self._currency_data[self._currency_select_data.get()]["id"]
        currency = self._exchange_currency_data[self._vs_currency_select_data.get()]['id']
        data = self.get_api_data(coin, currency)
        self._vs_currency_field.delete(0, tk.END)
        tmp_quantity = self._coin_quantity.get()
        self._vs_currency_field.insert(0, round(data[coin][currency] *
                                                float(tmp_quantity if tmp_quantity else 0), 4))




def main():
    root = tk.Tk()
    root.geometry("450x200")
    root.title("Курс обмена валют")
    root.grid_columnconfigure(0, weight=1)

    f = FindCurrency(root, name="frame1")
    f.grid(row=0, column=0, sticky='news')


    root.mainloop()

if __name__ == "__main__":
    main()