import os
import random
from datetime import datetime

import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

kivy.require("2.1.0")

Window.size = (400, 700)

# Custom TextInput that shows text immediately
class VisibleTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_color = (0, 0, 0, 1)
        self.background_color = (1, 1, 1, 1)
        self.cursor_color = (0.2, 0.8, 0.3, 1)
        self.font_size = '14sp'
        self.padding = [12, 12, 12, 12]
        self.size_hint_y = None
        self.height = 50
        self.multiline = False

class ChatBubble(BoxLayout):
    text = StringProperty("")
    is_sender = BooleanProperty(False)
    timestamp = StringProperty("")
    status = StringProperty("")

class LoginScreen(Screen):
    def do_login(self):
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()
        
        if email and password:
            button = self.ids.login_btn
            Animation.cancel_all(button)
            animation = Animation(opacity=0.75, duration=0.08) + Animation(opacity=1, duration=0.12)
            animation.start(button)
            Clock.schedule_once(lambda *_: self.login_success(), 0.2)
        else:
            self.show_error("Please enter email and password")
    
    def show_error(self, message):
        error_label = self.ids.error_label
        Animation.cancel_all(error_label)
        error_label.text = message
        error_label.opacity = 1
        Animation(opacity=0, duration=2).start(error_label)
    
    def login_success(self):
        chat_screen = self.manager.get_screen("chat")
        chat_screen.connect()
        self.manager.current = "chat"

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        self.typing_event = None
        
    def on_pre_leave(self, *_args):
        self.stop_typing_simulation()
        self.show_typing_indicator(False)
    
    def leave_chat(self):
        self.stop_typing_simulation()
        self.show_typing_indicator(False)
        self.manager.current = "login"
    
    def stop_typing_simulation(self):
        if self.typing_event is not None:
            self.typing_event.cancel()
            self.typing_event = None
    
    def connect(self):
        self.stop_typing_simulation()
        self.reset_chat()
        self.update_online_status(True)
        self.load_sample_messages()
        self.typing_event = Clock.schedule_interval(self.simulate_typing, 10)
    
    def reset_chat(self):
        self.ids.chat_container.clear_widgets()
        self.ids.msg.text = ""
        self.messages.clear()
    
    def update_online_status(self, is_online):
        status_label = self.ids.online_status
        Animation.cancel_all(status_label)
        
        if is_online:
            status_label.text = "● Online"
            status_label.color = [0.2, 0.9, 0.2, 1]
            animation = Animation(color=[0.2, 0.9, 0.2, 0.5], duration=1) + Animation(
                color=[0.2, 0.9, 0.2, 1], duration=1
            )
            animation.repeat = True
            animation.start(status_label)
        else:
            status_label.text = "○ Offline"
            status_label.color = [0.7, 0.7, 0.7, 1]
    
    def load_sample_messages(self):
        sample_messages = [
            ("Welcome to the Farmer Chat Group! 🌾", False, "10:30 AM", ""),
            ("Hello everyone! How's the harvest going?", True, "10:32 AM", "read"),
            ("Great weather for farming today!", False, "10:35 AM", ""),
            ("Has anyone tried the new seeds?", True, "10:38 AM", "sent"),
            ("Yes, the new seeds are great!", False, "10:40 AM", ""),
            ("Where can I buy them?", True, "10:42 AM", "delivered"),
            ("Check the local agricultural store", False, "10:43 AM", ""),
        ]
        
        for text, is_sender, timestamp, status in sample_messages:
            self.add_message(text, is_sender, timestamp, status, scroll=False)
        
        # Scroll to bottom after loading all messages
        Clock.schedule_once(self.scroll_to_bottom, 0.2)
    
    def add_message(self, text, is_sender, timestamp=None, status="sent", scroll=True):
        if timestamp is None:
            timestamp = datetime.now().strftime("%I:%M %p")
        
        bubble = ChatBubble(
            text=text,
            is_sender=is_sender,
            timestamp=timestamp,
            status=status if is_sender else "",
        )
        bubble.size_hint_y = None
        bubble.height = bubble.minimum_height
        
        self.ids.chat_container.add_widget(bubble)
        self.messages.append(bubble)
        
        # Animate bubble
        bubble.opacity = 0
        Clock.schedule_once(lambda *_: self.animate_bubble(bubble), 0.05)
        
        # Scroll to bottom if needed
        if scroll:
            Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def animate_bubble(self, bubble):
        Animation.cancel_all(bubble)
        anim = Animation(opacity=1, duration=0.3, t="out_quad")
        anim.start(bubble)
    
    def send(self):
        msg_text = self.ids.msg.text.strip()
        if not msg_text:
            return
        
        self.add_message(msg_text, True, status="sent", scroll=True)
        self.ids.msg.text = ""
        self.animate_send_button()
        self.update_message_statuses()
        
        # Simulate reply
        Clock.schedule_once(lambda *_: self.simulate_reply(msg_text), random.uniform(1.5, 3.0))
    
    def simulate_reply(self, _user_message):
        replies = [
            "That's interesting! Tell me more 🌱",
            "I agree with you on that! 👍",
            "Thanks for sharing your experience!",
            "Has anyone else tried this method?",
            "Great point! Let's discuss more 💬",
        ]
        
        reply = random.choice(replies)
        self.show_typing_indicator(True)
        reply_delay = random.uniform(0.9, 1.8)
        Clock.schedule_once(lambda *_: self.add_message(reply, False, scroll=True), reply_delay)
        Clock.schedule_once(lambda *_: self.show_typing_indicator(False), reply_delay + 0.05)
    
    def simulate_typing(self, _dt):
        if random.random() < 0.3:
            self.show_typing_indicator(True)
            Clock.schedule_once(lambda *_: self.show_typing_indicator(False), random.uniform(1.2, 2.2))
    
    def show_typing_indicator(self, show):
        typing_label = self.ids.typing_status
        Animation.cancel_all(typing_label)
        
        if show:
            typing_label.text = "Someone is typing..."
            Animation(opacity=1, duration=0.15).start(typing_label)
        else:
            typing_label.text = ""
            typing_label.opacity = 0
    
    def update_message_statuses(self):
        sender_messages = [message for message in self.messages if message.is_sender]
        for index, message in enumerate(reversed(sender_messages)):
            if index == 0:
                message.status = "read"
            elif index < 3:
                message.status = "delivered"
            else:
                message.status = "sent"
    
    def scroll_to_bottom(self, *args):
        # Force scroll to bottom
        scroll_view = self.ids.chat_scroll
        scroll_view.scroll_y = 0
        
        # Update container height to ensure scrolling works
        container = self.ids.chat_container
        container.height = container.minimum_height
    
    def animate_send_button(self):
        button = self.ids.send_btn
        Animation.cancel_all(button)
        animation = Animation(opacity=0.75, duration=0.08) + Animation(opacity=1, duration=0.08)
        animation.start(button)
    
    def send_image(self):
        self.add_message("📷 Image shared", True, status="sent", scroll=True)
        self.update_message_statuses()
        self.animate_send_button()
        self.show_typing_indicator(True)
        Clock.schedule_once(lambda *_: self.add_message("Nice picture! 🌄", False, scroll=True), 1.2)
        Clock.schedule_once(lambda *_: self.show_typing_indicator(False), 1.25)
    
    def send_voice(self):
        self.add_message("🎤 Voice message (0:32)", True, status="sent", scroll=True)
        self.update_message_statuses()
        self.animate_send_button()
        self.show_typing_indicator(True)
        Clock.schedule_once(lambda *_: self.add_message("Thanks for the voice note! 🎧", False, scroll=True), 1.4)
        Clock.schedule_once(lambda *_: self.show_typing_indicator(False), 1.45)

class FarmerChatApp(App):
    def build(self):
        self.title = "Farmer Connect - Agricultural Community"
        kv_path = os.path.join(os.path.dirname(__file__), "main.kv")
        return Builder.load_file(kv_path)
    
    def on_start(self):
        if self.root:
            self.root.opacity = 0
            Animation(opacity=1, duration=0.35).start(self.root)

if __name__ == "__main__":
    FarmerChatApp().run()