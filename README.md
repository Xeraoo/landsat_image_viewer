# Landsat Image Viewer

A Python-based graphical user interface (GUI) application for processing and visualizing Landsat satellite images. This program allows users to open Landsat GeoTIFF files, visualize different band compositions, compute NDVI, and save processed images.

## Features  
- Open Landsat GeoTIFF images.  
- Display RGB and CIR band compositions.  
- Compute and visualize NDVI (Normalized Difference Vegetation Index).  
- Save processed images in PNG format.  
- Switch between light and dark themes for better usability.

---

## Installation  

Install required Python dependencies:  
```bash
pip install numpy rasterio pillow
```

## Usage
Run the application:
```bash
python landsat_viewer.py
```
## Open an image:
- Use the "File" menu to load a Landsat GeoTIFF image.

## Select visualization:
- **RGB Composition:** Visualize a three-band composition (default: Band 4, Band 3, Band 2).
- **CIR Composition:** Create a false-color CIR (Color Infrared) image (Bands: NIR, Red, Green).
- **NDVI:** Compute and display the Normalized Difference Vegetation Index.

## Save processed images:
- Use the **Save** button to save the current visualization as a PNG file.

## Switch theme:
- Toggle between Light and Dark mode using the "Theme" menu.

---

## GUI Overview

- **File Menu:**  
  - Open Landsat images.  
- **Theme Menu:**  
  - Toggle between Light and Dark mode.  
- **Control Panel:**  
  - Band selectors for RGB composition.  
  - Buttons for RGB, CIR, and NDVI visualizations.  
  - Save button for exporting images.  
- **Image Display Panel:**  
  - Displays the selected visualization (resized for convenience).

---

## Dependencies

The application requires the following Python libraries:  
- `tkinter` (standard Python GUI library)  
- `numpy` (numerical operations)  
- `rasterio` (geospatial raster data processing)  
- `Pillow` (image processing)  

---

## How It Works

### Load Image:
- Loads GeoTIFF files using `rasterio` and reads all available bands.

### Visualization:
- RGB and CIR compositions are created by stacking selected bands.  
- NDVI is calculated using the formula:  
  \[
  \text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}
  \]

### Rendering:
- Processed images are normalized, resized to fit the display, and shown in the GUI.

### Saving:
- Current visualizations are saved as PNG files using `Pillow`.

---

## Screenshots
![image](https://github.com/user-attachments/assets/46ca362d-342f-4507-a3c0-c2ff27553107)
![image](https://github.com/user-attachments/assets/d0555f07-dfda-42e2-b485-58b0720fdcde)
![image](https://github.com/user-attachments/assets/a081f62f-340f-466b-a815-55e97b6c96a0)

---

## Authors  
- Tymoteusz Maj  
- Bartosz Augustyn
- Hubert Dębowski
- Michał Walencik
- Kaushika Eluwawalage
