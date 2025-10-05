import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk


def fcfs(processes):
    processes.sort(key=lambda x: x[1])  # sort by arrival
    start = 0
    results = []
    for x in processes:
        start = max(start, x[1])
        start_time = start
        finish_time = start + x[2]
        waiting_time = start - x[1]
        turnaround_time = finish_time - x[1]
        start = finish_time
        results.append((x[0], waiting_time, turnaround_time))
    return results


def sjf(processes):
    n = len(processes)
    remaining = processes[:]
    time = 0
    done = 0
    results = []
    visited = [False] * n

    while done < n:
        available = [p for p in remaining if p[1] <= time and not visited[remaining.index(p)]]
        if not available:
            time += 1
            continue
        available.sort(key=lambda x: x[2])  # shortest job
        current = available[0]
        idx = remaining.index(current)
        visited[idx] = True
        start_time = time
        finish_time = time + current[2]
        waiting_time = start_time - current[1]
        turnaround_time = finish_time - current[1]
        results.append((current[0], waiting_time, turnaround_time))
        time = finish_time
        done += 1
    return results


def round_robin(processes, quantum):
    queue = []
    time = 0
    results = {}
    processes.sort(key=lambda x: x[1])
    remaining = {x[0]: x[2] for x in processes}
    i = 0
    while True:
        while i < len(processes) and processes[i][1] <= time:
            queue.append(processes[i])
            i += 1
        if not queue:
            if i < len(processes):
                time = processes[i][1]
                continue
            else:
                break
        current = queue.pop(0)
        pid, at, bt = current
        if remaining[pid] > quantum:
            remaining[pid] -= quantum
            time += quantum
            while i < len(processes) and processes[i][1] <= time:
                queue.append(processes[i])
                i += 1
            queue.append(current)
        else:
            time += remaining[pid]
            waiting_time = time - at - bt
            turnaround_time = time - at
            results[pid] = (waiting_time, turnaround_time)
            remaining[pid] = 0
    return [(pid, *results[pid]) for pid in results]


# ---------------- GUI Functions ---------------- #
def calculate():
    try:
        data = []
        for x in table.get_children():
            values = table.item(x)["values"]
            pid, arrival, burst = values
            data.append((pid, int(arrival), int(burst)))

        algo = algo_var.get()
        if algo == "FCFS":
            res = fcfs(data)
        elif algo == "SJF":
            res = sjf(data)
        elif algo == "Round Robin":
            try:
                q = int(q_entry.get())
                if q <= 0:
                    raise ValueError("Time quantum must be a positive integer.")
                res = round_robin(data, q)
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))
                return
        else:
            messagebox.showerror("Error", "Please select an algorithm!")
            return

        # Display results
        output.delete(*output.get_children())
        total_wait = 0
        total_tat = 0
        for pid, wt, tat in res:
            output.insert("", "end", values=(pid, wt, tat))
            total_wait += wt
            total_tat += tat
        avg_wait = round(total_wait / len(res), 2)
        avg_tat = round(total_tat / len(res), 2)
        avg_label.config(text=f"Average Waiting Time: {avg_wait} | Average Turnaround Time: {avg_tat}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_process():
    try:
        pid = pid_entry.get()
        arrival = int(at_entry.get())
        burst = int(bt_entry.get())
        if not pid or arrival < 0 or burst <= 0:
            raise ValueError("PID can't be empty, Arrival Time can't be negative, and Burst Time must be positive.")
        table.insert("", "end", values=(pid, arrival, burst))
        pid_entry.delete(0, tk.END)
        at_entry.delete(0, tk.END)
        bt_entry.delete(0, tk.END)
        pid_entry.focus()
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred.")


# ---------------- GUI Layout ---------------- #
root = tk.Tk()
root.title("CPU Scheduler Simulator")
root.geometry("800x600")

# Apply the theme
sv_ttk.set_theme("dark")

main_frame = ttk.Frame(root, padding="15")
main_frame.pack(fill="both", expand=True)

# Title
title_label = ttk.Label(main_frame, text="BurstTime Chronicles", font=("Helvetica", 20, "bold"), anchor="center")
title_label.pack(pady=(5, 20), fill="x")

# Process Input Frame
input_frame = ttk.LabelFrame(main_frame, text="Add a Process", padding="10")
input_frame.pack(fill="x", pady=(0, 10))

ttk.Label(input_frame, text="Process ID:").grid(row=0, column=0, padx=5, pady=5)
pid_entry = ttk.Entry(input_frame, width=15)
pid_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5, pady=5)
at_entry = ttk.Entry(input_frame, width=15)
at_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(input_frame, text="Burst Time:").grid(row=0, column=4, padx=5, pady=5)
bt_entry = ttk.Entry(input_frame, width=15)
bt_entry.grid(row=0, column=5, padx=5, pady=5)

ttk.Button(input_frame, text="➕ Add Process", command=add_process).grid(row=0, column=6, padx=10, pady=5)

# Process Table
table_frame = ttk.LabelFrame(main_frame, text="Process List", padding="10")
table_frame.pack(fill="both", expand=True, pady=(0, 10))

columns = ("PID", "Arrival", "Burst")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")
table.pack(fill="both", expand=True)

# Algorithm Selection Frame
algo_frame = ttk.LabelFrame(main_frame, text="Choose Algorithm", padding="10")
algo_frame.pack(fill="x", pady=(0, 10))

ttk.Label(algo_frame, text="Select Algorithm:").grid(row=0, column=0, padx=5, pady=5)
algo_var = tk.StringVar()
algo_menu = ttk.Combobox(algo_frame, textvariable=algo_var, values=["FCFS", "SJF", "Round Robin"], state="readonly")
algo_menu.grid(row=0, column=1, padx=5, pady=5)
algo_menu.set("FCFS")

ttk.Label(algo_frame, text="Time Quantum (RR):").grid(row=0, column=2, padx=5, pady=5)
q_entry = ttk.Entry(algo_frame, width=10)
q_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(algo_frame, text="🚀 Calculate", command=calculate).grid(row=0, column=4, padx=(20, 5), pady=5)

# Results Table
output_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
output_frame.pack(fill="both", expand=True)

output = ttk.Treeview(output_frame, columns=("PID", "Waiting Time", "Turnaround Time"), show="headings")
for col in ("PID", "Waiting Time", "Turnaround Time"):
    output.heading(col, text=col)
    output.column(col, anchor="center")
output.pack(fill="both", expand=True)

# Average Time Label
avg_label = ttk.Label(main_frame, text="", font=("Helvetica", 12, "bold"), anchor="center")
avg_label.pack(pady=(10, 0), fill="x")

# Set initial focus
pid_entry.focus()

root.mainloop()