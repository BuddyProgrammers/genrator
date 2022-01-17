from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextFieldRound
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.theming import ThemableBehavior
from kivy.metrics import dp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.list import MDList
from kivy.base import EventLoop
from patcher import check, genotp, add_user
from QRgenerator import create_qr
from kivy.core.window import Window


class MeraButton(MDTextFieldRound):
    pass


class SelectPage(Screen):
    pass


class CodePage(Screen):
    pass


class ClickableTextFieldRound(RelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    passr = BooleanProperty()


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Signin_signup(Screen):
    pass


class ForPassScreen(Screen):
    time = StringProperty()
    title = StringProperty()
    total_time = 120

    def start_timer(self):
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        self.total_time -= 1
        self.time = "0"+str(int(self.total_time/60)) + \
            " : "+str(self.total_time % 60)
        if self.total_time == 0:
            return False


class Sign_Up_Screen(Screen):
    time = StringProperty()
    title = StringProperty()
    total_time = 120

    def start_timer(self):
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        self.total_time -= 1
        self.time = "0"+str(int(self.total_time/60)) + \
            " : "+str(self.total_time % 60)
        if self.total_time == 0:
            return False


class ChangePassScreen(Screen):
    pass


class SignScreen(Screen):
    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            # do what you want, return True for stopping the propagation
            return True

    def check_phone(self, teacher_id, passw):
        bu = check(teacher_id, passw)
        if bu["teacherid_mismatch"] is False:
            if bu["successful"] is True:
                return True
            return False
        else:
            return False


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
            if self.current_screen.name == "inup":
                return False  # exit the app from this page
            elif self.current_screen.name == "signin":
                self.transition.direction = 'right'
                self.current = "inup"
                return True  # do not exit the app
            elif self.current_screen.name == "signup":
                self.transition.direction = 'right'
                self.current = "inup"
                return True  # do not exit the app
            elif self.current_screen.name == "forpass":
                return True  # do not exit the app
            elif self.current_screen.name == "change_passo":
                return True  # do not exit the app
            elif self.current_screen.name == "inout":
                return False
            elif self.current_screen.name == "sels":
                return False  # do not exit the app
            elif self.current_screen.name == "cods":
                self.transition.direction = 'right'
                self.current = "sels"
                return True  # do not exit the app


class LoginApp(MDApp):
    user = {}

    def build(self):
        self.manager = ScreenManagement()
        self.manager.add_widget(Signin_signup(name='inup'))
        self.manager.add_widget(SignScreen(name='signin'))
        self.manager.add_widget(Sign_Up_Screen(name='signup'))
        self.manager.add_widget(ForPassScreen(name='forpass'))
        self.manager.add_widget(ChangePassScreen(name='change_passo'))
        self.cod_scr = CodePage(name="cods")
        self.sel_scr = SelectPage(name="sels")
        self.manager.add_widget(self.sel_scr)  # course code and shift
        self.manager.add_widget(self.cod_scr)  # qr code genrater

        pro_list = ["Data Structure and Algorithm CS20B302", "Principle of Programming Language CS20B305", "Java Programming CS20B303", "Operating System CS20B301",
                    "Project Based Learning-III PB20B301", "Quantative Aptitude-I UC20B302", "Linear Algebra AI20B306", "Probabilistic Modelling and Reasoning AI20B304", "Introduction to Cyber Security CY20B304"]
        program_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": i,
                "on_release": lambda x=i: self.set_item_p(x),
            } for i in pro_list]
        self.program = MDDropdownMenu(
            caller=self.sel_scr.ids.field_program,
            items=program_items,
            position="bottom",
            width_mult=7,
        )

        shift_list = ["8:30 to 9:20", "9:20 to 10:10", "10:10 to 11:00"]
        shift_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(50),
                "text": i,
                "on_release": lambda x=i: self.set_item_s(x),
            } for i in shift_list]
        self.shift = MDDropdownMenu(
            caller=self.sel_scr.ids.field_time,
            items=shift_items,
            position="bottom",
            width_mult=7,
        )
        icons_item = {
            "sort": "Sort",
            "sort-calendar-descending": "Sort attendance by date",
            "logout": "Logout"
        }
        for icon_name in icons_item.keys():
            self.sel_scr.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
        return self.manager

    def set_item_p(self, text__item):
        self.sel_scr.ids.field_program.text = text__item
        self.program.dismiss()

    def set_item_s(self, text__item):
        self.sel_scr.ids.field_time.text = text__item
        self.shift.dismiss()

    def otpgen(self, phone):
        self.my_otp = genotp(phone)["otp"]

    def add_User(self, f, l, ph, pa):
        dic = add_user(first_name=f, last_name=l, phone_no=ph, passw=pa)
        self.user["user_id"] = dic["user_id"]
    def qr_gen(self,data):
        create_qr(data);
        

LoginApp().run()
