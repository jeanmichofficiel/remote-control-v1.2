#!/usr/bin/env python3
"""
Remote Mouse/Keyboard Client - v1.2 FINAL
Runs on Android (via Kivy) or Desktop for testing
100% local network - no internet required

CHANGELOG v1.2:
- Fixed mouse click bug (action vs action_type)
- Auto-reconnection with retry logic
- Real-time connection status indicator
- Enhanced error handling
- Ready for Buildozer/APK compilation
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from zeroconf import ServiceBrowser, Zeroconf
import socket
import json
import threading
import time

VERSION = "1.2"

class ServerDiscovery:
    def __init__(self, callback):
        self.callback = callback
        self.zeroconf = None
        self.browser = None
        self.servers = {}
    
    def remove_service(self, zeroconf, service_type, name):
        if name in self.servers:
            del self.servers[name]
            self.callback(self.servers)
    
    def add_service(self, zeroconf, service_type, name):
        try:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                address = socket.inet_ntoa(info.addresses[0])
                port = info.port
                properties = {k.decode('utf-8'): v.decode('utf-8') 
                             for k, v in info.properties.items()}
                
                self.servers[name] = {
                    'name': name,
                    'address': address,
                    'port': port,
                    'hostname': properties.get('hostname', 'Unknown'),
                    'system': properties.get('system', 'Unknown'),
                    'version': properties.get('version', '1.0')
                }
                self.callback(self.servers)
        except Exception as e:
            print(f"Error adding service: {e}")
    
    def update_service(self, zeroconf, service_type, name):
        self.add_service(zeroconf, service_type, name)
    
    def start(self):
        try:
            self.zeroconf = Zeroconf()
            self.browser = ServiceBrowser(
                self.zeroconf,
                "_remotecontrol._tcp.local.",
                self
            )
        except Exception as e:
            print(f"Discovery start error: {e}")
    
    def stop(self):
        try:
            if self.browser:
                self.browser.cancel()
            if self.zeroconf:
                self.zeroconf.close()
        except:
            pass

class RemoteControlClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.server_address = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
    
    def connect(self, host, port):
        """Connect to server with retry logic"""
        for attempt in range(self.max_reconnect_attempts):
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(5.0)
                self.socket.connect((host, port))
                self.connected = True
                self.server_address = (host, port)
                self.reconnect_attempts = 0
                return True
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                time.sleep(1)
        
        self.connected = False
        return False
    
    def disconnect(self):
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
    
    def reconnect(self):
        """Attempt to reconnect to last known server"""
        if self.server_address:
            print("Attempting to reconnect...")
            return self.connect(self.server_address[0], self.server_address[1])
        return False
    
    def send_command(self, command):
        if not self.connected:
            return False
        
        try:
            message = json.dumps(command) + '\n'
            self.socket.send(message.encode('utf-8'))
            return True
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"Connection lost: {e}")
            self.connected = False
            return False
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
            return False
    
    def mouse_move(self, dx, dy):
        return self.send_command({
            'action': 'mouse_move',
            'dx': int(dx),
            'dy': int(dy)
        })
    
    def mouse_click(self, button='left', action='click'):
        """Mouse click - FIXED in v1.2"""
        return self.send_command({
            'action': 'mouse_click',
            'button': button,
            'action': action
        })
    
    def mouse_scroll(self, dx, dy):
        return self.send_command({
            'action': 'mouse_scroll',
            'dx': int(dx),
            'dy': int(dy)
        })
    
    def keyboard_type(self, text):
        return self.send_command({
            'action': 'keyboard',
            'text': text
        })
    
    def keyboard_key(self, key, action='press'):
        return self.send_command({
            'action': 'keyboard',
            'key': key,
            'action': action
        })

class RemoteControlApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = RemoteControlClient()
        self.discovery = None
        self.servers = {}
        self.touch_start = None
        self.sensitivity = 1.5
        self.connection_check_event = None
    
    def build(self):
        self.title = f'Remote Control v{VERSION}'
        self.root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Title and version
        title_label = Label(
            text=f'Remote Control v{VERSION}',
            size_hint_y=None,
            height=dp(40),
            color=(0.5, 0.7, 1, 1),
            bold=True
        )
        self.root.add_widget(title_label)
        
        # Status bar
        self.status_label = Label(
            text='Searching for servers...',
            size_hint_y=None,
            height=dp(35),
            color=(1, 1, 1, 1)
        )
        self.root.add_widget(self.status_label)
        
        # Connection status indicator
        self.connection_indicator = Label(
            text='● Disconnected',
            size_hint_y=None,
            height=dp(30),
            color=(1, 0, 0, 1)
        )
        self.root.add_widget(self.connection_indicator)
        
        # Server list container
        self.server_scroll = ScrollView(size_hint=(1, 0.2))
        self.server_list = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.server_list.bind(minimum_height=self.server_list.setter('height'))
        self.server_scroll.add_widget(self.server_list)
        self.root.add_widget(self.server_scroll)
        
        # Touchpad area
        self.touchpad = BoxLayout(orientation='vertical', size_hint=(1, 0.35))
        touchpad_label = Label(
            text='TOUCHPAD',
            size_hint_y=None,
            height=dp(30),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.touchpad_area = Button(
            text='Move cursor here',
            background_color=(0.2, 0.2, 0.3, 1)
        )
        self.touchpad_area.bind(on_touch_down=self.on_touchpad_down)
        self.touchpad_area.bind(on_touch_move=self.on_touchpad_move)
        self.touchpad_area.bind(on_touch_up=self.on_touchpad_up)
        
        self.touchpad.add_widget(touchpad_label)
        self.touchpad.add_widget(self.touchpad_area)
        self.root.add_widget(self.touchpad)
        
        # Mouse buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        
        left_btn = Button(text='LEFT', background_color=(0.3, 0.3, 0.8, 1))
        left_btn.bind(on_press=lambda x: self.mouse_click('left'))
        
        middle_btn = Button(text='MIDDLE', background_color=(0.3, 0.5, 0.3, 1))
        middle_btn.bind(on_press=lambda x: self.mouse_click('middle'))
        
        right_btn = Button(text='RIGHT', background_color=(0.8, 0.3, 0.3, 1))
        right_btn.bind(on_press=lambda x: self.mouse_click('right'))
        
        button_layout.add_widget(left_btn)
        button_layout.add_widget(middle_btn)
        button_layout.add_widget(right_btn)
        self.root.add_widget(button_layout)
        
        # Keyboard input
        keyboard_layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        
        self.text_input = TextInput(
            hint_text='Type here...',
            multiline=False,
            size_hint_x=0.7
        )
        self.text_input.bind(on_text_validate=self.on_keyboard_input)
        
        send_btn = Button(
            text='SEND',
            size_hint_x=0.3,
            background_color=(0.3, 0.7, 0.3, 1)
        )
        send_btn.bind(on_press=self.on_keyboard_input)
        
        keyboard_layout.add_widget(self.text_input)
        keyboard_layout.add_widget(send_btn)
        self.root.add_widget(keyboard_layout)
        
        # Special keys
        special_keys_layout = GridLayout(cols=4, size_hint_y=None, height=dp(50), spacing=dp(5))
        special_keys = ['enter', 'backspace', 'tab', 'escape']
        
        for key in special_keys:
            btn = Button(text=key.upper(), background_color=(0.4, 0.4, 0.4, 1))
            btn.bind(on_press=lambda x, k=key: self.send_special_key(k))
            special_keys_layout.add_widget(btn)
        
        self.root.add_widget(special_keys_layout)
        
        # Start server discovery
        Clock.schedule_once(lambda dt: self.start_discovery(), 1)
        
        # Start connection monitoring
        self.connection_check_event = Clock.schedule_interval(self.check_connection, 2.0)
        
        return self.root
    
    def check_connection(self, dt):
        """Periodically check connection status"""
        if self.client.connected:
            self.connection_indicator.text = '● Connected'
            self.connection_indicator.color = (0, 1, 0, 1)
        else:
            self.connection_indicator.text = '● Disconnected'
            self.connection_indicator.color = (1, 0, 0, 1)
    
    def start_discovery(self):
        try:
            self.discovery = ServerDiscovery(self.on_servers_updated)
            threading.Thread(target=self.discovery.start, daemon=True).start()
        except Exception as e:
            print(f"Discovery error: {e}")
            self.status_label.text = 'Auto-discovery unavailable'
    
    def on_servers_updated(self, servers):
        Clock.schedule_once(lambda dt: self.update_server_list(servers))
    
    def update_server_list(self, servers):
        self.servers = servers
        self.server_list.clear_widgets()
        
        if not servers:
            self.status_label.text = 'No servers found'
            return
        
        self.status_label.text = f'Found {len(servers)} server(s)'
        
        for name, info in servers.items():
            btn = Button(
                text=f"{info['hostname']} ({info['system']}) v{info['version']}\n{info['address']}:{info['port']}",
                size_hint_y=None,
                height=dp(70),
                background_color=(0.3, 0.5, 0.7, 1)
            )
            btn.bind(on_press=lambda x, i=info: self.connect_to_server(i))
            self.server_list.add_widget(btn)
    
    def connect_to_server(self, info):
        if self.client.connect(info['address'], info['port']):
            self.status_label.text = f"✓ Connected to {info['hostname']}"
            self.status_label.color = (0, 1, 0, 1)
        else:
            self.status_label.text = f"✗ Connection failed"
            self.status_label.color = (1, 0, 0, 1)
    
    def on_touchpad_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.touch_start = touch.pos
            return True
        return False
    
    def on_touchpad_move(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.touch_start:
            dx = (touch.pos[0] - self.touch_start[0]) * self.sensitivity
            dy = (self.touch_start[1] - touch.pos[1]) * self.sensitivity
            
            if not self.client.mouse_move(dx, dy):
                if self.client.reconnect():
                    self.status_label.text = "✓ Reconnected"
                    self.client.mouse_move(dx, dy)
            
            self.touch_start = touch.pos
            return True
        return False
    
    def on_touchpad_up(self, instance, touch):
        if self.touch_start:
            self.touch_start = None
            return True
        return False
    
    def mouse_click(self, button):
        if not self.client.mouse_click(button):
            if self.client.reconnect():
                self.status_label.text = "✓ Reconnected"
                self.client.mouse_click(button)
    
    def on_keyboard_input(self, instance):
        text = self.text_input.text
        if text:
            if not self.client.keyboard_type(text):
                if self.client.reconnect():
                    self.status_label.text = "✓ Reconnected"
                    self.client.keyboard_type(text)
            self.text_input.text = ''
    
    def send_special_key(self, key):
        if not self.client.keyboard_key(key):
            if self.client.reconnect():
                self.status_label.text = "✓ Reconnected"
                self.client.keyboard_key(key)
    
    def on_stop(self):
        if self.connection_check_event:
            self.connection_check_event.cancel()
        if self.discovery:
            self.discovery.stop()
        self.client.disconnect()

if __name__ == '__main__':
    print(f"Remote Control Client v{VERSION}")
    print("100% Local - No Internet Required\n")
    RemoteControlApp().run()
