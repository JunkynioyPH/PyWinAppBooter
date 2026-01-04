# Gemini Generated
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

def get_dark_palette():
    dark_palette = QPalette()

    # Base colors
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    
    # Highlight colors
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    
    # Disabled state (optional but recommended)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.darkGray)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.darkGray)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.darkGray)

    return dark_palette

def get_mint_blue_dark_palette():
    palette = QPalette()

    # Core Mint-Y Dark Colors
    mint_charcoal = QColor(47, 47, 47)      # Standard background
    mint_darker = QColor(36, 36, 36)        # Input fields / Base
    mint_blue = QColor(30, 120, 210)        # Official Mint Blue accent
    mint_text = QColor(211, 211, 211)       # Light grey text

    # Base window colors
    palette.setColor(QPalette.ColorRole.Window, mint_charcoal)
    palette.setColor(QPalette.ColorRole.WindowText, mint_text)
    palette.setColor(QPalette.ColorRole.Base, mint_darker)
    palette.setColor(QPalette.ColorRole.AlternateBase, mint_charcoal)
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.ToolTipText, mint_text)
    palette.setColor(QPalette.ColorRole.Text, mint_text)
    
    # Buttons
    palette.setColor(QPalette.ColorRole.Button, mint_charcoal)
    palette.setColor(QPalette.ColorRole.ButtonText, mint_text)
    
    # The Blue Tint (Highlights and Links)
    palette.setColor(QPalette.ColorRole.Highlight, mint_blue)
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Link, mint_blue)
    palette.setColor(QPalette.ColorRole.BrightText, mint_blue)

    # Disabled elements (important for that "Mint" look)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(100, 100, 100))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(100, 100, 100))

    return palette