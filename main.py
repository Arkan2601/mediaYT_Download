import ttkbootstrap as tb
from ui import create_ui
from explorer import populate_tree, go_to_parent, select_download_folder, on_item_double_click
from downloader import download_video, download_audio  # Importar funciones de descarga

# ======= Configuración Inicial =======
download_folder = "C:/Users/Arkan/Downloads"  # Cambia esto según tu preferencia
icons = {}  # Placeholder para íconos (si los usas)

# ======= Crear Ventana Principal =======
root = tb.Window(themename="darkly")
root.title("Media Downloader")
root.geometry("800x600")

# ======= Inicializar UI =======
ui_elements = create_ui(
    root, 
    download_folder, 
    icons, 
    lambda url, folder, tree, label: download_video(url, folder, tree, label, root),  # Pasar root
    lambda url, folder, tree, label: download_audio(url, folder, tree, label, root),  # Pasar root
    go_to_parent, 
    select_download_folder, 
    on_item_double_click
)

# Obtener elementos UI
file_tree = ui_elements["file_tree"]
folder_label = ui_elements["folder_label"]

# Poblar el explorador de archivos con la carpeta inicial
populate_tree(download_folder, file_tree, folder_label)

# Conectar doble clic en el explorador de archivos
file_tree.bind("<Double-1>", lambda event: on_item_double_click(event, file_tree, folder_label))

# ======= Ejecutar Aplicación =======
root.mainloop()