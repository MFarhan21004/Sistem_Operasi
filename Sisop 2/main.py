#!/usr/bin/env python3
"""
Main launcher untuk File System Simulator
Pilih antara CLI atau GUI mode
"""

import sys
import os

def print_banner():
    """Print banner aplikasi"""
    print("="*60)
    print("     FILE SYSTEM SIMULATOR - TUGAS SISTEM OPERASI")
    print("="*60)
    print("Simulasi sistem manajemen file seperti hard drive")
    print("dengan berbagai command seperti mkdir, rm, ls, dll.")
    print("="*60)
    print()

def print_menu():
    """Print menu pilihan"""
    print("Pilih mode aplikasi:")
    print("1. CLI Mode  - Terminal/Command Line Interface")
    print("2. GUI Mode  - Graphical User Interface")
    print("3. Run Tests - Jalankan unit tests")
    print("4. Exit      - Keluar dari aplikasi")
    print()

def main():
    """Main function"""
    print_banner()
    
    while True:
        print_menu()
        try:
            choice = input("Masukkan pilihan (1-4): ").strip()
            
            if choice == "1":
                print("\nMemulai CLI Mode...")
                print("Ketik 'help' untuk melihat command yang tersedia")
                print("Ketik 'exit' untuk keluar")
                print()
                
                try:
                    from cli import main as cli_main
                    cli_main()
                except KeyboardInterrupt:
                    print("\nKeluar dari CLI mode...")
                except ImportError as e:
                    print(f"Error import CLI module: {e}")
                except Exception as e:
                    print(f"Error menjalankan CLI: {e}")
                
            elif choice == "2":
                print("\nMemulai GUI Mode...")
                try:
                    import tkinter as tk
                    from gui import main as gui_main
                    gui_main()
                except ImportError:
                    print("Error: Tkinter tidak tersedia. Gunakan CLI mode.")
                except Exception as e:
                    print(f"Error menjalankan GUI: {e}")
                    
            elif choice == "3":
                print("\nMenjalankan unit tests...")
                try:
                    from test_filesystem import run_tests
                    run_tests()
                except Exception as e:
                    print(f"Error menjalankan tests: {e}")
                    
            elif choice == "4":
                print("Terima kasih telah menggunakan File System Simulator!")
                sys.exit(0)
                
            else:
                print("Pilihan tidak valid. Silakan pilih 1-4.")
                
        except KeyboardInterrupt:
            print("\n\nTerima kasih telah menggunakan File System Simulator!")
            sys.exit(0)
        except EOFError:
            print("\n\nTerima kasih telah menggunakan File System Simulator!")
            sys.exit(0)
        except Exception as e:
            print(f"Error tidak terduga: {e}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
