import tkinter as tk
from tkinter import ttk, filedialog
import os
import subprocess
import json
from datetime import datetime
import shutil
import sys
import time
from PIL import Image, ImageTk

def show_error_and_exit(message):
    """Affiche une erreur et quitte l'application"""
    print(f"Erreur fatale: {message}")
    try:
        import tkinter.messagebox as mb
        mb.showerror("Erreur fatale", message)
    except:
        pass
    sys.exit(1)

class PalworldServerManager:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Palworld Server Manager")
            
            # Configuration de l'icône
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "icon-256.png")
            if os.path.exists(icon_path):
                icon = ImageTk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
            
            # Configuration des couleurs
            self.colors = {
                'bg': '#2E2E2E',
                'fg': '#FFFFFF',
                'button': '#3E3E3E',
                'button_hover': '#4E4E4E',
                'success': '#28A745',
                'error': '#DC3545',
                'warning': '#FFC107'
            }
            
            # Configuration de base
            self.server_path = ""
            self.path_var = tk.StringVar()
            self.process = None
            
            # Configuration des backups
            self.backup_path = os.path.expanduser("~/palworld_backups")
            if not os.path.exists(self.backup_path):
                os.makedirs(self.backup_path)
            
            # Configuration de la fenêtre principale
            self.root.configure(bg=self.colors['bg'])
            self.root.geometry("800x600")
            self.root.minsize(800, 600)
            
            # Configuration du style
            self.setup_style()
            
            # Configuration de l'interface
            self.setup_ui()
            
            # Recherche initiale du serveur
            self.find_server_installation()
            
        except Exception as e:
            show_error_and_exit(f"Erreur lors de l'initialisation:\n{str(e)}")
    
    def _get_icon_path(self):
        """Récupère le chemin de l'icône"""
        try:
            # Essayer d'abord le chemin relatif
            icon_path = "Icon_256.png"
            if os.path.exists(icon_path):
                return icon_path
            
            # Essayer le chemin du script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "Icon_256.png")
            if os.path.exists(icon_path):
                return icon_path
            
            return None
        except Exception as e:
            print(f"Erreur lors de la recherche de l'icône: {e}")
            return None
    
    def setup_style(self):
        try:
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configuration des styles
            style.configure("TFrame", background=self.colors['bg'])
            style.configure("TLabel",
                          background=self.colors['bg'],
                          foreground=self.colors['fg'])
            style.configure("TButton",
                          padding=10,
                          background=self.colors['button'],
                          foreground=self.colors['fg'])
            style.configure("TEntry",
                          fieldbackground=self.colors['button'],
                          foreground=self.colors['fg'])
            
        except Exception as e:
            show_error_and_exit(f"Erreur lors de la configuration du style:\n{str(e)}")
    
    def setup_ui(self):
        try:
            # Frame principal
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.grid(row=0, column=0, sticky="nsew")
            
            # Configuration du grid principal
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            
            # Frame pour le chemin du serveur
            path_frame = ttk.Frame(main_frame)
            path_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
            
            path_label = ttk.Label(path_frame, text="📁 Chemin du serveur")
            path_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
            
            path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
            path_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
            
            browse_button = ttk.Button(path_frame, text="📂 Parcourir", command=self.browse_path)
            browse_button.grid(row=0, column=2, sticky="e")
            
            # Frame pour les boutons
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
            
            # Boutons
            buttons = [
                ("💾 Installer", self.install_server),
                ("▶️ Démarrer", self.start_server),
                ("⏹️ Arrêter", self.stop_server),
                ("🔄 Mettre à jour", self.update_server),
                ("💾 Sauvegarder", self.backup_server),
                ("📁 Ouvrir", self.open_server_folder)
            ]
            
            for i, (text, command) in enumerate(buttons):
                btn = ttk.Button(button_frame, text=text, command=command)
                btn.grid(row=0, column=i, sticky="ew", padx=5)
                
                if text == "▶️ Démarrer":
                    self.start_button = btn
                elif text == "⏹️ Arrêter":
                    self.stop_button = btn
                elif text == "🔄 Mettre à jour":
                    self.update_button = btn
                elif text == "💾 Installer":
                    self.install_button = btn
            
            # Configuration du grid pour les boutons
            for i in range(len(buttons)):
                button_frame.grid_columnconfigure(i, weight=1)
            
            # Zone de logs
            log_frame = ttk.Frame(main_frame)
            log_frame.grid(row=2, column=0, sticky="nsew")
            main_frame.grid_rowconfigure(2, weight=1)
            
            self.log_text = tk.Text(log_frame, wrap=tk.WORD, bg='#1E1E1E', fg='#FFFFFF')
            self.log_text.grid(row=0, column=0, sticky="nsew")
            
            scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            
            self.log_text.configure(yscrollcommand=scrollbar.set)
            
            # Configuration des grids
            path_frame.grid_columnconfigure(1, weight=1)
            log_frame.grid_columnconfigure(0, weight=1)
            log_frame.grid_rowconfigure(0, weight=1)
            
        except Exception as e:
            show_error_and_exit(f"Erreur lors de la création de l'interface:\n{str(e)}")
    
    def log(self, message):
        """Ajoute un message dans la zone de log"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
        except Exception as e:
            print(f"Erreur lors de l'ajout du log: {e}")
    
    def browse_path(self):
        """Ouvre une boîte de dialogue pour sélectionner le dossier"""
        try:
            path = filedialog.askdirectory()
            if path:
                self.server_path = path
                self.path_var.set(path)
        except Exception as e:
            self.log(f"Erreur lors de la sélection du dossier: {e}")
    
    def install_server(self):
        self.log("Installation du serveur...")
        # TODO: Implémenter l'installation
    
    def start_server(self):
        """Démarre le serveur Palworld"""
        try:
            if not self.server_path:
                self.log("❌ Erreur: Aucun serveur sélectionné")
                return
            
            # Nettoyer les anciennes instances
            self.cleanup_old_servers()
            
            server_script = os.path.join(self.server_path, "PalServer.sh")
            if not os.path.exists(server_script):
                self.log("❌ Erreur: PalServer.sh non trouvé")
                return
            
            # Rendre le script exécutable
            os.chmod(server_script, 0o755)
            
            # Vérifier si le serveur est déjà en cours d'exécution
            if hasattr(self, 'server_process') and self.server_process and self.server_process.poll() is None:
                self.log("⚠️ Le serveur est déjà en cours d'exécution")
                return
            
            self.log("🚀 Démarrage du serveur...")
            
            # Démarrer le serveur avec les bons paramètres
            env = os.environ.copy()
            env["LD_LIBRARY_PATH"] = os.path.join(self.server_path, "linux64")
            env["SteamAppId"] = "2394010"  # ID Steam de Palworld
            
            # Paramètres de démarrage du serveur
            server_params = [
                server_script,
                "-port=8211",  # Port du jeu
                "-queryport=27015",  # Port de requête Steam
                "-RCONEnabled=True",
                "-RCONPort=25575"  # Port RCON
            ]
            
            self.server_process = subprocess.Popen(
                server_params,
                cwd=self.server_path,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Mettre à jour l'interface
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # Lire la sortie du serveur dans un thread séparé
            def read_output():
                while True:
                    if not hasattr(self, 'server_process') or self.server_process.poll() is not None:
                        break
                    
                    line = self.server_process.stdout.readline()
                    if line:
                        self.log(f"🖥️ {line.strip()}")
                    
                    error = self.server_process.stderr.readline()
                    if error:
                        self.log(f"⚠️ {error.strip()}")
            
            import threading
            self.output_thread = threading.Thread(target=read_output, daemon=True)
            self.output_thread.start()
            
            # Vérifier périodiquement l'état du serveur
            def check_server():
                if hasattr(self, 'server_process'):
                    if self.server_process.poll() is not None:
                        self.log("⚠️ Le serveur s'est arrêté")
                        self.start_button.configure(state="normal")
                        self.stop_button.configure(state="disabled")
                    else:
                        self.root.after(5000, check_server)
            
            self.root.after(5000, check_server)
            
        except Exception as e:
            self.log(f"❌ Erreur lors du démarrage du serveur: {str(e)}")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
    
    def stop_server(self):
        """Arrête le serveur Palworld"""
        try:
            if not hasattr(self, 'server_process') or self.server_process.poll() is not None:
                self.log("ℹ️ Le serveur n'est pas en cours d'exécution")
                return
            
            self.log("🛑 Arrêt du serveur...")
            
            # Envoyer SIGTERM au processus
            self.server_process.terminate()
            
            try:
                # Attendre que le processus se termine
                self.server_process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                # Si le processus ne se termine pas, le tuer
                self.log("⚠️ Le serveur ne répond pas, arrêt forcé...")
                self.server_process.kill()
            
            self.log("✅ Serveur arrêté")
            
            # Mettre à jour l'interface
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            
        except Exception as e:
            self.log(f"❌ Erreur lors de l'arrêt du serveur: {str(e)}")
    
    def update_server(self):
        self.log("Mise à jour du serveur...")
        # TODO: Implémenter la mise à jour
    
    def backup_server(self):
        """Crée une sauvegarde du serveur"""
        try:
            if not self.server_path:
                self.log("❌ Erreur: Aucun serveur sélectionné")
                return
            
            save_dir = os.path.join(self.server_path, "Pal/Saved")
            if not os.path.exists(save_dir):
                self.log("❌ Erreur: Dossier de sauvegarde non trouvé")
                return
            
            # Créer un nom de fichier avec la date
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"palworld_backup_{timestamp}"
            backup_path = os.path.join(self.backup_path, backup_name)
            
            # Créer la sauvegarde
            self.log(f"📦 Création de la sauvegarde...")
            shutil.make_archive(backup_path, 'zip', save_dir)
            
            self.log(f"✅ Sauvegarde créée: {backup_path}.zip")
            
            # Ouvrir le dossier des backups
            subprocess.run(["xdg-open", self.backup_path])
            
        except Exception as e:
            self.log(f"❌ Erreur lors de la sauvegarde: {str(e)}")
    
    def open_server_folder(self):
        """Ouvre le dossier du serveur dans l'explorateur de fichiers"""
        try:
            if not self.server_path:
                self.log("❌ Erreur: Aucun serveur sélectionné")
                return
            
            if not os.path.exists(self.server_path):
                self.log("❌ Erreur: Le dossier n'existe pas")
                return
            
            subprocess.run(["xdg-open", self.server_path])
            self.log(f"✅ Ouverture du dossier: {self.server_path}")
            
        except Exception as e:
            self.log(f"❌ Erreur lors de l'ouverture du dossier: {str(e)}")
    
    def find_server_installation(self):
        """Recherche l'installation du serveur"""
        try:
            common_paths = [
                os.path.expanduser("~/palworld"),
                os.path.expanduser("~/Palworld"),
                os.path.expanduser("~/Steam/steamapps/common/PalServer"),
                os.path.expanduser("~/.steam/steam/steamapps/common/PalServer")
            ]
            
            for path in common_paths:
                if os.path.exists(os.path.join(path, "PalServer.sh")):
                    self.server_path = path
                    self.path_var.set(path)
                    self.log(f"✅ Serveur trouvé: {path}")
                    return True
            
            self.log("❌ Aucune installation trouvée")
            return False
            
        except Exception as e:
            self.log(f"Erreur lors de la recherche du serveur: {e}")
            return False
    
    def cleanup_old_servers(self):
        """Nettoie les anciennes instances du serveur"""
        try:
            # Chercher tous les processus PalServer.sh
            self.log("🧹 Nettoyage des anciennes instances...")
            subprocess.run(["pkill", "-f", "PalServer.sh"], check=False)
            time.sleep(2)  # Attendre que les processus se terminent
        except Exception as e:
            self.log(f"⚠️ Erreur lors du nettoyage: {str(e)}")

def main():
    try:
        app = PalworldServerManager()
        app.root.mainloop()
    except Exception as e:
        show_error_and_exit(f"Erreur fatale:\n{str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_error_and_exit(f"Erreur lors du démarrage: {str(e)}")
