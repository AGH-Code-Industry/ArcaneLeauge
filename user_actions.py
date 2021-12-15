from kivy import platform

def is_desktop(self):
    if platform in ["linux", "win", "macosx"]:
        return True
    else:
        return False

def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "space":
        pass
    elif keycode[1] == "up":
        if self.current_level < 2:
            self.current_level += 1
    elif keycode[1] == "down":
        if self.current_level > 0:
            self.current_level -= 1
    return True

def on_keyboard_up(self, keyboard, keycode):
    return True