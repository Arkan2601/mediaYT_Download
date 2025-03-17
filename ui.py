import ttkbootstrap as tb
from ttkbootstrap.constants import *

def create_ui(root, download_folder, icons, download_video, download_audio, go_to_parent, select_download_folder, on_item_double_click):
    # Configurar la disposición de la ventana principal
    root.grid_rowconfigure(0, weight=0)  # Control frame (no expandible)
    root.grid_rowconfigure(1, weight=1)  # File tree (expandible)
    root.grid_columnconfigure(0, weight=1)  # Expandible en horizontal

    # ========== Marco de Controles ==========
    control_frame = tb.Frame(root, padding=10)
    control_frame.grid(row=0, column=0, sticky="ew")
    control_frame.grid_columnconfigure(1, weight=1)  # Expansión de la entrada de URL

    # ----- Fila 1: Entrada de URL -----
    tb.Label(control_frame, text="🔗 URL de YouTube:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    url_entry = tb.Entry(control_frame, font=("Arial", 12))
    url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

    # ----- Fila 2: Botones de descarga -----
    button_frame = tb.Frame(control_frame)
    button_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
    
    tb.Button(button_frame, text="📹 Descargar Video", command=lambda: download_video(url_entry.get(), download_folder, file_tree, folder_label), bootstyle=PRIMARY).pack(side="left", padx=5)
    tb.Button(button_frame, text="🎵 Descargar Audio", command=lambda: download_audio(url_entry.get(), download_folder, file_tree, folder_label), bootstyle=SUCCESS).pack(side="left", padx=5)

    # ----- Fila 3: Controles de carpeta -----
    folder_frame = tb.Frame(control_frame)
    folder_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)
    
    tb.Button(folder_frame, text="⬅️ Atrás", command=lambda: go_to_parent(download_folder, file_tree, folder_label), bootstyle=DANGER).pack(side="left", padx=5)
    tb.Button(folder_frame, text="📂 Seleccionar Carpeta", command=lambda: select_download_folder(file_tree, folder_label), bootstyle=INFO).pack(side="left", padx=5)

    folder_label = tb.Label(control_frame, text=f"📂 Carpeta: {download_folder}", font=("Arial", 11, "italic"))
    folder_label.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

    # ========== Explorador de Archivos ==========
    file_tree = tb.Treeview(root, columns=("Tipo", "Fecha"), show="tree headings")
    file_tree.heading("#0", text="Nombre", anchor="w")
    file_tree.heading("Tipo", text="Tipo", anchor="w")
    file_tree.heading("Fecha", text="Fecha de creación", anchor="w")
    file_tree.column("#0", stretch=True)
    file_tree.column("Tipo", width=100, anchor="center")
    file_tree.column("Fecha", width=150, anchor="center")

    file_tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # Permitir que el árbol de archivos se expanda correctamente
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # ===== Vincular evento de doble clic =====
    file_tree.bind("<Double-1>", lambda event: on_item_double_click(event, file_tree, folder_label))

    return {"file_tree": file_tree, "folder_label": folder_label, "url_entry": url_entry}
