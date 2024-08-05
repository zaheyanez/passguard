from PyQt5.QtWidgets import QPushButton
from pyguard.config import APP_THEME_COLOR

def adjust_color_brightness(color, factor):
    """Adjusts the brightness of the given color."""
    color = color.lstrip('#')
    r, g, b = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    r = min(max(0, r + factor), 255)
    g = min(max(0, g + factor), 255)
    b = min(max(0, b + factor), 255)
    return f'#{r:02X}{g:02X}{b:02X}'

class BaseButton(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)

    def set_active(self, active):
        self.update_style(active)

    def update_style(self, active):
        raise NotImplementedError("Must be implemented in subclasses")

class SidebarButton(BaseButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.update_style(False)

    def update_style(self, active):
        color = APP_THEME_COLOR if active else "#2D2D2D"
        hover_color = adjust_color_brightness(color, -20) if active else "#3C3C3C"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #FFFFFF;
                border: none;
                padding: 20px;
                font-size: 16px;
                text-align: left;
                border-radius: 0;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

class StandardButton(BaseButton):
    @staticmethod
    def button_style():
        return f"""
            QPushButton {{
                background-color: #555;
                border: 1px solid #777;
                border-radius: 5px;
                color: #E0E0E0;
                font-size: 14px;
                padding: 7px 14px;
            }}
            QPushButton:hover {{
                background-color: #666;
                border: 1px solid #888;
            }}
        """

    @staticmethod  
    def primary_button_style():
        return f"""
            QPushButton {{
                background-color: {APP_THEME_COLOR};
                border: 1px solid {APP_THEME_COLOR};
                border-radius: 5px;
                color: #FFFFFF;
                font-size: 14px;
                padding: 7px 14px;
            }}
            QPushButton:hover {{
                background-color: {adjust_color_brightness(APP_THEME_COLOR, -20)};
            }}
        """