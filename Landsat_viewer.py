import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
import rasterio


def open_landsat_image():
    file_path = filedialog.askopenfilename(
        title="Select a Landsat Image",
        filetypes=(("GeoTIFF Files", "*.tif"), ("All Files", "*.*"))
    )
    if not file_path:
        return

    try:
        with rasterio.open(file_path) as src:
            bands = src.read()
            band_labels = [f"Band {i}" for i in range(1, bands.shape[0] + 1)]
            image_data['bands'] = bands
            image_data['path'] = file_path

        # Default RGB composition (R: Band 4, G: Band 3, B: Band 2)
        r_band_selector.set("Band 4")
        g_band_selector.set("Band 3")
        b_band_selector.set("Band 2")
        show_rgb_composition()

        # Update RGB band selectors
        r_band_selector['values'] = band_labels
        g_band_selector['values'] = band_labels
        b_band_selector['values'] = band_labels

        toggle_buttons(state="normal")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the file:\n{e}")


def toggle_buttons(state):
    rgb_button.config(state=state)
    manual_button.config(state=state)
    ndvi_button.config(state=state)
    cir_button.config(state=state)
    save_button.config(state=state)


def show_rgb_composition():
    if 'bands' not in image_data:
        messagebox.showerror("Error", "No data loaded.")
        return

    try:
        r_band = image_data['bands'][int(r_band_selector.get().split()[1]) - 1]
        g_band = image_data['bands'][int(g_band_selector.get().split()[1]) - 1]
        b_band = image_data['bands'][int(b_band_selector.get().split()[1]) - 1]

        rgb_image = np.stack([r_band, g_band, b_band], axis=-1)
        rgb_image = (rgb_image / rgb_image.max() * 255).astype(np.uint8)
        image_data['current_image'] = rgb_image

        render_image(rgb_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate RGB image:\n{e}")


def show_ndvi():
    if 'bands' not in image_data:
        messagebox.showerror("Error", "No data loaded.")
        return

    try:
        nir = image_data['bands'][5 - 1]
        red = image_data['bands'][4 - 1]

        ndvi = (nir - red) / (nir + red + 1e-10)
        ndvi_normalized = ((ndvi + 1) / 2 * 255).astype(np.uint8)
        image_data['current_image'] = ndvi_normalized

        render_image(ndvi_normalized, gray=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate NDVI:\n{e}")


def show_cir():
    if 'bands' not in image_data:
        messagebox.showerror("Error", "No data loaded.")
        return

    try:
        nir = image_data['bands'][5 - 1]
        red = image_data['bands'][4 - 1]
        green = image_data['bands'][3 - 1]

        cir_image = np.stack([nir, red, green], axis=-1)
        cir_image = (cir_image / cir_image.max() * 255).astype(np.uint8)
        image_data['current_image'] = cir_image

        render_image(cir_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate CIR:\n{e}")


def save_image():
    if 'current_image' not in image_data:
        messagebox.showerror("Error", "No image to save.")
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Image",
        defaultextension=".png",
        filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
    )
    if not file_path:
        return

    try:
        image = Image.fromarray(image_data['current_image'])
        image.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image:\n{e}")


def show_welcome_message():
    messagebox.showinfo(
        "About the Program",
        "A program for processing and visualizing Landsat satellite images.\n\n"
        "Features:\n"
        "- Display RGB and CIR compositions\n"
        "- Calculate NDVI\n"
        "- Save processed images"
    )


def render_image(image, gray=False):
    mode = "L" if gray else None
    image = Image.fromarray(image, mode=mode)
    image = image.resize((512, 512), Image.Resampling.LANCZOS)
    img_display = ImageTk.PhotoImage(image)
    image_panel.config(image=img_display)
    image_panel.image = img_display


def switch_theme():
    global dark_mode
    dark_mode = not dark_mode
    style.theme_use("clam" if dark_mode else "default")
    root.configure(bg="gray20" if dark_mode else "SystemButtonFace")
    theme_menu.entryconfig(0, label="Light Mode" if dark_mode else "Dark Mode")


# Global data
image_data = {}
dark_mode = False

# Main window
root = tk.Tk()
root.title("Landsat Viewer")
root.geometry("800x600")

style = ttk.Style(root)

# Welcome message
root.after(100, show_welcome_message)

# Menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open Image", command=open_landsat_image)
menu_bar.add_cascade(label="File", menu=file_menu)

theme_menu = tk.Menu(menu_bar, tearoff=0)
theme_menu.add_command(label="Dark Mode", command=switch_theme)
menu_bar.add_cascade(label="Theme", menu=theme_menu)

root.config(menu=menu_bar)

# Image display panel
image_panel = tk.Label(root)
image_panel.pack(pady=10)

# Band selection and buttons in one row
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

r_label = tk.Label(control_frame, text="R:")
r_label.grid(row=0, column=0)
r_band_selector = ttk.Combobox(control_frame, state="readonly", width=10)
r_band_selector.grid(row=0, column=1)

g_label = tk.Label(control_frame, text="G:")
g_label.grid(row=0, column=2)
g_band_selector = ttk.Combobox(control_frame, state="readonly", width=10)
g_band_selector.grid(row=0, column=3)

b_label = tk.Label(control_frame, text="B:")
b_label.grid(row=0, column=4)
b_band_selector = ttk.Combobox(control_frame, state="readonly", width=10)
b_band_selector.grid(row=0, column=5)

rgb_button = tk.Button(control_frame, text="RGB", command=show_rgb_composition, state="disabled")
rgb_button.grid(row=0, column=6, padx=5)

manual_button = tk.Button(control_frame, text="Composition", command=show_rgb_composition, state="disabled")
manual_button.grid(row=0, column=7, padx=5)

ndvi_button = tk.Button(control_frame, text="NDVI", command=show_ndvi, state="disabled")
ndvi_button.grid(row=0, column=8, padx=5)

cir_button = tk.Button(control_frame, text="CIR", command=show_cir, state="disabled")
cir_button.grid(row=0, column=9, padx=5)

save_button = tk.Button(control_frame, text="Save", command=save_image, state="disabled")
save_button.grid(row=0, column=10, padx=5)

root.mainloop()
