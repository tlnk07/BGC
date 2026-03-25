# ✂️ Background Cut (BGC)

A powerful, dark‑themed desktop tool to remove image backgrounds in one click.



## ✨ Features



### ✂️ Precision Background Removal

- **AI‑powered segmentation** – Uses the rembg engine (U²‑Net) to accurately detect the main subject and create a high‑quality alpha mask.

- **Real‑time preview** – See original and result side by side, with automatic scaling to fit the view.

- **Multiple input formats** – Supports JPG, JPEG, PNG, BMP, TIFF (any format Pillow can read).

### 🎨 Modern User Experience

- **Dark theme** – A sleek, eye‑friendly interface that follows your system appearance (light/dark).

- **Thread‑safe processing** – Background removal runs in a separate thread, keeping the UI responsive and smooth.

- **Instant feedback** – Status bar, loading indicator, and clear error messages guide you through the workflow.

### 💾 Export & Compatibility

- **Transparent PNG** – Result images preserve alpha transparency, perfect for graphic design or further editing.

- **One‑click save** – Choose destination and filename with a standard file dialog.


## 📦 Requirements

- Python 3.8+
- CustomTkinter – For the modern UI components.
- Pillow – Image loading, display, and saving
- rembg – AI background removal engine (includes onnxruntime and deep learning models)



## 🔧 Installation

- Clone or download this repository.

- Install the required packages using pip:

```bash

pip install -r requirements.txt

```

- Run the application:

```bash

python main.py

```



Viết readme như này cho background_cut
