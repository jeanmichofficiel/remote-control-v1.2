# 🖱️ Remote Control v1.2 - FINAL

**Contrôle souris/clavier à distance via WiFi local**  
100% Local - Aucun serveur externe - Aucune connexion internet requise

---

## 📦 Téléchargements

### Serveur Windows (.exe)
- **RemoteControlServer.exe** - Exécutable autonome pour Windows
- Aucune installation Python requise
- Double-cliquez pour lancer

### Client Android (.apk)
- **remotecontrol-1.2-debug.apk** - Application Android native
- Installation : Paramètres → Sécurité → Sources inconnues
- Puis installer l'APK

---

## 🚀 Utilisation

### Serveur (PC)
1. Lancer `RemoteControlServer.exe`
2. Autoriser dans le pare-feu si demandé
3. Noter l'IP affichée (ex: 192.168.1.100)

### Client (Android/PC)
1. Lancer l'application
2. Le serveur devrait apparaître automatiquement
3. Cliquer pour se connecter
4. Utiliser le touchpad virtuel !

---

## ✨ Fonctionnalités

- ✅ Contrôle souris (déplacement, clics)
- ✅ Contrôle clavier (saisie texte)
- ✅ Touches spéciales (Enter, Backspace, etc.)
- ✅ Auto-découverte réseau (mDNS)
- ✅ Reconnexion automatique
- ✅ 100% local (aucun serveur externe)

---

## 🔧 Compilation

### APK Android
Les APK sont compilés automatiquement via GitHub Actions.

Pour compiler manuellement :
```bash
# Linux avec Python 3.11
pip install buildozer cython
buildozer android debug
```

### EXE Windows
```powershell
pip install pyinstaller
pyinstaller --onefile --name "RemoteControlServer" remote_control_server_v1.2.py
```

---

## 📝 Version

**v1.2 - Version Finale**
- Bug clics souris corrigé
- Auto-reconnexion implémentée
- Interface graphique complète
- 100% fonctionnel

---

## 📄 Licence

MIT License - Utilisation libre

---

**Joyeux contrôle à distance ! 🎮**
