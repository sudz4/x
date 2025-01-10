import tkinter as tk
from PIL import Image, ImageTk
import itertools

def play_gif(gif_path):
    # Create the main window
    root = tk.Tk()
    root.title("GIF Player")

    # Load the GIF using PIL
    gif = Image.open(gif_path)

    # Create a label to display the GIF
    label = tk.Label(root)
    label.pack()

    # Get the frames of the GIF
    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(gif.copy())
            frames.append(frame)
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # End of GIF frames

    # Function to update the displayed frame
    def update_frame(index):
        frame = frames[index]
        label.configure(image=frame)
        index = (index + 1) % len(frames)  # Loop to the start
        root.after(gif.info.get("duration", 100), update_frame, index)

    # Start playing the GIF
    update_frame(0)

    # Run the main event loop
    root.mainloop()

# Provide the path to your GIF
play_gif("/Users/sudz4/Desktop/X/x/kb_knowledge_base/baby_pizza_chefs.gif")
