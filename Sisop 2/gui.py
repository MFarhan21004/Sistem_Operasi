#!/usr/bin/env python3
"""
Graphical User Interface untuk Sistem Manajemen File
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import os
from file_system import FileSystemSimulator

class FileSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File System Simulator")
        self.root.geometry("1000x700")
        
        self.fs = FileSystemSimulator()
        self.setup_ui()
        self.refresh_file_tree()
        
    def setup_ui(self):
        """Setup UI components"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for toolbar
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        ttk.Button(toolbar_frame, text="New Folder", command=self.new_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="New File", command=self.new_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Copy", command=self.copy_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Move", command=self.move_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Refresh", command=self.refresh_file_tree).pack(side=tk.LEFT, padx=(0, 5))
        
        # Current directory label
        self.current_dir_var = tk.StringVar(value=self.fs.current_directory)
        ttk.Label(toolbar_frame, text="Current Directory:").pack(side=tk.LEFT, padx=(20, 5))
        ttk.Label(toolbar_frame, textvariable=self.current_dir_var, font=("Courier", 9)).pack(side=tk.LEFT)
        
        # Paned window for split view
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for file tree
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # File tree
        ttk.Label(left_frame, text="File System Tree").pack(anchor=tk.W)
        
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        # Tree columns
        self.tree['columns'] = ('Type', 'Size', 'Modified', 'Path')
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('Type', width=80, minwidth=80)
        self.tree.column('Size', width=80, minwidth=80)
        self.tree.column('Modified', width=150, minwidth=150)
        self.tree.column('Path', width=0, minwidth=0)  # Hidden column for path storage
        
        self.tree.heading('#0', text='Name', anchor=tk.W)
        self.tree.heading('Type', text='Type', anchor=tk.W)
        self.tree.heading('Size', text='Size', anchor=tk.W)
        self.tree.heading('Modified', text='Modified', anchor=tk.W)
        
        # Tree events
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        self.tree.bind('<Button-3>', self.on_tree_right_click)
        
        # Right frame for details and operations
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        # Details section
        details_frame = ttk.LabelFrame(right_frame, text="Details")
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.details_text = ScrolledText(details_frame, height=8, width=40)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # System info section
        info_frame = ttk.LabelFrame(right_frame, text="System Information")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=4, width=40)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Command section
        cmd_frame = ttk.LabelFrame(right_frame, text="Command Line")
        cmd_frame.pack(fill=tk.BOTH, expand=True)
        
        self.command_text = ScrolledText(cmd_frame, height=10, width=40)
        self.command_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Command input
        cmd_input_frame = ttk.Frame(cmd_frame)
        cmd_input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        ttk.Label(cmd_input_frame, text="$").pack(side=tk.LEFT)
        self.command_entry = ttk.Entry(cmd_input_frame)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.command_entry.bind('<Return>', self.execute_command)
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.open_item)
        self.context_menu.add_command(label="New Folder", command=self.new_folder)
        self.context_menu.add_command(label="New File", command=self.new_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy", command=self.copy_item)
        self.context_menu.add_command(label="Move", command=self.move_item)
        self.context_menu.add_command(label="Delete", command=self.delete_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Properties", command=self.show_properties)
        
        # Update system info
        self.update_system_info()
    
    def get_selected_path(self):
        """Get currently selected path in tree"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        if len(values) >= 4:
            return values[3]  # Path is at index 3
        return None
    
    def refresh_file_tree(self):
        """Refresh the file tree display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add root
        self.add_tree_item('', '/', '/')
        
        # Update current directory
        self.current_dir_var.set(self.fs.current_directory)
        self.update_system_info()
    
    def add_tree_item(self, parent, path, name):
        """Add item to tree"""
        if not self.fs.path_exists(path):
            return
        
        file_info = self.fs.file_system[path]
        
        # Format size
        size_str = str(file_info['size']) if file_info['type'] == 'file' else '-'
        
        # Format modified date
        try:
            from datetime import datetime
            modified = datetime.fromisoformat(file_info['modified']).strftime('%Y-%m-%d %H:%M')
        except:
            modified = file_info['modified'][:16]
        
        # Insert item
        item_id = self.tree.insert(parent, 'end', text=name,
                                  values=(file_info['type'], size_str, modified, path))
        
        # Add children for directories
        if file_info['type'] == 'directory':
            for child_name, child_path in sorted(file_info['children'].items()):
                self.add_tree_item(item_id, child_path, child_name)
    
    def on_tree_double_click(self, event):
        """Handle tree double click"""
        self.open_item()
    
    def on_tree_right_click(self, event):
        """Handle tree right click"""
        # Select item under cursor
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def open_item(self):
        """Open selected item"""
        path = self.get_selected_path()
        if not path:
            return
        
        if self.fs.path_exists(path):
            file_info = self.fs.file_system[path]
            if file_info['type'] == 'directory':
                self.fs.cd(path)
                self.current_dir_var.set(self.fs.current_directory)
                self.show_details(path)
            else:
                self.show_details(path)
    
    def show_details(self, path):
        """Show details of selected item"""
        if not path or not self.fs.path_exists(path):
            return
        
        file_info = self.fs.file_system[path]
        
        details = f"Path: {path}\n"
        details += f"Type: {file_info['type']}\n"
        details += f"Size: {file_info['size']} bytes\n"
        details += f"Permissions: {file_info['permissions']}\n"
        details += f"Owner: {file_info['owner']}\n"
        details += f"Created: {file_info['created']}\n"
        details += f"Modified: {file_info['modified']}\n"
        
        if file_info['type'] == 'directory':
            details += f"Children: {len(file_info['children'])}\n"
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
    
    def new_folder(self):
        """Create new folder"""
        name = simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            if self.fs.mkdir(name):
                self.refresh_file_tree()
                self.log_command(f"mkdir {name}")
    
    def new_file(self):
        """Create new file"""
        name = simpledialog.askstring("New File", "Enter file name:")
        if name:
            if self.fs.touch(name):
                self.refresh_file_tree()
                self.log_command(f"touch {name}")
    
    def delete_item(self):
        """Delete selected item"""
        path = self.get_selected_path()
        if not path:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        if path == "/":
            messagebox.showerror("Error", "Cannot delete root directory")
            return
        
        name = self.fs.get_filename(path)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            if self.fs.rm(path, recursive=True):
                self.refresh_file_tree()
                self.log_command(f"rm -r {name}")
    
    def copy_item(self):
        """Copy selected item"""
        path = self.get_selected_path()
        if not path:
            messagebox.showwarning("Warning", "Please select an item to copy")
            return
        
        name = self.fs.get_filename(path)
        new_name = simpledialog.askstring("Copy", f"Copy '{name}' to:", initialvalue=f"{name}_copy")
        
        if new_name:
            if self.fs.cp(path, new_name):
                self.refresh_file_tree()
                self.log_command(f"cp {name} {new_name}")
    
    def move_item(self):
        """Move selected item"""
        path = self.get_selected_path()
        if not path:
            messagebox.showwarning("Warning", "Please select an item to move")
            return
        
        name = self.fs.get_filename(path)
        new_name = simpledialog.askstring("Move", f"Move '{name}' to:", initialvalue=name)
        
        if new_name:
            if self.fs.mv(path, new_name):
                self.refresh_file_tree()
                self.log_command(f"mv {name} {new_name}")
    
    def show_properties(self):
        """Show properties of selected item"""
        path = self.get_selected_path()
        if path:
            self.show_details(path)
    
    def update_system_info(self):
        """Update system information display"""
        info_text = f"Disk Size: {self.fs.disk_size} MB\n"
        info_text += f"Used Space: {self.fs.used_space // 1024 // 1024} MB\n"
        info_text += f"Free Space: {(self.fs.disk_size * 1024 * 1024 - self.fs.used_space) // 1024 // 1024} MB\n"
        info_text += f"Usage: {(self.fs.used_space / (self.fs.disk_size * 1024 * 1024) * 100):.1f}%"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
    
    def execute_command(self, event=None):
        """Execute command from command line"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        self.command_entry.delete(0, tk.END)
        self.log_command(command)
        
        # Simple command parsing
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0]
        args = parts[1:]
        
        try:
            if cmd == "ls":
                path = args[0] if args else None
                self.fs.ls(path)
            elif cmd == "cd":
                path = args[0] if args else "/"
                if self.fs.cd(path):
                    self.current_dir_var.set(self.fs.current_directory)
                    self.refresh_file_tree()
            elif cmd == "pwd":
                self.fs.pwd()
            elif cmd == "mkdir":
                for directory in args:
                    self.fs.mkdir(directory)
                self.refresh_file_tree()
            elif cmd == "touch":
                for file_path in args:
                    self.fs.touch(file_path)
                self.refresh_file_tree()
            elif cmd == "rm":
                for file_path in args:
                    self.fs.rm(file_path, recursive=True)
                self.refresh_file_tree()
            elif cmd == "df":
                self.fs.df()
                self.update_system_info()
            elif cmd == "find":
                name = args[0] if args else ""
                path = args[1] if len(args) > 1 else None
                self.fs.find(name, path)
            elif cmd == "clear":
                self.command_text.delete(1.0, tk.END)
            else:
                self.log_output(f"Unknown command: {cmd}")
        
        except Exception as e:
            self.log_output(f"Error: {e}")
    
    def log_command(self, command):
        """Log command to command text area"""
        self.command_text.insert(tk.END, f"$ {command}\n")
        self.command_text.see(tk.END)
    
    def log_output(self, output):
        """Log output to command text area"""
        self.command_text.insert(tk.END, f"{output}\n")
        self.command_text.see(tk.END)

def main():
    """Main function"""
    try:
        root = tk.Tk()
        app = FileSystemGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Please try CLI mode instead.")

if __name__ == "__main__":
    main()
