import keyboard
import threading

class HotkeyListener:
    """Global hotkey listener for flashcard ratings"""
    
    def __init__(self):
        self.callbacks = {
            'again': None,
            'hard': None,
            'good': None,
            'easy': None
        }
        self.is_active = False
        self.registered_hotkeys = []
    
    def register_hotkeys(self, hotkey_again, hotkey_hard, hotkey_good, hotkey_easy,
                        on_again, on_hard, on_good, on_easy):
        """
        Register global hotkeys
        
        Args:
            hotkey_again: Hotkey string for 'Again' (e.g., 'ctrl+1')
            hotkey_hard: Hotkey string for 'Hard'
            hotkey_good: Hotkey string for 'Good'
            hotkey_easy: Hotkey string for 'Easy'
            on_again: Callback for 'Again'
            on_hard: Callback for 'Hard'
            on_good: Callback for 'Good'
            on_easy: Callback for 'Easy'
        """
        # Unregister existing hotkeys first
        self.unregister_hotkeys()
        
        # Store callbacks
        self.callbacks['again'] = on_again
        self.callbacks['hard'] = on_hard
        self.callbacks['good'] = on_good
        self.callbacks['easy'] = on_easy
        
        # Register new hotkeys
        try:
            keyboard.add_hotkey(hotkey_again, self._on_again_pressed, suppress=True)
            keyboard.add_hotkey(hotkey_hard, self._on_hard_pressed, suppress=True)
            keyboard.add_hotkey(hotkey_good, self._on_good_pressed, suppress=True)
            keyboard.add_hotkey(hotkey_easy, self._on_easy_pressed, suppress=True)
            
            self.registered_hotkeys = [hotkey_again, hotkey_hard, hotkey_good, hotkey_easy]
            self.is_active = True
            
            print(f"Hotkeys registered: Again={hotkey_again}, Hard={hotkey_hard}, Good={hotkey_good}, Easy={hotkey_easy}")
        
        except Exception as e:
            print(f"Error registering hotkeys: {e}")
            raise
    
    def unregister_hotkeys(self):
        """Unregister all hotkeys"""
        if self.registered_hotkeys:
            for hotkey in self.registered_hotkeys:
                try:
                    keyboard.remove_hotkey(hotkey)
                except:
                    pass
            
            self.registered_hotkeys = []
        
        self.is_active = False
        print("Hotkeys unregistered")
    
    def _on_again_pressed(self):
        """Internal callback for 'Again' hotkey"""
        if self.callbacks['again']:
            self.callbacks['again']()
    
    def _on_hard_pressed(self):
        """Internal callback for 'Hard' hotkey"""
        if self.callbacks['hard']:
            self.callbacks['hard']()
    
    def _on_good_pressed(self):
        """Internal callback for 'Good' hotkey"""
        if self.callbacks['good']:
            self.callbacks['good']()
    
    def _on_easy_pressed(self):
        """Internal callback for 'Easy' hotkey"""
        if self.callbacks['easy']:
            self.callbacks['easy']()
    
    def activate(self):
        """Activate hotkey listening"""
        self.is_active = True
    
    def deactivate(self):
        """Deactivate hotkey listening (but don't unregister)"""
        self.is_active = False