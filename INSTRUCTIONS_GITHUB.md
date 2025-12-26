# 📋 INSTRUCTIONS GITHUB - APK Android

## 🎯 Ce Qu'on Va Faire

1. Créer la structure de dossiers dans GitHub
2. Uploader les fichiers nécessaires
3. GitHub compile automatiquement l'APK
4. Télécharger l'APK compilé

**Durée totale : ~15 min pour vous + 20 min compilation GitHub**

---

## 📁 ÉTAPE 1 : Créer la Structure de Dossiers

Dans votre repo GitHub `remote-control-v1.2` :

1. **Créer le dossier `.github/workflows/`** :
   - Cliquer "Add file" → "Create new file"
   - Taper : `.github/workflows/build-apk.yml`
   - GitHub créera automatiquement les dossiers

2. **Copier le contenu du fichier `build-apk.yml`** que je vous ai préparé

---

## 📤 ÉTAPE 2 : Uploader les Fichiers

### Fichiers à uploader (dans l'ordre) :

1. **`.github/workflows/build-apk.yml`** ← Workflow de compilation
2. **`buildozer.spec`** ← Configuration Android
3. **`remote_control_client_v1.2.py`** ← Code source client
4. **`README.md`** ← Documentation

---

## 🚀 ÉTAPE 3 : Lancer la Compilation

Une fois tous les fichiers uploadés :

1. Aller dans l'onglet **"Actions"** de votre repo
2. Vous devriez voir "Build Android APK" qui se lance automatiquement
3. Attendre ~20 minutes (première compilation)
4. La compilation apparaîtra en vert ✅ quand terminée

---

## 📥 ÉTAPE 4 : Télécharger l'APK

Quand la compilation est terminée :

1. Aller dans **"Actions"**
2. Cliquer sur la compilation réussie (✅)
3. Descendre jusqu'à **"Artifacts"**
4. Télécharger **"remote-control-apk"**
5. Extraire le ZIP → Vous avez votre APK !

---

## 📱 ÉTAPE 5 : Installer sur Android

### Méthode 1 : Via ADB (téléphone connecté en USB)
```powershell
adb install remotecontrol-1.2-armeabi-v7a-debug.apk
```

### Méthode 2 : Transfert manuel
1. Copier l'APK sur le téléphone (USB ou email)
2. Sur Android : Paramètres → Sécurité → Activer "Sources inconnues"
3. Taper sur le fichier APK pour installer

---

## 🔍 Dépannage

### "Actions" n'apparaît pas
- Le repo doit être **public** pour GitHub Actions gratuit
- OU avoir un compte GitHub Pro

### La compilation échoue
- Vérifier que tous les fichiers sont bien uploadés
- Vérifier que `remote_control_client_v1.2.py` est bien à la racine
- Regarder les logs dans "Actions" pour voir l'erreur exacte

### L'APK ne s'installe pas
- Vérifier "Sources inconnues" activées sur Android
- L'APK est signé en mode "debug" (normal pour développement)

---

## ✅ Checklist

- [ ] Créer `.github/workflows/build-apk.yml`
- [ ] Uploader `buildozer.spec`
- [ ] Uploader `remote_control_client_v1.2.py`
- [ ] Uploader `README.md`
- [ ] Vérifier dans "Actions" que la compilation se lance
- [ ] Attendre ~20 minutes
- [ ] Télécharger l'APK depuis "Artifacts"
- [ ] Installer sur Android
- [ ] Tester !

---

**Prêt ? Commençons avec l'étape 1 ! 🚀**
