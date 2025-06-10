#!/usr/bin/env python3
"""
Test Suite untuk File System Simulator
"""

import unittest
import os
import json
from file_system import FileSystemSimulator

class TestFileSystemSimulator(unittest.TestCase):
    def setUp(self):
        """Setup untuk setiap test"""
        self.fs = FileSystemSimulator(disk_size=100)  # 100MB untuk testing
        # Hapus file test jika ada
        test_file = "/home/Progger/Sisop 2/filesystem_data.json"
        if os.path.exists(test_file):
            os.remove(test_file)
    
    def tearDown(self):
        """Cleanup setelah test"""
        test_file = "/home/Progger/Sisop 2/filesystem_data.json"
        if os.path.exists(test_file):
            os.remove(test_file)
    
    def test_mkdir_basic(self):
        """Test basic mkdir functionality"""
        self.assertTrue(self.fs.mkdir("test_dir"))
        self.assertTrue(self.fs.path_exists("/test_dir"))
        self.assertEqual(self.fs.file_system["/test_dir"]["type"], "directory")
    
    def test_mkdir_recursive(self):
        """Test mkdir dengan -p flag"""
        self.assertTrue(self.fs.mkdir("parent/child", recursive=True))
        self.assertTrue(self.fs.path_exists("/parent"))
        self.assertTrue(self.fs.path_exists("/parent/child"))
    
    def test_mkdir_existing(self):
        """Test mkdir pada directory yang sudah ada"""
        self.fs.mkdir("test_dir")
        self.assertFalse(self.fs.mkdir("test_dir"))
    
    def test_touch_basic(self):
        """Test basic touch functionality"""
        self.assertTrue(self.fs.touch("test_file.txt"))
        self.assertTrue(self.fs.path_exists("/test_file.txt"))
        self.assertEqual(self.fs.file_system["/test_file.txt"]["type"], "file")
    
    def test_touch_with_size(self):
        """Test touch dengan ukuran file"""
        self.assertTrue(self.fs.touch("big_file.txt", size=1024))
        self.assertEqual(self.fs.file_system["/big_file.txt"]["size"], 1024)
        self.assertEqual(self.fs.used_space, 1024)
    
    def test_ls_empty_directory(self):
        """Test ls pada directory kosong"""
        result = self.fs.ls("/")
        self.assertEqual(len(result), 0)
    
    def test_ls_with_files(self):
        """Test ls dengan file dan directory"""
        self.fs.mkdir("dir1")
        self.fs.touch("file1.txt")
        result = self.fs.ls("/")
        self.assertIn("dir1/", result)
        self.assertIn("file1.txt", result)
    
    def test_cd_basic(self):
        """Test basic cd functionality"""
        self.fs.mkdir("test_dir")
        self.assertTrue(self.fs.cd("test_dir"))
        self.assertEqual(self.fs.current_directory, "/test_dir")
    
    def test_cd_parent(self):
        """Test cd ke parent directory"""
        self.fs.mkdir("test_dir")
        self.fs.cd("test_dir")
        self.assertTrue(self.fs.cd(".."))
        self.assertEqual(self.fs.current_directory, "/")
    
    def test_cd_nonexistent(self):
        """Test cd ke directory yang tidak ada"""
        self.assertFalse(self.fs.cd("nonexistent"))
        self.assertEqual(self.fs.current_directory, "/")
    
    def test_rm_file(self):
        """Test rm file"""
        self.fs.touch("test_file.txt")
        self.assertTrue(self.fs.rm("test_file.txt"))
        self.assertFalse(self.fs.path_exists("/test_file.txt"))
    
    def test_rm_directory_recursive(self):
        """Test rm directory secara recursive"""
        self.fs.mkdir("test_dir")
        self.fs.cd("test_dir")
        self.fs.touch("file_in_dir.txt")
        self.fs.cd("/")
        self.assertTrue(self.fs.rm("test_dir", recursive=True))
        self.assertFalse(self.fs.path_exists("/test_dir"))
    
    def test_rm_nonempty_directory_no_recursive(self):
        """Test rm directory yang tidak kosong tanpa -r"""
        self.fs.mkdir("test_dir")
        self.fs.cd("test_dir")
        self.fs.touch("file_in_dir.txt")
        self.fs.cd("/")
        self.assertFalse(self.fs.rm("test_dir", recursive=False))
        self.assertTrue(self.fs.path_exists("/test_dir"))
    
    def test_cp_file(self):
        """Test copy file"""
        self.fs.touch("original.txt", size=100)
        self.assertTrue(self.fs.cp("original.txt", "copy.txt"))
        self.assertTrue(self.fs.path_exists("/copy.txt"))
        self.assertEqual(self.fs.file_system["/copy.txt"]["size"], 100)
        self.assertEqual(self.fs.used_space, 200)  # Original + copy
    
    def test_mv_file(self):
        """Test move file"""
        self.fs.touch("original.txt", size=100)
        self.assertTrue(self.fs.mv("original.txt", "moved.txt"))
        self.assertFalse(self.fs.path_exists("/original.txt"))
        self.assertTrue(self.fs.path_exists("/moved.txt"))
        self.assertEqual(self.fs.used_space, 100)  # Space should remain same
    
    def test_find_file(self):
        """Test find functionality"""
        self.fs.mkdir("test_dir")
        self.fs.cd("test_dir")
        self.fs.touch("test_file.txt")
        self.fs.cd("/")
        
        results = self.fs.find("test_file.txt")
        self.assertIn("/test_dir/test_file.txt", results)
    
    def test_disk_space_limit(self):
        """Test disk space limitation"""
        # Try to create file larger than disk
        large_size = self.fs.disk_size * 1024 * 1024 + 1  # Larger than disk
        self.assertFalse(self.fs.touch("huge_file.txt", size=large_size))
    
    def test_absolute_vs_relative_paths(self):
        """Test absolute vs relative paths"""
        self.fs.mkdir("test_dir")
        self.fs.cd("test_dir")
        
        # Test relative path
        self.assertTrue(self.fs.touch("relative_file.txt"))
        self.assertTrue(self.fs.path_exists("/test_dir/relative_file.txt"))
        
        # Test absolute path
        self.assertTrue(self.fs.touch("/absolute_file.txt"))
        self.assertTrue(self.fs.path_exists("/absolute_file.txt"))
    
    def test_pwd(self):
        """Test pwd functionality"""
        self.assertEqual(self.fs.pwd(), "/")
        self.fs.mkdir("test_dir")
        self.fs.cd("test_dir")
        self.assertEqual(self.fs.pwd(), "/test_dir")
    
    def test_stat(self):
        """Test stat functionality"""
        self.fs.touch("test_file.txt", size=1024)
        info = self.fs.stat("test_file.txt")
        
        self.assertEqual(info["type"], "file")
        self.assertEqual(info["size"], 1024)
        self.assertEqual(info["owner"], "user")
    
    def test_df(self):
        """Test df functionality"""
        self.fs.touch("test_file.txt", size=1024)
        info = self.fs.df()
        
        self.assertEqual(info["used"], 1024)
        self.assertEqual(info["total"], self.fs.disk_size * 1024 * 1024)
        self.assertGreater(info["free"], 0)
    
    def test_persistence(self):
        """Test data persistence"""
        # Create some files and directories
        self.fs.mkdir("persist_dir")
        self.fs.touch("persist_file.txt", size=500)
        self.fs.cd("persist_dir")
        
        # Save state
        self.fs.save_filesystem()
        
        # Create new filesystem instance (simulate restart)
        fs2 = FileSystemSimulator()
        
        # Check if data persisted
        self.assertTrue(fs2.path_exists("/persist_dir"))
        self.assertTrue(fs2.path_exists("/persist_file.txt"))
        self.assertEqual(fs2.current_directory, "/persist_dir")
        self.assertEqual(fs2.used_space, 500)

def run_tests():
    """Run all tests"""
    unittest.main(verbosity=2)

if __name__ == "__main__":
    run_tests()
