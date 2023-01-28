
from src.graphical.menu import AlertContainer, Commands, LoadMenu, MultiMenu, StartMenu, Stats, TitleScreen
from src.ressources import get_app



class MenuController:
    def __init__(self) -> None:
        self.app = get_app()
        self.game = self.app.game
        self.manager = self.app.manager
        self.camera = self.game.camera
        self.start_menu = StartMenu(self)
        self.load_menu = LoadMenu(self)
        self.stats = Stats(self)
        self.title_screen = TitleScreen(self)
        self.commands = Commands(self)
        self.alert_container = AlertContainer()
        self.multi_menu = MultiMenu(self)
        self._menu = self.start_menu
        self._last = None
        self.statics = [self.commands, self.stats]
        for menu in self.statics:
            menu.hide()

    def run(self):
        self.alert_container.check_hiding()

    def start(self):
        self.hide_menu()
        for menu in self.statics:
            menu._show()
        
        self.commands.construct_menu.start()

    def stop(self):self.hide_menu();self.start_menu.show()
    def alert(self,text):self.alert_container.alert(text)
    def prompt(self,text):self.alert_container.prompt(text)

    def buyable(self, price:float|int, buy_possible:bool=False):
        """Check if something is buyable, and if buy_possible=True, removes the price from points"""
        if self.stats.points >= price:
            if buy_possible:
                self.stats.points -= price
            return True
        return False


    def handle_button_click_event(self, event):
        button_id = event.ui_element.object_ids[-1]
        if self.menu:
            self.menu.handle_click(button_id)
        else:
            self.handle_static_click(button_id)

    def handle_build_click(self, pos, to_construct):
        build = self.app.game.map.get(pos)
        
        if build:
            if self.app.event_controller.construction_mode: self.alert("Can't place that here !")
            elif self.menu == build.menu:
                self.hide_menu()
            else:
                self.menu = build.menu
                
        elif self.app.event_controller.construction_mode:
            self.app.event_controller.construct(pos)
            
        else:
            self.hide_menu()

    def handle_static_click(self, button_id):
        for menu in self.statics:
            menu.handle_click(button_id)

    @property
    def menu(self):
        return self._menu
    @menu.setter
    def menu(self, menu):
        self._last = self.menu
        if menu:
            menu._show()
        if self._menu:
            self._menu.hide()
        self._menu = menu

    def back(self):
        self.menu.hide()
        self._last.show()

    def hide_menu(self):
        self._last = self.menu
        if self.menu is not None:
            self.menu.hide()
            self.menu = None

    def hide_menus(self):
        self.hide_menu()
        for menu in self.statics:
            menu.hide()