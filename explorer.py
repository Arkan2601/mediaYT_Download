import os
import datetime
import tkinter.messagebox as messagebox
import ctypes

def format_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def is_hidden(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
        return attrs != -1 and (attrs & 2)  # 2 es FILE_ATTRIBUTE_HIDDEN
    except Exception:
        return False

def populate_tree(directory, file_tree, folder_label):
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "El directorio especificado no existe.")
        return

    folder_label.config(text=f"📂 Carpeta: {directory}")
    
    file_tree.delete(*file_tree.get_children())
    try:
        items = [
            (item, os.path.join(directory, item), os.path.isdir(os.path.join(directory, item))) 
            for item in os.listdir(directory) if not is_hidden(os.path.join(directory, item))
        ]
        for name, path, is_dir in sorted(items, key=lambda x: (not x[2], x[0].lower())):
            file_tree.insert('', 'end', text=name, values=("Carpeta" if is_dir else os.path.splitext(name)[1].lower(), format_date(os.path.getctime(path))))
    except PermissionError:
        messagebox.showerror("Error", "No tienes permiso para acceder a esta carpeta.")

def on_item_double_click(event, file_tree, folder_label):
    selected_item = file_tree.focus()
    if not selected_item:
        return
    
    # Obtener ruta absoluta combinando la carpeta actual con el nombre del ítem
    current_folder = folder_label.cget("text").replace("📂 Carpeta: ", "")
    item_name = file_tree.item(selected_item, 'text')
    item_path = os.path.join(current_folder, item_name)

    if os.path.isdir(item_path):
        populate_tree(item_path, file_tree, folder_label)
    elif os.path.isfile(item_path):
        try:
            os.startfile(item_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

def go_to_parent(download_folder, file_tree, folder_label):
    parent_path = os.path.dirname(download_folder)
    if parent_path and parent_path != download_folder:
        populate_tree(parent_path, file_tree, folder_label)

def select_download_folder(file_tree, folder_label):
    from tkinter import filedialog
    folder = filedialog.askdirectory()
    if folder:
        populate_tree(folder, file_tree, folder_label)
