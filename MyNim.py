import tkinter as tk
from tkinter import messagebox


class NimGameApp: # includes all game mechanics
    def __init__(self, root):
        self.root = root
        self.root.title("Nim Game")
        self.current_piles = [1, 3, 5, 7]
        self.user_first = True
        self.init_welcome_screen()

    def reset_game(self):
        # change variables to original values
        self.current_piles = [1, 3, 5, 7]
        self.init_welcome_screen()

    def init_welcome_screen(self):
        # welcome page
        self.clear_screen()
        label = tk.Label(self.root, text="Welcome to the Nim Game!", font=("Arial", 24))
        label.pack(pady=20)

        start_first_label = tk.Label(self.root, text="Do you want to go first?", font=("Arial", 18))
        start_first_label.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        yes_button = tk.Button(button_frame, text="Yes", font=("Arial", 16),
                               command=lambda: self.start_game(user_first=True))
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(button_frame, text="No", font=("Arial", 16),
                              command=lambda: self.start_game(user_first=False))
        no_button.pack(side=tk.RIGHT, padx=10)

    def start_game(self, user_first):
        # picks who starts given user input
        self.user_first = user_first
        self.init_game_screen()

    def init_game_screen(self):
        # game page
        self.clear_screen()

        tk.Label(self.root, text="Nim Game", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Click on a pile to remove objects.", font=("Arial", 16)).pack(pady=10)

        self.piles_frame = tk.Frame(self.root)
        self.piles_frame.pack(pady=20)
        self.update_piles_ui()

        self.status_label = tk.Label(self.root, text="Your Turn!" if self.user_first else "AI's Turn...",
                                     font=("Arial", 16))
        self.status_label.pack(pady=10)

        if not self.user_first:
            self.root.after(1000, self.ai_turn)

    def update_piles_ui(self):
        # after objects r removed from file, change to display the changes
        for widget in self.piles_frame.winfo_children():
            widget.destroy()

        for i, pile in enumerate(self.current_piles):
            pile_frame = tk.Frame(self.piles_frame)
            pile_frame.pack(side=tk.LEFT, padx=20)

            tk.Label(pile_frame, text=f"Pile {i + 1}", font=("Arial", 14)).pack(pady=5)

            for _ in range(pile):
                square = tk.Canvas(pile_frame, width=20, height=20, bg="blue")
                square.pack(pady=2)

            if pile > 0:
                tk.Button(pile_frame, text="Remove", command=lambda i=i: self.remove_objects(i)).pack(pady=5)

    def remove_objects(self, pile_index):
        # removes objects from file
        pile_size = self.current_piles[pile_index]

        if pile_size == 0:
            messagebox.showerror("Error", "This pile is empty!")
            return

        # number of objects to remove
        top = tk.Toplevel(self.root)
        top.title("Remove Objects")
        tk.Label(top, text=f"Pile {pile_index + 1} - Choose objects to remove:", font=("Arial", 14)).pack(pady=10)

        #implementing the removal/changes of piles
        for i in range(1, 4):
            if i <= pile_size:
                tk.Button(top, text=f"Remove {i}", font=("Arial", 12),
                          command=lambda i=i: self.apply_user_move(pile_index, i, top)).pack(pady=5)

    def apply_user_move(self, pile_index, objects_to_remove, window):
        # implement change in piles
        self.current_piles[pile_index] -= objects_to_remove
        window.destroy()
        self.update_piles_ui()

        if all(pile == 0 for pile in self.current_piles):
            self.show_game_over_screen(winner="AI")
        else:
            self.status_label.config(text="AI's Turn...")
            self.root.after(1000, self.ai_turn)

    def ai_turn(self):
        # ai makes move, then update the piles to reflect ai choise
        best_move = self.get_ai_move()
        if best_move:
            pile_index, objects_to_remove = best_move
            self.current_piles[pile_index] -= objects_to_remove

        self.update_piles_ui()

        if all(pile == 0 for pile in self.current_piles):
            self.show_game_over_screen(winner="User")
        else:
            self.status_label.config(text="Your Turn!")

    def minimax(self, piles, maximizing):
        # minimax implementation
        if all(pile == 0 for pile in piles):
            return -1 if maximizing else 1  # AI wins: 1, AI loses: -1

        if maximizing:
            best_score = float('-inf')
            for pile_index, pile in enumerate(piles):
                for remove in range(1, 4):
                    if pile >= remove:
                        new_piles = piles[:]
                        new_piles[pile_index] -= remove
                        score = self.minimax(new_piles, maximizing=False)
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for pile_index, pile in enumerate(piles):
                for remove in range(1, 4):
                    if pile >= remove:
                        new_piles = piles[:]
                        new_piles[pile_index] -= remove
                        score = self.minimax(new_piles, maximizing=True)
                        best_score = min(best_score, score)
            return best_score

    def get_ai_move(self):
        # use minimax to find ai move
        best_move = None
        best_score = float('-inf')

        for pile_index, pile in enumerate(self.current_piles):
            for remove in range(1, 4):
                if pile >= remove:
                    new_piles = self.current_piles[:]
                    new_piles[pile_index] -= remove
                    score = self.minimax(new_piles, maximizing=False)

                    if score > best_score:
                        best_score = score
                        best_move = (pile_index, remove)

        return best_move

    def show_game_over_screen(self, winner):
        # after game ends, show winner, option to restart
        self.clear_screen()
        message = f"Game Over! {winner} wins!"
        tk.Label(self.root, text=message, font=("Arial", 24)).pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        play_again_button = tk.Button(button_frame, text="Play Again", font=("Arial", 16),
                                      command=self.reset_game)
        play_again_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 16),
                                command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def clear_screen(self):
        #removes all widgets from the window
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = NimGameApp(root)
    root.mainloop()

