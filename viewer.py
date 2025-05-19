from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import math

def open_lol_file(file_path):
    try:
        with open(file_path, 'r') as f:
            hex_data = f.read().splitlines()
        
        # Calculate image dimensions
        num_pixels = len(hex_data)
        side_length = int(math.sqrt(num_pixels))
        
        if side_length * side_length != num_pixels:
            raise ValueError("Not a perfect square image - possibly corrupt file")
        
        # Convert hex to RGB values
        rgb_pixels = []
        for hex_code in hex_data:
            if len(hex_code) != 6:
                raise ValueError(f"Invalid hex code: {hex_code}")
            rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
            rgb_pixels.append(rgb)
        
        # Create image
        img = Image.new('RGB', (side_length, side_length))
        img.putdata(rgb_pixels)
        return img
    
    except Exception as e:
        raise ValueError(f"Error reading LOL file: {str(e)}")

def show_lol_viewer():
    root = tk.Tk()
    root.title("LOL File Viewer")
    root.geometry("400x200")
    
    def open_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("LOL files", "*.lol")],
            title="Select LOL File"
        )
        if not file_path:
            return
        
        try:
            img = open_lol_file(file_path)
            img.show()
            status_label.config(text=f"Displaying {img.size[0]}x{img.size[1]} image", fg="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Error loading file", fg="red")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill=tk.BOTH)
    
    tk.Label(frame, text="LOL File Viewer", font=("Arial", 14)).pack(pady=10)
    open_btn = tk.Button(frame, text="Open LOL File", command=open_file)
    open_btn.pack(pady=10)
    
    status_label = tk.Label(frame, text="", fg="gray")
    status_label.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    show_lol_viewer()