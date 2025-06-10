#!/usr/bin/env python3
"""
Sistem Manajemen File - Simulasi File System
Tugas Sistem Operasi
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import shutil

class FileSystemSimulator:
    def __init__(self, disk_size: int = 1024):  # Size in MB
        self.disk_size = disk_size
        self.used_space = 0
        self.current_directory = "/"
        self.file_system = {
            "/": {
                "type": "directory",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "size": 0,
                "permissions": "rwxr-xr-x",
                "owner": "user",
                "children": {}
            }
        }
        self.load_filesystem()
    
    def save_filesystem(self):
        """Simpan filesystem ke file JSON"""
        try:
            with open("filesystem_data.json", "w") as f:
                json.dump({
                    "file_system": self.file_system,
                    "current_directory": self.current_directory,
                    "used_space": self.used_space,
                    "disk_size": self.disk_size
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving filesystem: {e}")
    
    def load_filesystem(self):
        """Load filesystem dari file JSON"""
        try:
            if os.path.exists("filesystem_data.json"):
                with open("filesystem_data.json", "r") as f:
                    data = json.load(f)
                    self.file_system = data.get("file_system", self.file_system)
                    self.current_directory = data.get("current_directory", "/")
                    self.used_space = data.get("used_space", 0)
                    self.disk_size = data.get("disk_size", 1024)
        except Exception as e:
            print(f"Error loading filesystem: {e}")
    
    def get_absolute_path(self, path: str) -> str:
        """Konversi path relatif ke absolute path"""
        if path.startswith("/"):
            return path
        
        if self.current_directory == "/":
            return "/" + path
        else:
            return self.current_directory + "/" + path
    
    def path_exists(self, path: str) -> bool:
        """Cek apakah path ada dalam filesystem"""
        abs_path = self.get_absolute_path(path)
        return abs_path in self.file_system
    
    def get_parent_path(self, path: str) -> str:
        """Dapatkan parent directory dari path"""
        if path == "/":
            return "/"
        parts = path.rstrip("/").split("/")
        if len(parts) <= 1:
            return "/"
        return "/".join(parts[:-1]) or "/"
    
    def get_filename(self, path: str) -> str:
        """Dapatkan nama file/directory dari path"""
        return path.rstrip("/").split("/")[-1]
    
    def mkdir(self, path: str, recursive: bool = False) -> bool:
        """Buat directory baru"""
        abs_path = self.get_absolute_path(path)
        
        if self.path_exists(abs_path):
            print(f"Directory '{path}' already exists")
            return False
        
        parent_path = self.get_parent_path(abs_path)
        
        if not self.path_exists(parent_path):
            if recursive:
                self.mkdir(parent_path, recursive=True)
            else:
                print(f"Parent directory '{parent_path}' does not exist")
                return False
        
        if self.file_system[parent_path]["type"] != "directory":
            print(f"'{parent_path}' is not a directory")
            return False
        
        # Buat directory baru
        dir_name = self.get_filename(abs_path)
        self.file_system[abs_path] = {
            "type": "directory",
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "size": 0,
            "permissions": "rwxr-xr-x",
            "owner": "user",
            "children": {}
        }
        
        # Update parent directory
        self.file_system[parent_path]["children"][dir_name] = abs_path
        self.file_system[parent_path]["modified"] = datetime.now().isoformat()
        
        self.save_filesystem()
        print(f"Directory '{path}' created successfully")
        return True
    
    def touch(self, path: str, size: int = 0) -> bool:
        """Buat file baru atau update timestamp"""
        abs_path = self.get_absolute_path(path)
        
        if self.path_exists(abs_path):
            # Update timestamp
            self.file_system[abs_path]["modified"] = datetime.now().isoformat()
            print(f"File '{path}' timestamp updated")
            return True
        
        parent_path = self.get_parent_path(abs_path)
        
        if not self.path_exists(parent_path):
            print(f"Parent directory '{parent_path}' does not exist")
            return False
        
        if self.file_system[parent_path]["type"] != "directory":
            print(f"'{parent_path}' is not a directory")
            return False
        
        # Cek space
        if self.used_space + size > self.disk_size * 1024 * 1024:  # Convert MB to bytes
            print("Not enough disk space")
            return False
        
        # Buat file baru
        file_name = self.get_filename(abs_path)
        self.file_system[abs_path] = {
            "type": "file",
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "size": size,
            "permissions": "rw-r--r--",
            "owner": "user",
            "content": ""
        }
        
        # Update parent directory
        self.file_system[parent_path]["children"][file_name] = abs_path
        self.file_system[parent_path]["modified"] = datetime.now().isoformat()
        
        self.used_space += size
        self.save_filesystem()
        print(f"File '{path}' created successfully")
        return True
    
    def rm(self, path: str, recursive: bool = False, force: bool = False) -> bool:
        """Hapus file atau directory"""
        abs_path = self.get_absolute_path(path)
        
        if not self.path_exists(abs_path):
            if not force:
                print(f"'{path}' does not exist")
            return False
        
        if abs_path == "/":
            print("Cannot remove root directory")
            return False
        
        file_info = self.file_system[abs_path]
        
        # Jika directory dan tidak kosong
        if file_info["type"] == "directory" and file_info["children"]:
            if not recursive:
                print(f"Directory '{path}' is not empty. Use -r flag to remove recursively")
                return False
            
            # Hapus semua children secara rekursif
            for child_name, child_path in list(file_info["children"].items()):
                self.rm(child_path, recursive=True, force=True)
        
        # Hapus dari parent directory
        parent_path = self.get_parent_path(abs_path)
        file_name = self.get_filename(abs_path)
        
        if parent_path in self.file_system:
            if file_name in self.file_system[parent_path]["children"]:
                del self.file_system[parent_path]["children"][file_name]
            self.file_system[parent_path]["modified"] = datetime.now().isoformat()
        
        # Update used space
        if file_info["type"] == "file":
            self.used_space -= file_info["size"]
        
        # Hapus dari filesystem
        del self.file_system[abs_path]
        
        self.save_filesystem()
        print(f"'{path}' removed successfully")
        return True
    
    def ls(self, path: str = None, long_format: bool = False, all_files: bool = False) -> List[str]:
        """List isi directory"""
        if path is None:
            path = self.current_directory
        
        abs_path = self.get_absolute_path(path)
        
        if not self.path_exists(abs_path):
            print(f"'{path}' does not exist")
            return []
        
        if self.file_system[abs_path]["type"] != "directory":
            print(f"'{path}' is not a directory")
            return []
        
        children = self.file_system[abs_path]["children"]
        result = []
        
        if not children:
            print("Directory is empty")
            return []
        
        for name, child_path in sorted(children.items()):
            if not all_files and name.startswith("."):
                continue
            
            child_info = self.file_system[child_path]
            
            if long_format:
                # Format: permissions owner size date name
                perms = child_info["permissions"]
                owner = child_info["owner"]
                size = child_info["size"]
                modified = datetime.fromisoformat(child_info["modified"]).strftime("%b %d %H:%M")
                file_type = "d" if child_info["type"] == "directory" else "-"
                
                line = f"{file_type}{perms} {owner:>8} {size:>8} {modified} {name}"
                if child_info["type"] == "directory":
                    line += "/"
                
                result.append(line)
                print(line)
            else:
                display_name = name
                if child_info["type"] == "directory":
                    display_name += "/"
                result.append(display_name)
                print(display_name, end="  ")
        
        if not long_format:
            print()  # New line after listing
        
        return result
    
    def cd(self, path: str) -> bool:
        """Change directory"""
        if path == "..":
            if self.current_directory != "/":
                self.current_directory = self.get_parent_path(self.current_directory)
            return True
        
        abs_path = self.get_absolute_path(path)
        
        if not self.path_exists(abs_path):
            print(f"Directory '{path}' does not exist")
            return False
        
        if self.file_system[abs_path]["type"] != "directory":
            print(f"'{path}' is not a directory")
            return False
        
        self.current_directory = abs_path
        self.save_filesystem()
        return True
    
    def pwd(self) -> str:
        """Print working directory"""
        print(self.current_directory)
        return self.current_directory
    
    def cp(self, source: str, destination: str) -> bool:
        """Copy file atau directory"""
        abs_source = self.get_absolute_path(source)
        abs_dest = self.get_absolute_path(destination)
        
        if not self.path_exists(abs_source):
            print(f"Source '{source}' does not exist")
            return False
        
        if self.path_exists(abs_dest):
            print(f"Destination '{destination}' already exists")
            return False
        
        source_info = self.file_system[abs_source]
        
        # Copy file info
        new_info = source_info.copy()
        new_info["created"] = datetime.now().isoformat()
        new_info["modified"] = datetime.now().isoformat()
        
        if source_info["type"] == "file":
            # Cek space
            if self.used_space + source_info["size"] > self.disk_size * 1024 * 1024:
                print("Not enough disk space")
                return False
            self.used_space += source_info["size"]
        
        self.file_system[abs_dest] = new_info
        
        # Update parent directory
        parent_path = self.get_parent_path(abs_dest)
        file_name = self.get_filename(abs_dest)
        
        if parent_path in self.file_system:
            self.file_system[parent_path]["children"][file_name] = abs_dest
            self.file_system[parent_path]["modified"] = datetime.now().isoformat()
        
        self.save_filesystem()
        print(f"'{source}' copied to '{destination}'")
        return True
    
    def mv(self, source: str, destination: str) -> bool:
        """Move/rename file atau directory"""
        if self.cp(source, destination):
            return self.rm(source, recursive=True, force=True)
        return False
    
    def df(self) -> Dict[str, Any]:
        """Display filesystem disk usage"""
        total_space = self.disk_size * 1024 * 1024  # Convert to bytes
        used_space = self.used_space
        free_space = total_space - used_space
        usage_percent = (used_space / total_space) * 100 if total_space > 0 else 0
        
        info = {
            "total": total_space,
            "used": used_space,
            "free": free_space,
            "usage_percent": usage_percent
        }
        
        print(f"Filesystem     Size   Used  Avail Use%")
        print(f"simfs         {self.disk_size}M   {used_space//1024//1024}M   {free_space//1024//1024}M   {usage_percent:.1f}%")
        
        return info
    
    def find(self, name: str, path: str = None) -> List[str]:
        """Cari file/directory berdasarkan nama"""
        if path is None:
            path = self.current_directory
        
        abs_path = self.get_absolute_path(path)
        results = []
        
        def search_recursive(current_path: str):
            if not self.path_exists(current_path):
                return
            
            current_info = self.file_system[current_path]
            current_name = self.get_filename(current_path)
            
            # Check if current item matches
            if name in current_name or current_name == name:
                results.append(current_path)
            
            # Search in children if directory
            if current_info["type"] == "directory":
                for child_name, child_path in current_info["children"].items():
                    search_recursive(child_path)
        
        search_recursive(abs_path)
        
        if results:
            for result in results:
                print(result)
        else:
            print(f"No files or directories found matching '{name}'")
        
        return results
    
    def stat(self, path: str) -> Dict[str, Any]:
        """Display detailed file/directory information"""
        abs_path = self.get_absolute_path(path)
        
        if not self.path_exists(abs_path):
            print(f"'{path}' does not exist")
            return {}
        
        info = self.file_system[abs_path]
        
        print(f"File: {path}")
        print(f"Type: {info['type']}")
        print(f"Size: {info['size']} bytes")
        print(f"Permissions: {info['permissions']}")
        print(f"Owner: {info['owner']}")
        print(f"Created: {info['created']}")
        print(f"Modified: {info['modified']}")
        
        if info["type"] == "directory":
            print(f"Children: {len(info['children'])}")
        
        return info
