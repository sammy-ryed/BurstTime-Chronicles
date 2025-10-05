# BurstTime Chronicles

Welcome to **BurstTime Chronicles**, the place where you decide the fate of your digital workers, also known as *processes*.  
They arrive, they wait, they run, and sometimes, they suffer the wrath of your scheduling choices.  
Will you be a fair ruler or a tyrant of time? The CPU clock is ticking.

---

## The Algorithms

Every story needs its characters, and in BurstTime Chronicles, three mighty schedulers take the stage:

### **1. FCFS — The Gentle Giant**  
The "First Come, First Served" approach. It’s polite, orderly, and never cuts the line.  
If a process shows up first, it runs first. Simple, but sometimes too patient for its own good.

### **2. SJF — The Speed Enthusiast**  
The "Shortest Job First" algorithm. It adores efficiency and hates waiting.  
If you’re small and quick, you’ll be picked first. Longer jobs might just sulk in the queue.

### **3. Round Robin — The Fair Juggler**  
No favorites here. Everyone gets a turn, one time slice at a time.  
It keeps things fair, though a bit dizzying, imagine a spinning CPU trying to please everyone at once.

---

## Performance Scores

Every ruler must measure their reign. In BurstTime Chronicles, your success is judged by two scores:

### **Waiting Time (WT)**  
How long your poor processes stood in line before finally getting their moment to shine.  
The smaller this number, the happier your subjects.

### **Turnaround Time (TAT)**  
The grand total from the moment a process enters your kingdom to the moment it departs victorious.  
Lower is better here too, unless you enjoy watching the world burn slowly.

---

## Get it Running

Setting up your realm is easier than declaring sovereignty.

### **Prerequisites**
1. You’ll need **Python 3.x** installed.  
   (If you can run `python --version` in your terminal and see something starting with a 3, you’re good.)
2. You’ll also need **sv-ttk** for a sleek modern look. Install it using:

```
pip install sv-ttk
```
---

### **How to Begin the Chronicles**
1. Save the script as `bursttime_chronicles.py`
2. Open your terminal in the same folder.
3. Run the command:

```
python bursttime_chronicles.py
```
4. Watch your processes line up, battle for CPU glory, and learn who emerges victorious.

---

## The Verdict

BurstTime Chronicles isn’t just a simulator; it’s a courtroom, a racetrack, and a drama of milliseconds.  
Choose your scheduler wisely. Balance fairness with speed. And remember:  
every process deserves a little CPU time before the end of its tale.
