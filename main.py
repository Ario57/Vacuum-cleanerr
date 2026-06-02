import tkinter as tk
from tkinter import ttk

class VacuumSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Vacuum Cleaner Agent Simulation")
        self.root.geometry("700x450")
        self.root.configure(bg="#f0f2f5")

        # System State
        self.rooms = {'A': 'Dirty', 'B': 'Clean', 'C': 'Dirty'}
        self.agent_location = 'A'
        self.room_order = ['A', 'B', 'C']
        self.current_idx = 0
        self.is_running = False
        self.simulation_speed = 1000 # ms per action

        # UI Components Dictionaries
        self.room_frames = {}
        self.status_labels = {}
        self.agent_labels = {}

        # Build Interface
        self.create_header()
        self.create_room_interfaces()
        self.create_control_panel()
        self.update_ui_display()

    def create_header(self):
        header = tk.Label(
            self.root, 
            text="Intelligent Reflex Agent Simulation (Rooms A, B, C)", 
            font=("Helvetica", 16, "bold"), 
            bg="#f0f2f5", 
            fg="#1a73e8"
        )
        header.pack(pady=15)

    def create_room_interfaces(self):
        # Container for rooms
        rooms_container = tk.Frame(self.root, bg="#f0f2f5")
        rooms_container.pack(pady=10, fill=tk.X, expand=True)

        for room in self.room_order:
            # Main card frame for each room
            frame = tk.LabelFrame(
                rooms_container, 
                text=f" Room {room} ", 
                font=("Helvetica", 12, "bold"),
                bd=2, 
                relief=tk.GROOVE, 
                bg="#ffffff"
            )
            frame.pack(side=tk.LEFT, padx=20, pady=10, expand=True, fill=tk.BOTH)
            self.room_frames[room] = frame

            # Agent Presence indicator
            agent_lbl = tk.Label(frame, text="", font=("Helvetica", 24), bg="#ffffff")
            agent_lbl.pack(pady=5)
            self.agent_labels[room] = agent_lbl

            # Clean/Dirty Status Label
            status_lbl = tk.Label(frame, text="", font=("Helvetica", 11, "bold"), bg="#ffffff")
            status_lbl.pack(pady=5)
            self.status_labels[room] = status_lbl

            # User Interactive Controls to update state dynamically
            btn_frame = tk.Frame(frame, bg="#ffffff")
            btn_frame.pack(pady=10)

            dirty_btn = ttk.Button(btn_frame, text="Make Dirty", command=lambda r=room: self.set_room_status(r, 'Dirty'))
            dirty_btn.grid(row=0, column=0, padx=2)

            clean_btn = ttk.Button(btn_frame, text="Make Clean", command=lambda r=room: self.set_room_status(r, 'Clean'))
            clean_btn.grid(row=0, column=1, padx=2)

    def create_control_panel(self):
        control_frame = tk.Frame(self.root, bg="#f0f2f5")
        control_frame.pack(pady=20)

        self.start_btn = tk.Button(
            control_frame, 
            text="Start Agent Simulation", 
            font=("Helvetica", 11, "bold"),
            bg="#34a853", 
            fg="white", 
            padx=10, 
            pady=5,
            command=self.toggle_simulation
        )
        self.start_btn.grid(row=0, column=0, padx=10)

        # Status logger display
        self.log_label = tk.Label(
            self.root, 
            text="Status: Waiting for user to start...", 
            font=("Helvetica", 11, "italic"), 
            bg="#f0f2f5", 
            fg="#5f6368"
        )
        self.log_label.pack(pady=5)

    def set_room_status(self, room, status):
        self.rooms[room] = status
        self.update_ui_display()
        self.log_label.config(text=f"User manually updated Room {room} to {status}!")

    def update_ui_display(self):
        for room in self.room_order:
            status = self.rooms[room]
            
            # Update background color based on status
            if status == 'Dirty':
                self.room_frames[room].config(bg="#fce8e6") # Light red
                self.status_labels[room].config(text="STATUS: DIRTY", fg="#c5221f", bg="#fce8e6")
                self.room_frames[room].winfo_children()[2].config(bg="#fce8e6") # Frame wrapper inner fix
            else:
                self.room_frames[room].config(bg="#e6f4ea") # Light green
                self.status_labels[room].config(text="STATUS: CLEAN", fg="#137333", bg="#e6f4ea")
                self.room_frames[room].winfo_children()[2].config(bg="#e6f4ea")

            # Update Agent representation position
            if self.agent_location == room:
                self.agent_labels[room].config(text="🤖", bg=self.room_frames[room].cget("bg"))
                self.room_frames[room].config(bd=3, relief=tk.SOLID) # Highlight active frame
            else:
                self.agent_labels[room].config(text="", bg=self.room_frames[room].cget("bg"))
                self.room_frames[room].config(bd=2, relief=tk.GROOVE)

    def toggle_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text="Pause Simulation", bg="#ea4335")
            self.agent_step()
        else:
            self.is_running = False
            self.start_btn.config(text="Resume Simulation", bg="#34a853")

    def agent_step(self):
        if not self.is_running:
            return

        current_room = self.room_order[self.current_idx]
        self.agent_location = current_room
        self.update_ui_display()

        # Simple Agent Reflex Rules
        if self.rooms[current_room] == 'Dirty':
            # Action: Clean the room
            self.rooms[current_room] = 'Clean'
            self.log_label.config(text=f"Agent 🤖 found Room {current_room} DIRTY. Action: SUCKING DIRT...")
            self.update_ui_display()
            # Let the cleaning action occupy this step, move next time
            self.root.after(self.simulation_speed, self.agent_step)
        else:
            # Action: Room is clean, log and prepare transition to the next room interface
            self.log_label.config(text=f"Agent 🤖 found Room {current_room} CLEAN. Moving to next interface...")
            self.current_idx = (self.current_idx + 1) % len(self.room_order)
            
            # Schedule next movement execution step
            self.root.after(self.simulation_speed, self.agent_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumSimulation(root)
    root.mainloop()