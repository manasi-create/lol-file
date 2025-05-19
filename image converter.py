from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os

class LolConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG to LOL Converter")
        self.root.geometry("500x300")
        
        self.create_widgets()
        self.input_path = ""
        self.output_path = ""
        self.cropped = False

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Input file selection
        ttk.Label(main_frame, text="Select JPG File:").grid(row=0, column=0, sticky=W)
        self.input_entry = ttk.Entry(main_frame, width=40)
        self.input_entry.grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_input).grid(row=1, column=1, padx=5)

        # Output file selection
        ttk.Label(main_frame, text="Save LOL File To:").grid(row=2, column=0, sticky=W, pady=(15,0))
        self.output_entry = ttk.Entry(main_frame, width=40)
        self.output_entry.grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_output).grid(row=3, column=1, padx=5)

        # Conversion info
        self.info_label = ttk.Label(main_frame, text="", foreground="gray")
        self.info_label.grid(row=4, column=0, columnspan=2, pady=(10,0))

        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert to LOL", command=self.convert)
        self.convert_btn.grid(row=5, column=0, columnspan=2, pady=15)

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="gray")
        self.status_label.grid(row=6, column=0, columnspan=2)

    def select_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            self.input_path = file_path
            self.input_entry.delete(0, END)
            self.input_entry.insert(0, file_path)
            self.suggest_output_path()
            self.show_image_info(file_path)

    def show_image_info(self, file_path):
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                aspect = "1:1" if w == h else f"{w}:{h}"
                self.info_label.config(text=f"Original Size: {w}x{h} ({aspect})")
        except:
            self.info_label.config(text="")

    def select_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".lol",
            filetypes=[("LOL files", "*.lol")]
        )
        if file_path:
            self.output_path = file_path
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, file_path)

    def suggest_output_path(self):
        if self.input_path:
            base = os.path.splitext(os.path.basename(self.input_path))[0]
            dir_path = os.path.dirname(self.input_path)
            suggested_path = os.path.join(dir_path, f"{base}.lol")
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, suggested_path)
            self.output_path = suggested_path

    def convert(self):
        if not self.input_path or not self.output_path:
            messagebox.showerror("Error", "Please select both input and output paths")
            return

        try:
            self.cropped = False
            self.status_label.config(text="Converting...", foreground="black")
            self.convert_btn.config(state=DISABLED)
            self.root.update_idletasks()

            self.jpg_to_lol(self.input_path, self.output_path)

            msg = "Successfully converted"
            if self.cropped:
                msg += " (image was cropped to 1:1)"
            messagebox.showinfo("Success", msg)
            self.status_label.config(text="Ready", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Error occurred", foreground="red")
        finally:
            self.convert_btn.config(state=NORMAL)

    def jpg_to_lol(self, input_jpg_path, output_lol_path):
        try:
            with Image.open(input_jpg_path) as img:
                original_width, original_height = img.size
                
                # Crop to 1:1 if needed
                if original_width != original_height:
                    self.cropped = True
                    size = min(original_width, original_height)
                    left = (original_width - size) // 2
                    top = (original_height - size) // 2
                    right = left + size
                    bottom = top + size
                    img = img.crop((left, top, right, bottom))

                # Convert to RGB and process
                rgb_img = img.convert('RGB')
                hex_pixels = [f"{r:02x}{g:02x}{b:02x}" for r, g, b in rgb_img.getdata()]
                
                with open(output_lol_path, 'w') as lol_file:
                    lol_file.write('\n'.join(hex_pixels))

        except Exception as e:
            raise IOError(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = LolConverterApp(root)
    root.mainloop()