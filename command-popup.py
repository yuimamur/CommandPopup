import tkinter as tk
import subprocess
import os

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result.stdout.decode('utf-8'))
        output_text.insert(tk.END, result.stderr.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error: {e.stderr.decode('utf-8')}")

def find_other_exe_files():
    exe_files = []
    current_exe = os.path.basename(__file__)
    for file in os.listdir('.'):
        if file.endswith('.exe') and file != current_exe:
            exe_files.append(file)
    return exe_files

def on_button_click(button_name):
    # コンソールに押されたボタンを出力
    print(f"Button {button_name} pressed!")

    try:
        with open("input.txt", "r") as file:
            file_content = file.readlines()
            value = None
            for line in file_content:
                if line.startswith(f"{button_name}:"):
                    value = line.strip().split(":")[1].strip()
                    break
            if value:
                exe_files = find_other_exe_files()
                if exe_files:
                    exe_files[0] = "ls"
                    #command = f"{exe_files[0]} 'Button {button_name} pressed! Content: {value}'"
                    command = f"{exe_files[0]} {value}"
                else:
                    command = f"echo 'No other exe files found. Button {button_name} pressed! Content: {value}'"
                run_command(command)
            else:
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, f"Error: Value for {button_name} not found.")
    except FileNotFoundError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Error: 'input.txt' not found.")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("Simple Command Runner")

frame = tk.Frame(root)
frame.pack(pady=20)

button_a = tk.Button(frame, text="Button A", command=lambda: on_button_click("A"))
button_a.grid(row=0, column=0, padx=10)

button_b = tk.Button(frame, text="Button B", command=lambda: on_button_click("B"))
button_b.grid(row=0, column=1, padx=10)

button_c = tk.Button(frame, text="Button C", command=lambda: on_button_click("C"))
button_c.grid(row=0, column=2, padx=10)

output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=20)

root.mainloop()
