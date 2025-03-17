import os
import subprocess
import threading
import tkinter.messagebox as messagebox

def download_media(media_type, format_ext, extra_params, url, download_folder, file_tree, folder_label, root):
    if not url:
        messagebox.showerror("Error", "Por favor ingresa la URL de YouTube.")
        return

    def download():
        try:
            command = [
                'yt-dlp', '-o', os.path.join(download_folder, '%(title)s.' + format_ext),
                *extra_params, url
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            for stdout_line in iter(process.stdout.readline, ""):
                print(stdout_line, end="")
                # Capturar el progreso del porcentaje
                if "[download]" in stdout_line and "%" in stdout_line:
                    percentage = extract_percentage(stdout_line)
                    if percentage:
                        root.title(f"Media Downloader - Progreso: {percentage}")
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Éxito", f"El {media_type} se ha descargado exitosamente en formato {format_ext.upper()}.")
                from explorer import populate_tree
                populate_tree(download_folder, file_tree, folder_label)
            else:
                messagebox.showerror("Error", f"Hubo un error al descargar el {media_type}.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            root.title("Media Downloader")  # Restaurar el título original

    def extract_percentage(line):
        """Extraer el porcentaje de una línea de progreso."""
        try:
            # Buscar el porcentaje en la línea de progreso
            parts = line.split()
            for part in parts:
                if "%" in part and part.replace("%", "").replace(".", "").isdigit():
                    return part.strip()
        except Exception:
            pass
        return None

    threading.Thread(target=download, daemon=True).start()

def download_video(url, download_folder, file_tree, folder_label, root):
    download_media("video", "mp4", ['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'], url, download_folder, file_tree, folder_label, root)

def download_audio(url, download_folder, file_tree, folder_label, root):
    download_media("audio", "mp3", ['-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3'], url, download_folder, file_tree, folder_label, root)