import tkinter as tk
from tkinter import messagebox
import itertools

base_resistors = [1.0, 1.5, 2.2, 3.3, 4.7, 5.6, 6.8, 8.2]

def generate_resistor_range(base_resistors, min_multiplier, max_multiplier):

    resistor_range = []
    for multiplier in range(min_multiplier, max_multiplier + 1):
        resistor_range.extend([r * (10 ** multiplier) for r in base_resistors])
    return resistor_range

def equivalent_resistance_series(resistors):

    return sum(resistors)

def equivalent_resistance_parallel(resistors):

    return 1 / sum(1 / r for r in resistors)

def find_closest_resistance(target, resistors, max_combination=3):

    closest_resistance = None
    closest_diff = float('inf')
    best_combo = None
    best_type = None
    min_resistor_count = float('inf')

    for n in range(1, max_combination + 1):
        for combo in itertools.combinations_with_replacement(resistors, n):
            series_resistance = equivalent_resistance_series(combo)
            series_diff = abs(series_resistance - target)

            if series_diff < closest_diff or (series_diff == closest_diff and n < min_resistor_count):
                closest_resistance = series_resistance
                closest_diff = series_diff
                best_combo = combo
                best_type = "Series"
                min_resistor_count = n

            parallel_resistance = equivalent_resistance_parallel(combo)
            parallel_diff = abs(parallel_resistance - target)
            if parallel_diff < closest_diff or (parallel_diff == closest_diff and n < min_resistor_count):
                closest_resistance = parallel_resistance
                closest_diff = parallel_diff
                best_combo = combo
                best_type = "Parallel"
                min_resistor_count = n

    return closest_resistance, best_combo, best_type

def on_calculate():
    try:

        target_resistance = float(entry_target_resistance.get())
        min_multiplier = int(entry_min_multiplier.get())
        max_multiplier = int(entry_max_multiplier.get())

        resistors = generate_resistor_range(base_resistors, min_multiplier, max_multiplier)

        closest_resistance, best_combo, best_type = find_closest_resistance(target_resistance, resistors)

        result_text = f"Closest Resistance: {closest_resistance:.2f}Ω ({best_type})\nResistor Values Used: {best_combo}"
        label_result.config(text=result_text)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")

root = tk.Tk()
root.title("Resistor Calculator")

label_target_resistance = tk.Label(root, text="Enter Target Resistance (in ohms):")
label_target_resistance.pack(pady=5)

entry_target_resistance = tk.Entry(root)
entry_target_resistance.pack(pady=5)

label_min_multiplier = tk.Label(root, text="Enter Minimum Multiplier Power (e.g., 0 for 1x):")
label_min_multiplier.pack(pady=5)

entry_min_multiplier = tk.Entry(root)
entry_min_multiplier.pack(pady=5)

label_max_multiplier = tk.Label(root, text="Enter Maximum Multiplier Power (e.g., 5 for 100,000x):")
label_max_multiplier.pack(pady=5)

entry_max_multiplier = tk.Entry(root)
entry_max_multiplier.pack(pady=5)

button_calculate = tk.Button(root, text="Calculate", command=on_calculate)
button_calculate.pack(pady=10)

label_result = tk.Label(root, text="", font=("Helvetica", 10), justify="left")
label_result.pack(pady=10)

root.mainloop()
