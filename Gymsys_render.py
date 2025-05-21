import threading
corner_label_id = None

class VisualSemaphore:
    def __init__(self, canvas, x, y, width=50, height=20, max_permits=1, machine_id=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_permits = max_permits
        self.machine_id = machine_id

        self.semaphore = threading.Semaphore(max_permits)  # Set initial semaphore value
        
        # Create rectangles for each permit
        self.rectangles = []
        self.circles = []  # List to hold the circles for active permits
        self.labels = []  # List to hold the labels for thread information

        for i in range(self.max_permits):
            rect = self.canvas.create_rectangle(self.x + (i * (self.width + 5)), self.y, 
                                                self.x + (i + 1) * (self.width + 5), self.y + self.height, 
                                                fill="green", tags="clear")  # Add "clear" tag here
            self.rectangles.append(rect)
            
            # Create a blue circle below each rectangle to represent the thread using the permit
            circle = self.canvas.create_oval(self.x + (i * (self.width + 5)) + self.width / 2 - 5,
                                             self.y + self.height + 5, 
                                             self.x + (i * (self.width + 5)) + self.width / 2 + 5, 
                                             self.y + self.height + 20, 
                                             fill="white", tags="clear")  # Add "clear" tag here
            self.circles.append(circle)

            # Label for the thread using the circle (initially no text)
            label = self.canvas.create_text(self.x + (i * (self.width + 5)) + self.width / 2, 
                                            self.y + self.height + 25, text="", fill="black", tags="clear")  # Add "clear" tag here
            self.labels.append(label)

        # Create a label for the machine at the top
        self.label = self.canvas.create_text(self.x + self.width * self.max_permits / 2, 
                                             self.y - 10, text=f"Máquina {self.machine_id} - {self.max_permits} unidade(s)", fill="black")


    def acquire(self, thread_id):
        if self.semaphore.acquire():  # Try to acquire
            for i in range(self.max_permits):
                # Check for an empty circle (white) and turn it blue (in use)
                if self.canvas.itemcget(self.circles[i], "fill") == "white":
                    self.canvas.itemconfig(self.circles[i], fill="blue")  # Change circle to blue
                    self.canvas.itemconfig(self.labels[i], text=f"Aluno {thread_id}")  # Add label with thread ID
                    # Only change the color of the acquired rectangle to red
                    self.canvas.itemconfig(self.rectangles[i], fill="red")  # Change color of the specific permit's rectangle to red
                    break
            return True
        return False


    def release(self):
        self.semaphore.release()  # Release the semaphore
        for i in range(self.max_permits):
            # Reset the circle to white when a thread is done
            if self.canvas.itemcget(self.circles[i], "fill") == "blue":
                self.canvas.itemconfig(self.circles[i], fill="white")  # Reset circle to white
                self.canvas.itemconfig(self.labels[i], text="")  # Remove thread label
                # Reset the corresponding rectangle to green
                self.canvas.itemconfig(self.rectangles[i], fill="green")  # Change rectangle back to green
                break


def update_canvas_size(maquinas, canvas):
    # Hard-code to have 4 machines per row
    max_columns = 4
    max_row_height = 0
    x_offset = 50
    y_offset = 100
    machines_per_row = 0
    max_row_width = 0
    num_rows = 0  # Track how many rows we need

    # Reset the positions and calculate rows
    for i, machine in enumerate(maquinas):
        if machines_per_row >= max_columns:
            # If a row exceeds max_columns, move to the next row
            x_offset = 50  # Reset x_offset for the new row
            y_offset += max_row_height + 75  # Move to the next row
            max_row_height = 0  # Reset max_row_height for the new row
            machines_per_row = 0  # Reset machine counter for the new row
            num_rows += 1  # Increment row count

        # Update the position of each machine in the grid
        machine.x = x_offset
        machine.y = y_offset

        # Adjust max_row_width and max_row_height
        max_row_width = max(max_row_width, x_offset + (machine.width * machine.max_permits + 10))
        max_row_height = max(max_row_height, machine.height)

        # Increment x_offset for next machine (increase space between machines)
        x_offset += (machine.width * machine.max_permits + 100)  # Increased horizontal spacing
        machines_per_row += 1

    # Increment row height to fit all rows
    num_rows += 1  # One more row for the last line of machines
    canvas.config(width=max_row_width + 100, height=(y_offset + max_row_height + 50))

    # Update the canvas with the new positions
    for machine in maquinas:
        for i, rect in enumerate(machine.rectangles):
            machine.canvas.coords(rect, machine.x + (i * (machine.width + 5)), machine.y, 
                                  machine.x + (i + 1) * (machine.width + 5), machine.y + machine.height)
        machine.canvas.coords(machine.label, machine.x + machine.width * machine.max_permits / 2, machine.y - 10)
        
        # Update circle positions based on rectangles
        for i, circle in enumerate(machine.circles):
            machine.canvas.coords(circle, 
                                  machine.x + (i * (machine.width + 5)) + machine.width / 2 - 5,
                                  machine.y + machine.height + 5, 
                                  machine.x + (i * (machine.width + 5)) + machine.width / 2 + 5, 
                                  machine.y + machine.height + 20)
            machine.canvas.coords(machine.labels[i], 
                                  machine.x + (i * (machine.width + 5)) + machine.width / 2, 
                                  machine.y + machine.height + 25)

def update_corner_label(canvas, variable_value):
    global corner_label_id
    if corner_label_id is None or not canvas.find_withtag("corner_label"):
        corner_label_id = canvas.create_text(10, 10, anchor="nw", text=f"Tempo de espera total: {variable_value}", fill="black", font=("Arial", 12), tags="corner_label")
    else:
        canvas.itemconfig(corner_label_id, text=f"Tempo de espera total: {variable_value}")