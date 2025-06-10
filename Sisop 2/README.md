# File System Simulator - Tugas Sistem Operasi

Simulasi sistem manajemen file yang menyerupai hard drive dengan berbagai command seperti sistem operasi Unix/Linux.

## Fitur

### Command Line Interface (CLI)
- **mkdir** - Membuat directory baru
- **touch** - Membuat file baru atau update timestamp
- **rm** - Menghapus file/directory 
- **ls** - Menampilkan isi directory
- **cd** - Berpindah directory
- **pwd** - Menampilkan current directory
- **cp** - Copy file/directory
- **mv** - Move/rename file/directory
- **df** - Menampilkan penggunaan disk
- **find** - Mencari file/directory
- **stat** - Menampilkan informasi detail file/directory

### Graphical User Interface (GUI)
- Tree view untuk menampilkan struktur file system
- Toolbar dengan tombol untuk operasi file
- Panel detail untuk informasi file
- Panel system information untuk status disk
- Integrated command line
- Context menu (klik kanan)

### Fitur Sistem
- Simulasi disk dengan ukuran terbatas (default 1GB)
- Persistent storage (data disimpan dalam JSON)
- Manajemen space dan quota
- File permissions dan ownership
- Timestamp tracking (created/modified)
- Path resolution (absolute/relative)

## Struktur File

```
/home/Progger/Sisop 2/
├── main.py              # Main launcher
├── file_system.py       # Core file system logic
├── cli.py              # Command line interface
├── gui.py              # Graphical user interface
├── test_filesystem.py  # Unit tests
├── tugas.txt           # Spesifikasi tugas
└── README.md           # Dokumentasi ini
```

## Instalasi dan Penggunaan

### Persyaratan
- Python 3.6+
- Tkinter (untuk GUI mode, biasanya sudah include di Python)

### Menjalankan Aplikasi

1. **Main Launcher**
   ```bash
   python3 main.py
   ```
   Akan menampilkan menu untuk memilih mode:
   - CLI Mode
   - GUI Mode  
   - Run Tests

2. **CLI Mode Langsung**
   ```bash
   python3 cli.py
   ```

3. **GUI Mode Langsung**
   ```bash
   python3 gui.py
   ```

4. **Menjalankan Tests**
   ```bash
   python3 test_filesystem.py
   ```

## Contoh Penggunaan CLI

```bash
# Membuat directory
simfs:/$ mkdir documents
simfs:/$ mkdir -p projects/python/myapp

# Membuat file
simfs:/$ touch readme.txt
simfs:/$ touch projects/python/main.py

# Navigasi
simfs:/$ cd documents
simfs:/documents$ pwd
simfs:/documents$ cd ..
simfs:/$ ls -la

# Copy dan move
simfs:/$ cp readme.txt backup.txt
simfs:/$ mv backup.txt documents/

# Hapus file/directory
simfs:/$ rm documents/backup.txt
simfs:/$ rm -rf projects

# Informasi sistem
simfs:/$ df
simfs:/$ stat readme.txt
simfs:/$ find main.py
```

## Arsitektur Sistem

### FileSystemSimulator Class
Core class yang mengimplementasikan:
- File system tree structure
- Space management
- Path resolution
- CRUD operations
- Persistence

### CLI Interface
- Command parsing
- Interactive shell
- Help system
- Error handling

### GUI Interface
- Tkinter-based interface
- Tree view navigation
- Drag & drop operations
- Context menus
- Real-time updates

## Testing

Unit tests mencakup:
- Basic file operations
- Directory operations
- Path resolution
- Space management
- Error conditions
- Data persistence

Jalankan tests dengan:
```bash
python3 test_filesystem.py -v
```

## Limitasi

1. **Simulasi Only** - Tidak mengakses real file system
2. **Single User** - Tidak ada multi-user support
3. **Basic Permissions** - Simplified permission model
4. **Memory Based** - File content tidak disimpan, hanya metadata
5. **Single Threading** - Tidak ada concurrent access handling

## Implementasi Teknis

### Data Structure
```python
file_system = {
    "/": {
        "type": "directory",
        "created": "2024-01-01T00:00:00",
        "modified": "2024-01-01T00:00:00", 
        "size": 0,
        "permissions": "rwxr-xr-x",
        "owner": "user",
        "children": {
            "file1.txt": "/file1.txt",
            "dir1": "/dir1"
        }
    },
    "/file1.txt": {
        "type": "file",
        "size": 1024,
        # ... metadata lainnya
    }
}
```

### Persistence
Data disimpan dalam `filesystem_data.json` yang berisi:
- File system tree
- Current directory
- Disk usage
- Configuration

## Pengembangan Lebih Lanjut

Fitur yang bisa ditambahkan:
1. File content editor
2. Symbolic links
3. File compression
4. Network file system
5. Multi-user support
6. Advanced permissions
7. File versioning
8. Backup/restore
9. File search indexing
10. Plugin system

## Kontribusi

Tugas ini dibuat untuk mata kuliah Sistem Operasi dengan tujuan memahami:
- File system concepts
- Directory structures  
- File operations
- Space management
- User interfaces
- Testing methodologies

---
**Dibuat oleh**: Mahasiswa Sistem Operasi  
**Tanggal**: 2024  
**Versi**: 1.0
