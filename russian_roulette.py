import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import os
import sys
import psutil
import gc
import ctypes
from ctypes import wintypes
import subprocess
import random

class RussianRouletteGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 RUSSIAN ROULETTE - SYSTEM DESTROYER 🎯")
        self.root.geometry("600x500")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Game variables
        self.target_number = random.randint(1, 10)
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.game_active = True
        
        self.setup_ui()
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎯 RUSSIAN ROULETTE 🎯", 
            font=('Arial', 24, 'bold'),
            fg='#ff4444',
            bg='#1a1a1a'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Guess the number between 1-10 or face REAL SYSTEM CRASH!",
            font=('Arial', 12),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        subtitle_label.pack(pady=10)
        
        # Number selection frame
        number_frame = tk.Frame(self.root, bg='#1a1a1a')
        number_frame.pack(pady=20)
        
        # Create number buttons
        self.number_buttons = []
        for i in range(1, 11):
            btn = tk.Button(
                number_frame,
                text=str(i),
                font=('Arial', 16, 'bold'),
                width=4,
                height=2,
                bg='#333333',
                fg='white',
                activebackground='#555555',
                command=lambda x=i: self.select_number(x)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.number_buttons.append(btn)
        
        # Selected number display
        self.selected_label = tk.Label(
            self.root,
            text="Select a number above",
            font=('Arial', 14),
            fg='#ffff00',
            bg='#1a1a1a'
        )
        self.selected_label.pack(pady=10)
        
        # Guess button
        self.guess_button = tk.Button(
            self.root,
            text="PULL THE TRIGGER",
            font=('Arial', 16, 'bold'),
            bg='#ff4444',
            fg='white',
            activebackground='#ff6666',
            command=self.make_guess,
            state=tk.DISABLED
        )
        self.guess_button.pack(pady=20)
        
        # Result display
        self.result_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 16, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a',
            wraplength=500
        )
        self.result_label.pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg='#1a1a1a')
        stats_frame.pack(pady=20)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Games: 0 | Wins: 0 | Losses: 0",
            font=('Arial', 12),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        self.stats_label.pack()
        
        # Warning label
        warning_label = tk.Label(
            self.root,
            text="⚠️ WARNING: This will actually crash your system! ⚠️",
            font=('Arial', 10, 'bold'),
            fg='#ff0000',
            bg='#1a1a1a'
        )
        warning_label.pack(pady=10)
        
        self.selected_number = None
    
    def select_number(self, number):
        """Handle number selection"""
        if not self.game_active:
            return
            
        self.selected_number = number
        self.selected_label.config(text=f"Selected: {number}")
        self.guess_button.config(state=tk.NORMAL)
        
        # Highlight selected button
        for i, btn in enumerate(self.number_buttons):
            if i + 1 == number:
                btn.config(bg='#ff4444', fg='white')
            else:
                btn.config(bg='#333333', fg='white')
    
    def make_guess(self):
        """Handle the guess"""
        if not self.game_active or self.selected_number is None:
            return
            
        self.game_active = False
        self.games_played += 1
        
        # Disable all buttons
        self.guess_button.config(state=tk.DISABLED)
        for btn in self.number_buttons:
            btn.config(state=tk.DISABLED)
        
        # Show result
        if self.selected_number == self.target_number:
            self.handle_win()
        else:
            self.handle_loss()
    
    def handle_win(self):
        """Handle winning"""
        self.wins += 1
        self.result_label.config(
            text="🎉 CONGRATULATIONS! You survived! 🎉",
            fg='#00ff00'
        )
        self.update_stats()
        
        # Reset after 3 seconds
        self.root.after(3000, self.reset_game)
    
    def handle_loss(self):
        """Handle losing - TRIGGER REAL SYSTEM CRASH"""
        self.losses += 1
        self.result_label.config(
            text="💀 WRONG GUESS! System crash initiated... 💀",
            fg='#ff0000'
        )
        self.update_stats()
        
        # Show crash message box
        self.root.after(1000, self.show_crash_message)
    
    def show_crash_message(self):
        """Show the crash message box"""
        messagebox.showerror(
            "SYSTEM CRASH DETECTED",
            "CRITICAL ERROR: Wrong guess detected!\n\n"
            "Your system is now experiencing:\n"
            "• Memory overflow\n"
            "• CPU overload\n"
            "• System instability\n\n"
            "The only solution is to RESTART your computer!\n\n"
            "Good luck! 💀"
        )
        
        # Start the actual crash sequence
        self.root.after(500, self.trigger_system_crash)
    
    def trigger_system_crash(self):
        """Trigger multiple crash mechanisms simultaneously"""
        # Start crash threads
        crash_threads = [
            threading.Thread(target=self.memory_bomb, daemon=True),
            threading.Thread(target=self.cpu_bomb, daemon=True),
            threading.Thread(target=self.system_call_bomb, daemon=True),
            threading.Thread(target=self.file_system_bomb, daemon=True),
            threading.Thread(target=self.network_bomb, daemon=True),
            threading.Thread(target=self.registry_bomb, daemon=True)
        ]
        
        for thread in crash_threads:
            thread.start()
        
        # Also try to crash the GUI
        self.crash_gui()
    
    def memory_bomb(self):
        """Consume all available memory"""
        try:
            memory_list = []
            while True:
                # Allocate 100MB chunks
                memory_list.append('x' * (100 * 1024 * 1024))
                time.sleep(0.001)  # Small delay to prevent immediate crash
        except:
            pass
    
    def cpu_bomb(self):
        """Consume all CPU resources"""
        try:
            while True:
                # Infinite loop consuming CPU
                pass
        except:
            pass
    
    def system_call_bomb(self):
        """Make excessive system calls"""
        try:
            while True:
                # Make system calls that can cause instability
                os.getpid()
                os.getcwd()
                time.sleep(0.001)
        except:
            pass
    
    def file_system_bomb(self):
        """Create excessive file operations"""
        try:
            counter = 0
            while True:
                # Create temporary files
                with open(f"temp_crash_{counter}.tmp", "w") as f:
                    f.write("x" * 1000)
                counter += 1
                if counter > 10000:  # Prevent infinite file creation
                    break
        except:
            pass
    
    def network_bomb(self):
        """Attempt to create network connections"""
        try:
            while True:
                # Try to create network connections
                subprocess.Popen(['ping', '127.0.0.1'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                time.sleep(0.1)
        except:
            pass
    
    def registry_bomb(self):
        """Attempt registry operations (Windows only)"""
        try:
            if sys.platform == "win32":
                import winreg
                while True:
                    # Try to access registry keys
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software")
                    winreg.CloseKey(key)
                    time.sleep(0.001)
        except:
            pass
    
    def crash_gui(self):
        """Crash the GUI itself"""
        try:
            # Create infinite windows
            while True:
                crash_window = tk.Toplevel(self.root)
                crash_window.title("CRASH")
                crash_window.geometry("100x100")
                crash_window.configure(bg='red')
                time.sleep(0.01)
        except:
            pass
    
    def update_stats(self):
        """Update statistics display"""
        self.stats_label.config(
            text=f"Games: {self.games_played} | Wins: {self.wins} | Losses: {self.losses}"
        )
    
    def reset_game(self):
        """Reset the game for another round"""
        self.game_active = True
        self.target_number = random.randint(1, 10)
        self.selected_number = None
        self.selected_label.config(text="Select a number above")
        self.result_label.config(text="", fg='#ffffff')
        
        # Re-enable buttons
        self.guess_button.config(state=tk.DISABLED)
        for btn in self.number_buttons:
            btn.config(state=tk.NORMAL, bg='#333333', fg='white')
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🎯 RUSSIAN ROULETTE - SYSTEM DESTROYER 🎯")
    print("WARNING: This game will actually crash your system!")
    print("Make sure you save all your work before playing!")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    
    try:
        input()
        game = RussianRouletteGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame cancelled. Your system is safe!")
        sys.exit(0)
