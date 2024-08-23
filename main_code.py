import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import pygame

root = Tk()
root.title("KNOWLEDGEABLE KNIGHT")
width=root.winfo_screenwidth()
height=root.winfo_screenheight()
root.geometry("%dx%d" %(width,height))
label = Label(root)
label.pack()

image1 = Image.open('C:\\Users\\pvars\\OneDrive\\Desktop\\ezgif.com-resize.gif')

# Set the desired size for the GIF
desired_width = 400
desired_height = 300

# Resize each frame of the GIF
frames = [ImageTk.PhotoImage(frame.resize((desired_width, desired_height))) for frame in ImageSequence.Iterator(image1)]



frame_count = len(frames)
frame_index = 0

def update_frame():
    global frame_index
    frame_index += 1
    if frame_index >= frame_count:
        frame_index = 0
    label.config(image=frames[frame_index])
    root.after(100, update_frame)

root.after(0, update_frame)

def open_second_window():
    second_window = tk.Toplevel(root)
    second_window.title("Chessboard with Knight Movement")
    
    second_window.geometry(f"{width}x{height}")  # Set reduced size
    chessboard = [[None for _ in range(8)] for _ in range(8)]

    def on_click(row, col):
        for i in range(8):
            for j in range(8):
                if (abs(i - row) == 2 and abs(j - col) == 1) or (abs(i - row) == 1 and abs(j - col) == 2):
                    chessboard[i][j]["bg"] = "green"
                else:
                    chessboard[i][j]["bg"] = "white"

        output = tk.Toplevel(second_window)
        output.title("Output")
        output.geometry("200x200")

        def count_moves(row, col):
            count = 0
            for i in range(8):
                for j in range(8):
                    if (abs(i - row) == 2 and abs(j - col) == 1) or (abs(i - row) == 1 and abs(j - col) == 2):
                        count += 1
            return count

        label = tk.Label(output, text=f"The number of valid moves for the knight is {count_moves(row, col)}", font=("Arial", 5))
        label.pack()

    for row in range(8):
        for col in range(8):
            color = "white" if (row + col) % 2 == 0 else "black"
            chessboard[row][col] = tk.Button(second_window, width=5, height=2, bg=color)
            chessboard[row][col].grid(row=row, column=col)
            chessboard[row][col].configure(command=lambda row=row, col=col: on_click(row, col))

Title = Button(root, text="KNOWLEDGEABLE KNIGHTS", font=60)
Title.pack(padx=10, pady=10)
start_button = Button(root, text="Start", command=open_second_window, fg="white", bg="red", font=("Perpetua", 25))
start_button.pack()

root.mainloop()

def correct_move(x, y, n, visited):
    return 0 <= x < n and 0 <= y < n and visited[x][y] == -1

def next_moves(x, y, n, visited):
    moves = [(1, 2), (2, 1), (-1, 2), (2, -1), (-2, -1), (-1, -2), (1, -2), (-2, 1)]
    moves_list = []
    for a, b in moves:
        new_x, new_y = x + a, y + b
        if correct_move(new_x, new_y, n, visited):
            count = 0
            for next_a, next_b in moves:
                if correct_move(new_x + next_a, new_y + next_b, n, visited):
                    count += 1
            moves_list.append((new_x, new_y, count))
    moves_list.sort(key=lambda move: move[2])
    return moves_list

def possible_knight_tour(x, y, move_count, n, visited, canvas):
    visited[x][y] = move_count

    if canvas:
        draw_board(canvas, n, visited)
        canvas.update()
        canvas.after(500)

    if move_count == n * n:
        return True

    for new_x, new_y, _ in next_moves(x, y, n, visited):
        if correct_move(new_x, new_y, n, visited) and possible_knight_tour(new_x, new_y, move_count + 1, n, visited, canvas):
            return True

    visited[x][y] = -1

    if canvas:
        draw_board(canvas, n, visited)
        canvas.update()
        canvas.after(500)
        
    return False

    pygame.init()
    pygame.mixer.music.load("C:\\Users\\pvars\\OneDrive\\Desktop\\knightwalk (online-audio-converter.com).zip")
    pygame.mixer.music.play()

def knight_tour(n, start_x, start_y):
    visited = [[-1 for _ in range(n)] for _ in range(n)]
    move_count = 1
    root = tk.Tk()
    root.title("Knight's Tour")
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight()
    root.geometry("%dx%d" %(width,height))
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    if possible_knight_tour(start_x, start_y, move_count, n, visited, canvas):
        print("Solution found")
        draw_board(canvas, n, visited)
        canvas.update()
        messagebox.showinfo("Result", "Solution found")
    else:
        print("No solution")
        draw_board(canvas, n, visited)
        canvas.update()
        messagebox.showinfo("Result", "No solution")
    root.mainloop()

def draw_board(canvas, n, board):
    canvas.delete("all")
    cell_size = 70  
    for i in range(n):
        for j in range(n):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            color = "#7c4700" if (i + j) % 2 == 0 else "#997950"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)

            if board[i][j] != -1:
                canvas.create_text(x0 + cell_size / 2, y0 + cell_size / 2, text=str(board[i][j]), font=("Perpetua", 20))

    pygame.init()
    pygame.mixer.music.load("C:\\Users\\pvars\\OneDrive\\Desktop\\knightwalk (online-audio-converter.com)\\knightwalk (online-audio-converter.com).mp3")
    pygame.mixer.music.play()

def start(entry_n, entry_row, entry_col):
    try:
        n = int(entry_n.get())
        start_x = int(entry_row.get())
        start_y = int(entry_col.get())
        if n < 4 or start_x < 0 or start_y < 0 or start_x >= n or start_y >= n:
            raise ValueError
        knight_tour(n, start_x, start_y)
    except ValueError:
        messagebox.showerror("Error", "Invalid input")

def create_welcome_window():
    welcome_root = tk.Tk()
    welcome_root.title("Welcome to Knight's Tour")
    width=welcome_root.winfo_screenwidth()
    height=welcome_root.winfo_screenheight()
    welcome_root.geometry("%dx%d" %(width,height))
    pygame.init()
    pygame.mixer.music.load("C:\\Users\\pvars\\OneDrive\\Desktop\\knightwalk (online-audio-converter.com)\\knightwalk (online-audio-converter.com).mp3")

    pygame.mixer.music.play()

    image = tk.PhotoImage(file='C:\\Users\\pvars\\OneDrive\\Desktop\\knighttttt (1).ppm')  
    image_label = tk.Label(welcome_root, image=image, width=800, height=400, bg="#FFC0CB")
    image_label.pack()

    welcome_label = tk.Label(welcome_root, text="Welcome to Knight's Tour!", font=("Perpetua", 25, "bold"))
    welcome_label.pack(padx=5, pady=5)

    start_button = tk.Button(welcome_root, text="Start", command=lambda: open_main_window(welcome_root), font=("Perpetua", 20, "bold"), bg="#36F57F")
    start_button.pack(pady=1)

    welcome_root.mainloop()

def open_main_window(previous_window):
    previous_window.destroy()
    main_window = tk.Tk()
    main_window.title("Knight's Tour Input")
    width=main_window.winfo_screenwidth()
    height=main_window.winfo_screenheight()
    main_window.geometry("%dx%d" %(width,height))

    bg_image = tk.PhotoImage(file="C:\\Users\\pvars\\OneDrive\\Pictures\\knight56.png") 
    bg_label = tk.Label(main_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_n = tk.Label(main_window, text="Enter the board size (n):", font=("Perpetua", 25), fg="#E55451")
    label_n.grid(row=12, column=4, padx=50, pady=80)

    entry_n = tk.Entry(main_window, font=("Arial", 15))
    entry_n.grid(row=13, column=4, pady=5)

    label_row = tk.Label(main_window, text="Enter the starting row:", font=("Perpetua", 25), fg="#E55451")
    label_row.grid(row=16, column=4, pady=5)

    entry_row = tk.Entry(main_window, font=("Arial", 15))
    entry_row.grid(row=17, column=4, pady=5)

    label_col = tk.Label(main_window, text="Enter the starting column:", font=("Perpetua", 25), fg="#E55451")
    label_col.grid(row=20, column=4, pady=5)

    entry_col = tk.Entry(main_window, font=("Arial", 15))
    entry_col.grid(row=21, column=4, pady=5)

    start_button = tk.Button(main_window, text="Start", command=lambda: start(entry_n, entry_row, entry_col), font=("Perpetua", 20, "bold"), bg="#36F57F")
    start_button.grid(row=22, column=4, pady=5)

    main_window.mainloop()

create_welcome_window()


if _name_ == "_main_":
    create_welcome_window()
