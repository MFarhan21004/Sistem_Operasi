#!/usr/bin/env python3
"""
Command Line Interface untuk Sistem Manajemen File
"""

import sys
import shlex
from file_system import FileSystemSimulator

class FileSystemCLI:
    def __init__(self):
        self.fs = FileSystemSimulator()
        self.running = True
        
    def get_prompt(self) -> str:
        """Dapatkan prompt untuk CLI"""
        return f"simfs:{self.fs.current_directory}$ "
    
    def parse_command(self, command_line: str) -> tuple:
        """Parse command line input"""
        try:
            parts = shlex.split(command_line.strip())
            if not parts:
                return None, []
            return parts[0], parts[1:]
        except ValueError:
            print("Error: Invalid command syntax")
            return None, []
    
    def handle_mkdir(self, args: list):
        """Handle mkdir command"""
        if not args:
            print("Usage: mkdir [-p] <directory>...")
            return
        
        recursive = False
        dirs = []
        
        i = 0
        while i < len(args):
            if args[i] == "-p":
                recursive = True
            else:
                dirs.append(args[i])
            i += 1
        
        if not dirs:
            print("Usage: mkdir [-p] <directory>...")
            return
        
        for directory in dirs:
            self.fs.mkdir(directory, recursive=recursive)
    
    def handle_touch(self, args: list):
        """Handle touch command"""
        if not args:
            print("Usage: touch <file>...")
            return
        
        for file_path in args:
            self.fs.touch(file_path)
    
    def handle_rm(self, args: list):
        """Handle rm command"""
        if not args:
            print("Usage: rm [-rf] <file/directory>...")
            return
        
        recursive = False
        force = False
        files = []
        
        i = 0
        while i < len(args):
            if args[i].startswith("-"):
                if "r" in args[i]:
                    recursive = True
                if "f" in args[i]:
                    force = True
            else:
                files.append(args[i])
            i += 1
        
        if not files:
            print("Usage: rm [-rf] <file/directory>...")
            return
        
        for file_path in files:
            self.fs.rm(file_path, recursive=recursive, force=force)
    
    def handle_ls(self, args: list):
        """Handle ls command"""
        long_format = False
        all_files = False
        paths = []
        
        i = 0
        while i < len(args):
            if args[i].startswith("-"):
                if "l" in args[i]:
                    long_format = True
                if "a" in args[i]:
                    all_files = True
            else:
                paths.append(args[i])
            i += 1
        
        if not paths:
            paths = [None]  # Current directory
        
        for path in paths:
            if len(paths) > 1 and path:
                print(f"\n{path}:")
            self.fs.ls(path, long_format=long_format, all_files=all_files)
    
    def handle_cd(self, args: list):
        """Handle cd command"""
        if not args:
            self.fs.cd("/")  # Go to root if no argument
        else:
            self.fs.cd(args[0])
    
    def handle_pwd(self, args: list):
        """Handle pwd command"""
        self.fs.pwd()
    
    def handle_cp(self, args: list):
        """Handle cp command"""
        if len(args) != 2:
            print("Usage: cp <source> <destination>")
            return
        
        self.fs.cp(args[0], args[1])
    
    def handle_mv(self, args: list):
        """Handle mv command"""
        if len(args) != 2:
            print("Usage: mv <source> <destination>")
            return
        
        self.fs.mv(args[0], args[1])
    
    def handle_df(self, args: list):
        """Handle df command"""
        self.fs.df()
    
    def handle_find(self, args: list):
        """Handle find command"""
        if not args:
            print("Usage: find <name> [path]")
            return
        
        name = args[0]
        path = args[1] if len(args) > 1 else None
        self.fs.find(name, path)
    
    def handle_stat(self, args: list):
        """Handle stat command"""
        if not args:
            print("Usage: stat <file/directory>")
            return
        
        for path in args:
            self.fs.stat(path)
            if len(args) > 1:
                print()
    
    def handle_help(self, args: list):
        """Handle help command"""
        print("Available commands:")
        print("  mkdir [-p] <dir>...     - Create directories")
        print("  touch <file>...         - Create files or update timestamps")
        print("  rm [-rf] <path>...      - Remove files/directories")
        print("  ls [-la] [path]...      - List directory contents")
        print("  cd [path]               - Change directory")
        print("  pwd                     - Print working directory")
        print("  cp <src> <dst>          - Copy file/directory")
        print("  mv <src> <dst>          - Move/rename file/directory")
        print("  df                      - Display filesystem usage")
        print("  find <name> [path]      - Find files/directories")
        print("  stat <path>             - Display file/directory info")
        print("  clear                   - Clear screen")
        print("  help                    - Show this help")
        print("  exit, quit              - Exit the program")
    
    def handle_clear(self, args: list):
        """Handle clear command"""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def handle_exit(self, args: list):
        """Handle exit command"""
        print("Goodbye!")
        self.running = False
    
    def execute_command(self, command: str, args: list):
        """Execute a command"""
        commands = {
            'mkdir': self.handle_mkdir,
            'touch': self.handle_touch,
            'rm': self.handle_rm,
            'ls': self.handle_ls,
            'cd': self.handle_cd,
            'pwd': self.handle_pwd,
            'cp': self.handle_cp,
            'mv': self.handle_mv,
            'df': self.handle_df,
            'find': self.handle_find,
            'stat': self.handle_stat,
            'help': self.handle_help,
            'clear': self.handle_clear,
            'exit': self.handle_exit,
            'quit': self.handle_exit
        }
        
        if command in commands:
            try:
                commands[command](args)
            except Exception as e:
                print(f"Error executing command: {e}")
        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands")
    
    def run(self):
        """Main CLI loop"""
        print("Welcome to File System Simulator")
        print("Type 'help' for available commands")
        print()
        
        while self.running:
            try:
                command_line = input(self.get_prompt())
                
                if not command_line.strip():
                    continue
                
                command, args = self.parse_command(command_line)
                
                if command:
                    self.execute_command(command, args)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to exit the program")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")

def main():
    """Main function"""
    cli = FileSystemCLI()
    cli.run()

if __name__ == "__main__":
    main()
