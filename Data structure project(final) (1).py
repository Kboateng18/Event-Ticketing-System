import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time
import re
import uuid

class TicketSystemValidator:
    @staticmethod
    def validate_name(name):
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long."
        name = name.strip()
        if not re.match(r'^[A-Za-z]+(?:\s[A-Za-z]+)*$', name):
            return False, "Name can only contain letters and single spaces between words."
        if '  ' in name:
            return False, "Name cannot contain consecutive spaces."
        return True, name

class TicketSystemApp:
    def __init__(self, master):
        self.master = master
        master.title("Event Ticketing System")
        master.geometry("700x600")
        
        # Define a vibrant color palette
        self.colors = {
            'background': '#D2B48C',  # Brown color for background
            'primary': '#4A90E2',      # Bright blue for main elements
            'secondary': '#50E3C2',    # Teal for accents
            'highlight': '#FF6B6B',    # Coral red for important buttons
            'text': '#2C3E50'          # Dark blue-gray for text
        }

        # Configure master window
        master.configure(bg=self.colors['background'])

        # System variables
        self.vip_tickets = 10
        self.regular_tickets = 15
        self.vip_queue = []
        self.regular_queue = []
        self.transaction_log = []
        self.transaction_details = {}

        # Create main frame with new styling
        self.main_frame = tk.Frame(master, bg=self.colors['background'])
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create and display buttons
        self.create_buttons()

        # Create transaction log view
        self.create_transaction_log()

        # Create ticket status display
        self.create_ticket_status()

    def create_ticket_status(self):
        """Create a frame to display current ticket status with new styling"""
        status_frame = tk.Frame(self.main_frame, 
                                relief=tk.RIDGE, 
                                borderwidth=2, 
                                bg=self.colors['background'])
        status_frame.pack(fill=tk.X, pady=10)

        # VIP Tickets
        self.vip_label = tk.Label(status_frame, 
                                  text=f"VIP Tickets: {self.vip_tickets}", 
                                  font=("Helvetica", 10, "bold"),
                                  fg=self.colors['text'],
                                  bg=self.colors['background'])
        self.vip_label.pack(side=tk.LEFT, padx=10)

        # Regular Tickets
        self.regular_label = tk.Label(status_frame, 
                                      text=f"Regular Tickets: {self.regular_tickets}", 
                                      font=("Helvetica", 10, "bold"),
                                      fg=self.colors['text'],
                                      bg=self.colors['background'])
        self.regular_label.pack(side=tk.LEFT, padx=10)

    def update_ticket_status(self):
        """Update ticket status labels"""
        self.vip_label.config(text=f"VIP Tickets: {self.vip_tickets}")
        self.regular_label.config(text=f"Regular Tickets: {self.regular_tickets}")

    def create_buttons(self):
        """Create main menu buttons with vibrant colors"""
        button_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=10)

        buttons = [
            ("Register Ticket", self.register_user, self.colors['primary']),
            ("Process Next Ticket", self.process_next_ticket, self.colors['secondary']),
            ("Cancel Registered Ticket", self.cancel_ticket_request, self.colors['highlight']),
            ("Exit", self.exit_application, '#E74C3C')  # Bright red for exit
        ]

        for text, command, color in buttons:
            btn = tk.Button(button_frame, 
                            text=text, 
                            width=20, 
                            command=command,
                            bg=color,
                            fg='white',
                            font=("Helvetica", 10, "bold"),
                            activebackground=color,
                            activeforeground='white',
                            relief=tk.RAISED,
                            borderwidth=3)
            btn.pack(side=tk.LEFT, padx=5, expand=True)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.darken_color(e.widget['bg'])))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=e.widget['bg']))

    def darken_color(self, hex_color, amount=0.2):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, int(c * (1 - amount))) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)

    def exit_application(self):
        """Confirm and exit the application"""
        # Prompt for confirmation before closing
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the Event Ticketing System?"):
            self.master.destroy()  # Changed from quit() to destroy()

    def create_transaction_log(self):
        """Create transaction log treeview with new styling"""
        # Transaction Log Label
        log_label = tk.Label(self.main_frame, 
                             text="Transaction Log", 
                             font=("Helvetica", 12, "bold"),
                             fg=self.colors['text'],
                             bg=self.colors['background'])
        log_label.pack(pady=(10, 5))

        # Treeview for transaction log
        columns = ("Transaction ID", "Name", "Ticket Type", "Status", "Timestamp")
        style = ttk.Style()
        
        # Configure treeview style
        style.theme_use('clam')  # Use clam theme for more modern look
        style.configure("Ticket.Treeview", 
                        background=self.colors['background'],
                        foreground=self.colors['text'],
                        rowheight=25,
                        fieldbackground=self.colors['background'])
        style.map('Ticket.Treeview', 
                  background=[('selected', self.colors['primary'])],
                  foreground=[('selected', 'white')])

        self.log_tree = ttk.Treeview(self.main_frame, 
                                     columns=columns, 
                                     show="headings", 
                                     style="Ticket.Treeview")
        
        # Define headings
        for col in columns:
            self.log_tree.heading(col, text=col, anchor=tk.CENTER)
            self.log_tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.log_tree.yview)
        self.log_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def register_user(self):
        """Open registration dialog"""
        # Create a top-level window for registration
        reg_window = tk.Toplevel(self.master)
        reg_window.title("Ticket Registration")
        reg_window.geometry("400x400")
        reg_window.configure(bg=self.colors['background'])

        # First Name
        tk.Label(reg_window, text="First Name:", 
                 bg=self.colors['background'], 
                 fg=self.colors['text']).pack(pady=(10, 0))
        first_name_entry = tk.Entry(reg_window, width=30)
        first_name_entry.pack(pady=(0, 10))

        # Last Name
        tk.Label(reg_window, text="Last Name:", 
                 bg=self.colors['background'], 
                 fg=self.colors['text']).pack(pady=(10, 0))
        last_name_entry = tk.Entry(reg_window, width=30)
        last_name_entry.pack(pady=(0, 10))

        # Ticket Type
        tk.Label(reg_window, text="Ticket Type:", 
                 bg=self.colors['background'], 
                 fg=self.colors['text']).pack(pady=(10, 0))
        ticket_type_var = tk.StringVar(value="Regular")
        ticket_type_combo = ttk.Combobox(reg_window, textvariable=ticket_type_var, 
                                         values=["VIP", "Regular"], state="readonly")
        ticket_type_combo.pack(pady=(0, 10))

        # Ticket Quantity
        tk.Label(reg_window, text="Number of Tickets:", 
                 bg=self.colors['background'], 
                 fg=self.colors['text']).pack(pady=(10, 0))
        ticket_quantity_var = tk.StringVar(value="1")
        ticket_quantity_combo = ttk.Combobox(reg_window, 
                                             textvariable=ticket_quantity_var, 
                                             values=[str(i) for i in range(1, 6)], 
                                             state="readonly")
        ticket_quantity_combo.pack(pady=(0, 10))

        def submit_registration():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            ticket_type = ticket_type_var.get()
            ticket_quantity = int(ticket_quantity_var.get())

            # Validate names
            first_name_valid = TicketSystemValidator.validate_name(first_name)
            last_name_valid = TicketSystemValidator.validate_name(last_name)

            if not first_name_valid[0]:
                messagebox.showerror("Error", first_name_valid[1])
                return
            
            if not last_name_valid[0]:
                messagebox.showerror("Error", last_name_valid[1])
                return

            full_name = f"{first_name_valid[1]} {last_name_valid[1]}"

            # Check ticket availability
            if ticket_type == "VIP" and ticket_quantity > self.vip_tickets:
                messagebox.showerror("Error", f"Only {self.vip_tickets} VIP tickets available.")
                return
            
            if ticket_type == "Regular" and ticket_quantity > self.regular_tickets:
                messagebox.showerror("Error", f"Only {self.regular_tickets} Regular tickets available.")
                return

            # Register multiple tickets with unique transaction IDs
            for _ in range(ticket_quantity):
                # Generate transaction ID
                transaction_id = str(uuid.uuid4())[:8]

                # Update queues and ticket counts
                if ticket_type == "VIP":
                    self.vip_queue.append(full_name)
                    self.vip_tickets -= 1
                else:
                    self.regular_queue.append(full_name)
                    self.regular_tickets -= 1

                # Create transaction details
                transaction_details = {
                    "transaction_id": transaction_id,
                    "name": full_name,
                    "ticket_type": ticket_type,
                    "status": "Registered",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                # Add to transaction log
                self.transaction_log.append(transaction_details)
                self.transaction_details[transaction_id] = transaction_details

                # Update transaction log view
                self.log_tree.insert("", tk.END, values=(
                    transaction_id, 
                    full_name, 
                    ticket_type, 
                    "Registered", 
                    transaction_details["timestamp"]
                ))

            # Save to transaction log text file
            self.save_transaction_log()

            # Update ticket status display
            self.update_ticket_status()

            messagebox.showinfo("Success", f"{ticket_quantity} {ticket_type} ticket(s) registered successfully!")
            reg_window.destroy()

        # Submit Button
        submit_btn = tk.Button(reg_window, 
                               text="Submit", 
                               command=submit_registration,
                               bg=self.colors['primary'],
                               fg='white',
                               font=("Helvetica", 10, "bold"))
        submit_btn.pack(pady=10)

    def process_next_ticket(self):
        """Process the next ticket in queue"""
        if self.vip_queue:
            next_person = self.vip_queue.pop(0)
            ticket_type = "VIP"
        elif self.regular_queue:
            next_person = self.regular_queue.pop(0)
            ticket_type = "Regular"
        else:
            messagebox.showinfo("Information", "No tickets to process.")
            return

        # Update transaction log status
        for transaction in self.transaction_log:
            if transaction['name'] == next_person and transaction['ticket_type'] == ticket_type:
                transaction['status'] = 'Processed'
                break

        # Update treeview
        for item in self.log_tree.get_children():
            if self.log_tree.item(item)['values'][1] == next_person:
                values = list(self.log_tree.item(item)['values'])
                values[3] = 'Processed'
                self.log_tree.item(item, values=values)
                break

        # Save to transaction log text file
        self.save_transaction_log()

        messagebox.showinfo("Ticket Processed", f"Processing {ticket_type} ticket for: {next_person}")

    def cancel_ticket_request(self):
        """Cancel a registered ticket"""
        # Find registered tickets
        registered_tickets = [t for t in self.transaction_log if t['status'] == 'Registered']
        
        if not registered_tickets:
            messagebox.showinfo("Cancel Ticket", "No registered tickets available to cancel.")
            return
        
        # Create cancellation dialog
        cancel_window = tk.Toplevel(self.master)
        cancel_window.title("Cancel Ticket")
        cancel_window.geometry("500x400")
        cancel_window.configure(bg=self.colors['background'])
        
        # Label
        tk.Label(cancel_window, 
                 text="Select Ticket to Cancel", 
                 font=("Helvetica", 12, "bold"),
                 bg=self.colors['background'],
                 fg=self.colors['text']).pack(pady=10)
        
        # Treeview to show registered tickets
        columns = ("Name", "Ticket Type", "Transaction ID", "Timestamp")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Cancel.Treeview", 
                        background=self.colors['background'],
                        foreground=self.colors['text'],
                        rowheight=25,
                        fieldbackground=self.colors['background'])
        style.map('Cancel.Treeview', 
                  background=[('selected', self.colors['primary'])],
                  foreground=[('selected', 'white')])

        cancel_tree = ttk.Treeview(cancel_window, 
                                   columns=columns, 
                                   show="headings", 
                                   style="Cancel.Treeview")
        
        # Define headings
        for col in columns:
            cancel_tree.heading(col, text=col, anchor=tk.CENTER)
            cancel_tree.column(col, width=100, anchor=tk.CENTER)
        
        # Populate treeview with registered tickets
        for ticket in registered_tickets:
            cancel_tree.insert("", tk.END, values=(
                ticket['name'], 
                ticket['ticket_type'], 
                ticket['transaction_id'], 
                ticket['timestamp']
            ))
        
        cancel_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        def confirm_cancellation():
            selected_item = cancel_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a ticket to cancel.")
                return
            
            # Get ticket details
            values = cancel_tree.item(selected_item[0])['values']
            full_name = values[0]
            ticket_type = values[1]
            transaction_id = values[2]
            
            # Find the matching transaction
            transaction = next((t for t in self.transaction_log if t['transaction_id'] == transaction_id), None)
            
            if not transaction:
                messagebox.showerror("Error", "Ticket not found.")
                return
            
            # Confirm cancellation
            confirm = messagebox.askyesno("Confirm Cancellation", 
                                          f"Are you sure you want to cancel the ticket for {full_name}?")
            if not confirm:
                return
            
            # Update transaction status
            transaction['status'] = 'Cancelled'
            transaction['cancel_timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Restore ticket and remove from queue
            if ticket_type == "VIP":
                if full_name in self.vip_queue:
                    self.vip_queue.remove(full_name)
                    self.vip_tickets += 1
            else:
                if full_name in self.regular_queue:
                    self.regular_queue.remove(full_name)
                    self.regular_tickets += 1
            
            # Update treeview
            for item in self.log_tree.get_children():
                if self.log_tree.item(item)['values'][0] == transaction_id:
                    values = list(self.log_tree.item(item)['values'])
                    values[3] = 'Cancelled'
                    self.log_tree.item(item, values=values)
                    break
            
            # Save updated transaction log
            self.save_transaction_log()
            
            # Update ticket status display
            self.update_ticket_status()
            
            messagebox.showinfo("Success", f"Ticket for {full_name} has been cancelled.")
            cancel_window.destroy()
        
        # Cancel Button
        cancel_btn = tk.Button(cancel_window, text="Cancel Selected Ticket", command=confirm_cancellation)
        cancel_btn.pack(pady=10)

    def save_transaction_log(self):
        """Save transaction log to a text file"""
        with open("transaction_log.txt", "w") as file:
            file.write("Transaction ID".ljust(15) + "\t Name".ljust(20) + "Ticket Type".ljust(15) + 
              "Status".ljust(15) + "Timestamp".ljust(20) + "\t Cancel Timestamp\n")
            file.write("-" * 120+"\n")
            for transaction in self.transaction_log:
                # Add optional cancel_timestamp if it exists
                cancel_timestamp = transaction.get('cancel_timestamp', '')
                file.write(f"{transaction['transaction_id']}\t|| {transaction['name']}\t|| "
                           f"{transaction['ticket_type']}\t|| {transaction['status']}\t|| "
                           f"{transaction['timestamp']}\t|| {cancel_timestamp}\n")

# Main loop
root = tk.Tk()
app = TicketSystemApp(root)
root.mainloop()
