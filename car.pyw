'''
CAR - Chrome Auto Refresher
'''

import tkinter as tk
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Chrome Auto Refresher')
        self.job = None
        self.chrome = None
        self.frame = tk.Frame(self, padx=5, pady=5)
        self.var_refresh = tk.DoubleVar()
        self.var_url = tk.StringVar()        
        self.var_go_txt = tk.StringVar()
        self.var_go_val = tk.BooleanVar()
        self.var_go_val.set(False)
        self.lb_url = tk.Label(self.frame, text="Input URL:")
        self.tx_url = tk.Entry(self.frame, textvar=self.var_url, width=100)
        self.lb_refresh = tk.Label(self.frame, text="Refresh Frequency:")
        self.sc_refresh = tk.Scale(
            self.frame,
            variable=self.var_refresh,
            from_=0.25,
            to=5.00,
            orient=tk.HORIZONTAL,
            resolution=0.25,
            digits=3,
            length=400
            )
        self.bt_go = tk.Checkbutton(
            self.frame,
            textvariable=self.var_go_txt,
            variable=self.var_go_val,
            command=self.toggle_button_state,
            indicatoron=False,
            relief=tk.FLAT
            )

        # default values
        self.var_go_txt.set('Start Auto Refresh')
        # self.var_url.set('https://www.google.ca/')  # default your favorite shortcut

    def toggle_button_state(self):
        if self.var_go_val.get():
            self.var_go_txt.set('Auto Refreshing...')
            self.refresh()
            for widget in (self.sc_refresh, self.tx_url):
                widget.config(state=tk.DISABLED)
        else:
            self.var_go_txt.set('Start Auto Refresh')
            for widget in (self.sc_refresh, self.tx_url):
                widget.config(state=tk.NORMAL)            
            self._cancel_job()

    def _cancel_job(self):
        if self.job is not None:
            self.after_cancel(self.job)

    def get_refresh_rate(self):
        return int(self.var_refresh.get() * 60000)

    def refresh(self):        
        try:
            self.chrome.refresh()
        except AttributeError:
            self.chrome = AutoRefresher(self.var_url.get())            
        except (WebDriverException, ConnectionRefusedError):
            self.chrome.driver.quit()
            del self.chrome     # see if it garbage collects
            self.chrome = AutoRefresher(self.var_url.get())
        self._cancel_job()
        self.job = self.after(ms=self.get_refresh_rate(), func=self.refresh)

    def run(self):
        self.lb_url.grid(row=0, column=0)
        self.tx_url.grid(row=0, column=1, columnspan=2)
        self.lb_refresh.grid(row=1, column=0, sticky=tk.S)
        self.sc_refresh.grid(row=1, column=1, sticky=tk.S)
        self.bt_go.grid(row=1, column=2, sticky=tk.S)
        self.frame.pack()
        self.mainloop()

class AutoRefresher():
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
    def refresh(self):
        self.driver.refresh()

if __name__ == '__main__':
    gui = GUI()
    gui.run()
