import os
import subprocess
import threading
import tkinter.messagebox as messagebox

def download_media(media_type, format_ext, extra_params, url, download_folder, file_tree, folder_label):
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
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Éxito", f"El {media_type} se ha descargado exitosamente en formato {format_ext.upper()}.")
                from explorer import populate_tree
                populate_tree(download_folder, file_tree, folder_label)
            else:
                messagebox.showerror("Error", f"Hubo un error al descargar el {media_type}.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    threading.Thread(target=download, daemon=True).start()

def download_video(url, download_folder, file_tree, folder_label):
    download_media("video", "mp4", ['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'], url, download_folder, file_tree, folder_label)

def download_audio(url, download_folder, file_tree, folder_label):
    download_media("audio", "mp3", ['-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3'], url, download_folder, file_tree, folder_label)
