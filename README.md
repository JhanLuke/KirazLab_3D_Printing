
# 🖨️ 3D Printer Controller GUI

A Python-based graphical user interface (GUI) for controlling and calibrating a syringe-based 3D printer for aerogels. This tool supports direct G-code interaction, step-by-step movement, extrusion control, and calibration for precise material deposition.

We also provide CAD files for the modular syringe pump system, enabling easy fabrication and assembly of the extrusion hardware.

---

## ✅ Tested System

> ⚠️ This software was tested **only on**:
> - **Operating System**: Windows 11
> - **Printer**: Creality Ender 3 with a syringe-based extruder modification controlled via the extruder (stepper motor)

---

## 🧰 Requirements

- **Python** 3.7 or newer
- Python packages:
  ```bash
  pip install pyserial pillow
  ```

---

## ⚙️ Setup

1. **Download or clone** this repository.
2. **Edit paths and settings** in `GUI.py`:
   - Serial port:
     ```python
     SERIAL_PORT = "COM3"  # Or your printer's actual COM port
     ```

3. **Run the GUI**:
   ```bash
   python GUI.py
   ```

---

## 🧭 GUI Overview

### 🔌 Connection & Command Panel
- **Home Axis**: Sends `G28` to zero all axes.
- **Send G-code**: Allows custom G-code input.
- **Calibrate**: Opens the 2-step extrusion calibration window.

### ⚙️ Settings Panel
- Set extrusion mode: `M302 S0`, `M83`
- Adjust feed rate (`F`) and extruder steps (`E`)

### 💧 Extrusion Control
- Extrude and retract a specified volume
- Use `↑` and `↓` keys for quick extrusion commands

### 🧱 Manual Movement
- Move the print head on X, Y, and Z axes
- Input custom step size and move with directional buttons

---

## 🔧 Calibration Steps

1. Click **Calibrate**
2. Ensure ~10 mL of material is loaded
3. Enter current `E` steps (e.g., 100)
4. Click **Extrude 2 mL**
5. Measure actual volume extruded (e.g., 1.5 mL)
6. Input measured amount and calculate corrected `E` steps
7. Apply new `E` steps back in the main GUI

---

## 🛠 File Paths to Update

| Purpose        | Default Path                         | Suggested Action            |
|----------------|--------------------------------------|-----------------------------|
| Serial Port    | `"COM3"`                             | Set to your printer's port  |


---

## ⌨️ Keyboard Shortcuts

| Key        | Function     |
|------------|--------------|
| `Enter`    | Send command |
| `↑` Arrow  | Extrude      |
| `↓` Arrow  | Retract      |

---


## 🙌 Author

**Jhan Luke Okkabaz**  
For questions or contributions, please open a GitHub Issue or Pull Request.

---
