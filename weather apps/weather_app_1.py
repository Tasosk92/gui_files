"""Weather app using OpenWeatherMap API."""

from configparser import ConfigParser
import requests as r
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pyowm.utils.config import get_default_config
from PIL import Image, ImageTk


config_dict = get_default_config()
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)


class App():
    
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric&lang={}'
    api_key = config['weather_app']['api']
    config_dict = get_default_config()
    btn_clicked = 0
    image1 = Image.open('gr_flag.ico')
    image2 = Image.open('gb_flag.ico')
    resize_image1 = image1.resize((15, 15))
    resize_image2 = image2.resize((15, 15))

    def __init__(self, root):
        
        self.root = root
        self.icongr = ImageTk.PhotoImage(App.resize_image1)
        self.icongb = ImageTk.PhotoImage(App.resize_image2)
        self.widgets()
        self.root.resizable(0, 0)
        self.root.geometry('450x300')
        self.root.title("Πρόγνωση καιρού")

    def widgets(self):

        self.lang_btn = tk.Button(self.root,
                                  image=self.icongr, command=self.set_language)
        self.lang_btn.grid(row=0, column=0, sticky='e')

        self.city_name = tk.StringVar()
        self.entry_box = tk.Entry(self.root, textvariable=self.city_name,
                                  font='Arial 12 italic', fg='grey')
        self.entry_box.grid(row=0, column=1, sticky='w')
        self.entry_box.bind("<Return>", self.handle_enter)
        self.entry_box.bind("<FocusIn>", lambda e: self.handle_focus_in(e))
        self.entry_box.bind("<FocusOut>", self.handle_focus_out)
        self.city_name.set('π.χ. Αθήνα,GR🔍')

        self.title = tk.StringVar()
        self.title.set("")
        tk.Label(self.root, textvariable=self.title,
                 font='Arial 25 bold').grid(row=3, column=1, sticky='nwse', pady=10)

        self.verdict = tk.StringVar()
        self.coords_, self.sun_, = tk.StringVar(), tk.StringVar()
        self.temp_feels, self.temp_max_min = tk.StringVar(), tk.StringVar()

        self.lbl1 = tk.Label(self.root, textvariable=self.verdict,
                             font="Arial 15 bold", )
        self.lbl1.grid(row=4, column=1)

        lbl2_1 = tk.Label(self.root, textvariable=self.coords_,
                          font="Arial 10", )
        lbl2_1.grid(row=5, column=1)
        lbl2_2 = tk.Label(self.root, textvariable=self.sun_,
                          font="Arial 10", )
        lbl2_2.grid(row=6, column=1)

        lbl2_3 = tk.Label(self.root, textvariable=self.temp_feels,
                          font="Arial 10", )
        lbl2_3.grid(row=7, column=1)
        lbl2_4 = tk.Label(self.root, textvariable=self.temp_max_min,
                          font="Arial 10", )
        lbl2_4.grid(row=8, column=1)

    def handle_focus_in(self, event):
        
        self.entry_box.delete(0, tk.END)
        self.entry_box.config(fg='black')

    def handle_focus_out(self, event):
        
        self.entry_box.delete(0, tk.END)
        self.entry_box.config(fg='grey')
        if App.btn_clicked % 2 == 1:
            self.city_name.set("e.g. Athens,GR🔍")
        else:
            self.city_name.set("π.χ. Αθήνα,GR🔍")

    def handle_enter(self, event):
        
        self.getweather()
        if App.btn_clicked == 0:
            self.title.set("Ο καιρός τώρα")
        self.root.focus()

    def set_language(self):
        
        App.btn_clicked += 1
        if App.btn_clicked % 2 == 1:
            self.root.title("Weather app")
            self.lang_btn.config(image=self.icongb)
            self.city_name.set("e.g. Athens,GR🔍")
        else:
            self.root.title("Πρόγνωση καιρού")
            self.lang_btn.config(image=self.icongr)
            self.city_name.set("π.χ. Αθήνα,GR🔍")

    def getweather(self):
        
        self.entry_text = self.city_name.get()
        if App.btn_clicked % 2 == 1:
            self.result = r.get(App.url.format(
                self.entry_text, App.api_key, 'en'))
        else:
            self.result = r.get(App.url.format(
                self.entry_text, App.api_key, 'el'))

        self.result = self.result.json()

        try:
            self.city = self.result['name']
            self.country = self.result['sys']['country']
            self.lon = self.result['coord']['lon']
            self.lat = self.result['coord']['lat']
            self.sunrise = self.result['sys']['sunrise']
            self.sunset = self.result['sys']['sunset']
            self.temp = self.result['main']['temp']
            self.feels_like = self.result['main']['feels_like']
            self.temp_max = self.result['main']['temp_max']
            self.temp_min = self.result['main']['temp_min']
            self.weather_descr = self.result['weather'][0]['description'].capitalize()
            self.humidity = self.result['main']['humidity']
            self.wind = self.result['wind']['speed']

            if App.btn_clicked % 2 == 1:
                self.title.set(" Current Weather ")
                self.coords_.set('City: {}\nLongitude: {:.2f}\u00b0\tLatitude: {:.2f}\u00b0 '.format(
                    str(self.city) + ', ' + str(self.country),
                    self.lon, self.lat))

                self.sun_.set('Sunrise: {}UTC  Sunset: {}UTC'.format(
                    str(datetime.utcfromtimestamp(
                        self.sunrise).strftime('%H:%M:%S')),
                    str(datetime.utcfromtimestamp(self.sunset).strftime('%H:%M:%S'))))
                self.temp_feels.set('Temperature: {}\u2103  Feels like: {}\u2103'.format(
                    str(self.temp), str(self.feels_like)))
                self.temp_max_min.set('Max Temperature: {}\u2103  Min Temperature: {}\u2103'.format(
                    (self.temp_max), str(self.temp_min)))

            else:
                self.title.set("Ο καιρός τώρα")
                self.coords_.set('Πόλη: {}\nΓεωγραφικό μήκος: {:.2f}\u00b0\tΓεωγραφικό πλάτος: {:.2f}\u00b0 '.format(
                    str(self.city) + ', ' + str(self.country),
                    self.lon, self.lat))

                self.sun_.set('Ανατολή ηλίου: {}UTC  Δύση ηλίου: {}UTC'.format(
                    str(datetime.utcfromtimestamp(
                        self.sunrise).strftime('%H:%M:%S')),
                    str(datetime.utcfromtimestamp(self.sunset).strftime('%H:%M:%S'))))
                self.temp_feels.set('Θερμοκρασία: {}\u2103  Αίσθηση: {}\u2103'.format(
                    str(self.temp), str(self.feels_like)))
                self.temp_max_min.set('Μέγιστη Θερμοκρασία: {}\u2103  Ελάχιστη Θερμοκρασία: {}\u2103'.format(
                    (self.temp_max), str(self.temp_min)))

            self.verdict.set(str(self.weather_descr))
            self.root.focus()

        except KeyError:
            if App.btn_clicked % 2 == 1:
                messagebox.showwarning('Warning', 'No city found')
            else:
                messagebox.showwarning('Σφάλμα', 'Η πόλη δεν βρέθηκε')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
