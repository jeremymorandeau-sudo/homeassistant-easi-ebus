# Guide de publication sur GitHub

## Étapes pour publier votre addon sur GitHub

### 1. Créer un compte GitHub (si nécessaire)
- Allez sur https://github.com
- Cliquez sur "Sign up"
- Suivez les instructions

### 2. Créer un nouveau dépôt

1. Connectez-vous à GitHub
2. Cliquez sur le **+** en haut à droite → **New repository**
3. Remplissez les informations :
   - **Repository name** : `homeassistant-easi-ebus` (ou autre nom)
   - **Description** : "Home Assistant addon pour systèmes easi> eBUS"
   - **Public** ou **Private** : Choisissez (Public recommandé)
   - ❌ Ne cochez PAS "Initialize this repository with a README"
4. Cliquez sur **Create repository**

### 3. Configurer Git localement

Ouvrez un terminal et allez dans le dossier du projet :

```bash
cd homeassistant-easi-ebus
```

Configurez votre identité Git (si première fois) :

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### 4. Initialiser et envoyer le dépôt

```bash
# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - easi> eBUS Integration v1.0.0"

# Lier au dépôt GitHub (remplacez VOTRE_USERNAME par votre nom d'utilisateur)
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus.git

# Envoyer sur GitHub
git push -u origin main
```

### 5. Personnaliser le dépôt

Une fois le code envoyé, personnalisez les fichiers suivants :

#### repository.json
Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub

#### README.md
Remplacez :
- `VOTRE_USERNAME` par votre nom d'utilisateur GitHub
- Les liens des badges
- Votre nom et email dans le maintainer

#### config.yaml (dans easi_ebus/)
Remplacez l'URL dans le fichier

### 6. Créer une release (version)

1. Allez sur votre dépôt GitHub
2. Cliquez sur **Releases** → **Create a new release**
3. Cliquez sur **Choose a tag** → Tapez `v1.0.0` → **Create new tag**
4. **Release title** : `v1.0.0 - Initial Release`
5. **Description** : Copiez le contenu du CHANGELOG.md
6. Cliquez sur **Publish release**

### 7. Tester l'installation

Dans Home Assistant :
1. Allez dans **Paramètres** → **Modules complémentaires** → **Boutique**
2. **⋮** → **Dépôts**
3. Ajoutez : `https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus`
4. Recherchez votre addon
5. Installez-le et testez

### 8. (Optionnel) Ajouter des images

Pour améliorer la présentation :

1. Créez un dossier `images/` dans votre dépôt
2. Ajoutez des captures d'écran :
   - `logo.png` : Logo de votre addon
   - `screenshot-dashboard.png` : Capture du dashboard
   - `screenshot-config.png` : Capture de la configuration
3. Mettez à jour les liens dans le README.md

```bash
mkdir images
# Copiez vos images dans ce dossier
git add images/
git commit -m "Add screenshots"
git push
```

### 9. (Optionnel) GitHub Actions

Les GitHub Actions sont déjà configurées dans `.github/workflows/builder.yml`

Pour les activer :
1. Allez dans **Settings** → **Actions** → **General**
2. Autorisez les actions

### 10. Partager votre addon

Une fois publié, vous pouvez :
- Partager le lien sur le forum Home Assistant
- Le soumettre à HACS (Home Assistant Community Store)
- Le partager sur Reddit (r/homeassistant)

## Commandes Git utiles

```bash
# Voir le statut
git status

# Ajouter des modifications
git add .

# Commit
git commit -m "Description des changements"

# Envoyer sur GitHub
git push

# Créer une nouvelle branche
git checkout -b nouvelle-fonctionnalite

# Revenir à main
git checkout main

# Mettre à jour depuis GitHub
git pull
```

## Mise à jour de version

Pour publier une nouvelle version :

1. Modifiez les fichiers nécessaires
2. Mettez à jour `CHANGELOG.md`
3. Mettez à jour le numéro de version dans `config.yaml`
4. Commitez et pushez :
```bash
git add .
git commit -m "Version 1.1.0 - Nouvelles fonctionnalités"
git push
```
5. Créez une nouvelle release sur GitHub avec le tag `v1.1.0`

## Dépannage

### Erreur d'authentification
Si vous avez une erreur lors du push, GitHub nécessite maintenant un token :
1. Allez sur GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **Generate new token**
3. Donnez les permissions `repo`
4. Utilisez ce token comme mot de passe lors du push

### Le dépôt existe déjà
Si vous obtenez une erreur "repository already exists" :
```bash
git remote set-url origin https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus.git
```

## Ressources

- [Documentation Git](https://git-scm.com/doc)
- [Guide GitHub](https://guides.github.com/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/docs/add-ons)

Bon courage ! 🚀
