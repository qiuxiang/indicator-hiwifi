# coding: utf-8
from os import path
from time import sleep
from threading import Thread
from requests import ConnectionError
from gi.repository import Gtk, AppIndicator3
from hiwifi import Hiwifi


class Indicator:
    def __init__(self):
        self.config = {
            'password': 'your password',
            'interval': 5,
        }
        self.menu = Gtk.Menu()
        self.indicator = AppIndicator3.Indicator.new(
            'indicator-hiwifi',
            path.abspath(path.dirname(__file__)) + '/icon.svg',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

        menu_item = Gtk.MenuItem('退出')
        menu_item.show()
        menu_item.connect('activate', Gtk.main_quit)
        self.menu.append(menu_item)

        self.login()

        self.update_traffics_thread = Thread(target=self.update_traffics)
        self.update_traffics_thread.setDaemon(True)
        self.update_traffics_thread.start()

        Gtk.main()

    def login(self):
        self.hifiwi = Hiwifi()
        response = self.hifiwi.login(self.config['password'])
        if response != True:
            print(response)
            exit(1)

    def update_traffics(self):
        while True:
            try:
                data = self.hifiwi.traffics()['data']
                self.indicator.set_label('↑ %s KB/S    ↓ %s KB/S' % (
                    data['total']['up'], data['total']['down']), '')
                sleep(self.config['interval'])
            except ConnectionError as error:
                print(error)

if __name__ == '__main__':
    Indicator()
