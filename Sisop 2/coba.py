import datetime

TOTAL_CAPACITY = 1_000_000  # 1 GB = 1,000,000 KB
used_space = 0

class FileNode:
    def __init__(self, name, is_dir, size=0):
        self.name = name
        self.is_dir = is_dir
        self.size = size
        self.created = datetime.datetime.now()
        self.children = {} if is_dir else None
        self.parent = None

    def add_child(self, node):
        if self.is_dir:
            self.children[node.name] = node
            node.parent = self

    def remove_child(self, name):
        if name in self.children:
            del self.children[name]

root = FileNode("/", True)
current_dir = root

def get_path(node):
    path = []
    while node and node.name != "/":
        path.append(node.name)
        node = node.parent
    return "/" + "/".join(reversed(path))

def mkdir(name):
    if name in current_dir.children:
        print("Folder sudah ada.")
    else:
        new_folder = FileNode(name, True)
        current_dir.add_child(new_folder)

def touch(name, size):
    global used_space
    size = int(size)
    if used_space + size > TOTAL_CAPACITY:
        print("Gagal: ruang disk tidak cukup.")
        return
    if name in current_dir.children:
        print("File sudah ada.")
        return
    new_file = FileNode(name, False, size)
    current_dir.add_child(new_file)
    used_space += size

def ls():
    for child in current_dir.children.values():
        tipe = "DIR" if child.is_dir else "FILE"
        print(f"{tipe}\t{child.name}")

def cd(name):
    global current_dir
    if name == "..":
        if current_dir.parent:
            current_dir = current_dir.parent
    elif name in current_dir.children and current_dir.children[name].is_dir:
        current_dir = current_dir.children[name]
    else:
        print("Folder tidak ditemukan.")

def rm(name):
    global used_space
    node = current_dir.children.get(name)
    if node and not node.is_dir:
        used_space -= node.size
        current_dir.remove_child(name)
    else:
        print("File tidak ditemukan atau ini folder.")

def rmdir(name):
    node = current_dir.children.get(name)
    if node and node.is_dir and not node.children:
        current_dir.remove_child(name)
    else:
        print("Folder tidak kosong atau tidak ditemukan.")

def stat(name):
    node = current_dir.children.get(name)
    if node:
        print(f"Nama: {node.name}")
        print(f"Jenis: {'Folder' if node.is_dir else 'File'}")
        print(f"Ukuran: {node.size} KB")
        print(f"Dibuat: {node.created}")
    else:
        print("File/folder tidak ditemukan.")

def pwd():
    print(get_path(current_dir))

def disk_status():
    print(f"Total: {TOTAL_CAPACITY} KB | Terpakai: {used_space} KB | Sisa: {TOTAL_CAPACITY - used_space} KB")

# Loop utama CLI
def run_cli():
    while True:
        cmd = input(f"{get_path(current_dir)}> ").strip().split()
        if not cmd:
            continue
        match cmd[0]:
            case "exit": break
            case "mkdir": mkdir(cmd[1])
            case "touch": 
                if len(cmd) == 3: touch(cmd[1], cmd[2])
                else: print("Gunakan: touch <nama> <ukuran>")
            case "ls": ls()
            case "cd": cd(cmd[1])
            case "pwd": pwd()
            case "rm": rm(cmd[1])
            case "rmdir": rmdir(cmd[1])
            case "stat": stat(cmd[1])
            case "disk": disk_status()
            case _: print("Perintah tidak dikenali")

run_cli()
