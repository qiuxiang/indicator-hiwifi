# coding: utf-8
from os import path
from time import sleep
from threading import Thread
from requests import ConnectionError
from gi.repository import Gtk, AppIndicator3
from hiwifi import Hiwifi


class App:
    def __init__(self):
        self.menu = Gtk.Menu()

        self.indicator = AppIndicator3.Indicator.new(
            'indicator-hiwifi',
            path.abspath(path.dirname(__file__)) + '/icon.svg',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

        menu_item = Gtk.SeparatorMenuItem()
        menu_item.show()
        self.menu.append(menu_item)

        menu_item = Gtk.MenuItem('退出')
        menu_item.show()
        menu_item.connect('activate', Gtk.main_quit)
        self.menu.append(menu_item)

        self.devices = {}
        self.hifiwi = Hiwifi()
        self.hifiwi.login('password')

        self.update_traffics_thread = Thread(target=self.update_traffics)
        self.update_traffics_thread.setDaemon(True)
        self.update_traffics_thread.start()

        Gtk.main()

    def update_traffics(self):
        for device in self.hifiwi.devices()['devices']:
            self.devices[device['ip']] = device

        while True:
            try:
                data = self.hifiwi.traffics()['data']
                self.indicator.set_label('↑ %s KB/S    ↓ %s KB/S' % (
                    data['total']['up'], data['total']['down']), '')

                # print('\033c', end='')
                # for item in data['list']:
                #     if item['ip'] in self.devices:
                #         print('↑ %s KB/S\t↓ %s KB/S\t%s' % (
                #             item['up'], item['down'], self.devices[item['ip']]['name']), '')

                sleep(4)
            except ConnectionError as error:
                print(error)

    @staticmethod
    def create_menu_item(label):
        menu_item = Gtk.MenuItem(label)
        menu_item.show()
        return menu_item

if __name__ == '__main__':
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    app = App()
