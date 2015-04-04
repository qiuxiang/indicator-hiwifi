# coding: utf-8
from os import path
from requests import ConnectionError
from threading import Thread
from time import sleep
from gi.repository import Gtk, AppIndicator3
from hiwifi import Hiwifi


class App:
    def __init__(self):
        self.menu = Gtk.Menu()

        self.indicator = AppIndicator3.Indicator.new(
            'example-simple-client',
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
            submenu_item_up = self.create_menu_item('上传：')
            submenu_item_down = self.create_menu_item('下载：')

            submenu = Gtk.Menu()
            submenu.append(self.create_menu_item('IP：' + device['ip']))
            submenu.append(self.create_menu_item('MAC：' + device['mac']))
            submenu.append(self.create_menu_item('连接类型：' + device['type']))
            submenu.append(submenu_item_up)
            submenu.append(submenu_item_down)

            menu_item = self.create_menu_item(device['name'])
            menu_item.set_submenu(submenu)
            self.menu.prepend(menu_item)

            device['menu_item'] = menu_item
            device['submenu_item_up'] = submenu_item_up
            device['submenu_item_down'] = submenu_item_down
            self.devices[device['ip']] = device

        while True:
            try:
                data = self.hifiwi.traffics()['data']
                self.indicator.set_label('↑ %s KB/S    ↓ %s KB/S' % (
                    data['total']['up'], data['total']['down']), '')

                for item in data['list']:
                    if item['ip'] in self.devices:
                        device = self.devices[item['ip']]
                        device['submenu_item_up'].set_label('上传：%s KB/S' % item['up'])
                        device['submenu_item_down'].set_label('下载：%s KB/S' % item['down'])

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
