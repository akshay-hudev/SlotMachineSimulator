import random
import tkinter as tk
from tkinter import messagebox

# Constants
INIT_STAKE = 5000
ITEMS = ["🍒", "💰", "🎱", "🐍"]
SPIN_DURATION = 2  # Duration for spin animation in seconds
SPIN_INTERVAL = 0.1  # Interval between symbol updates during spin in seconds
WIN_AMOUNT_BIG = 25000  # Amount won for three matching symbols
WIN_AMOUNT_SMALL = 5000  # Amount won for two matching symbols
LOSS_AMOUNT = -1000  # Amount lost for no matching symbols

class SlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Simulator")
        self.root.geometry("800x600")
        self.stake = INIT_STAKE

        self.create_ui_elements()

    def create_ui_elements(self):
        """
        Create and arrange all UI elements for the slot machine.
        """
        # Create the main canvas for drawing slot machine elements
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Draw the slot machine background
        self.canvas.create_rectangle(50, 50, 750, 550, fill="lightgray", outline="black", width=2)

        # Create wheels for slot machine symbols
        self.wheels = []
        for i in range(3):
            wheel = self.canvas.create_text(150 + i * 200, 300, text="", font=("Arial", 100))
            self.wheels.append(wheel)

        # Create result label to display win/loss messages
        self.result_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.result_label.place(x=300, y=500)

        # Create spin button to trigger the spin action
        self.spin_button = tk.Button(self.root, text="Spin", font=("Arial", 16), command=self.start_spin)
        self.spin_button.place(x=350, y=550)

        # Create stake display label to show the current stake
        self.stake_label = tk.Label(self.root, text=f"Stake: ₹{self.stake}", font=("Arial", 16))
        self.stake_label.place(x=50, y=20)

    def start_spin(self):
        """
        Disable the spin button and start the spinning animation.
        """
        self.spin_button.config(state="disabled")
        # Schedule the end of the spin animation
        self.root.after(int(SPIN_DURATION * 1000), self.end_spin)
        self.spin_wheels()

    def spin_wheels(self):
        """
        Animate the spinning of the slot machine wheels by updating symbols.
        """
        # Randomly choose symbols for each wheel
        symbols = [random.choice(ITEMS) for _ in range(3)]
        for i, symbol in enumerate(symbols):
            self.canvas.itemconfig(self.wheels[i], text=symbol)
        self.canvas.update()
        # Continue updating symbols at intervals if spin is still active
        if self.spin_button['state'] == 'disabled':
            self.root.after(int(SPIN_INTERVAL * 1000), self.spin_wheels)

    def end_spin(self):
        """
        Enable the spin button and determine the result of the spin.
        """
        self.spin_button.config(state="normal")

        # Retrieve the symbols displayed on the wheels
        symbols = [self.canvas.itemcget(wheel, "text") for wheel in self.wheels]
        result_text, win_amount = self.determine_result(symbols)

        # Update the stake based on the result
        self.stake += win_amount
        self.stake_label.config(text=f"Stake: ₹{self.stake}")
        self.result_label.config(text=result_text)

        # Check if the stake has fallen to zero or below
        if self.stake <= 0:
            messagebox.showinfo("Game Over", "You have run out of money!")
            self.root.quit()

    def determine_result(self, symbols):
        """
        Determine the result of the spin based on the symbols.
        
        Parameters:
            symbols (list): List of symbols displayed on the wheels.

        Returns:
            tuple: A message and the amount won or lost.
        """
        if symbols[0] == symbols[1] == symbols[2]:
            return "You win ₹25000", WIN_AMOUNT_BIG
        elif symbols[0] == symbols[1] or symbols[0] == symbols[2] or symbols[1] == symbols[2]:
            return "You win ₹5000", WIN_AMOUNT_SMALL
        else:
            return "You lose ₹1000", LOSS_AMOUNT

def main():
    """
    Initialize the main application window and start the slot machine.
    """
    root = tk.Tk()
    slot_machine = SlotMachine(root)
    root.mainloop()

if __name__ == "__main__":
    main()
