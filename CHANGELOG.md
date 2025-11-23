# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### À venir
- Support de l'écriture de valeurs eBUS
- Interface de configuration web intégrée
- Support des commandes eBUS
- Dashboard intégré

## [1.0.0] - 2025-11-23

### Ajouté
- Version initiale de l'addon
- Connexion à micro-ebusd via API REST
- Auto-discovery MQTT pour Home Assistant
- Configuration flexible des entités
- Support de tous les circuits eBUS (heating, hotwater, controller)
- Gestion des unités et device_class
- Logs détaillés pour le débogage
- Documentation complète en français
- Support multi-architecture (aarch64, amd64, armhf, armv7, i386)

### Fonctionnalités
- Récupération automatique des données eBUS
- Mise à jour configurable (scan_interval)
- Attributs détaillés pour chaque entité
- Reconnexion automatique en cas de perte de connexion
- Gestion d'erreurs robuste

## Format de version

Le numéro de version suit le format MAJOR.MINOR.PATCH :
- MAJOR : Changements incompatibles avec les versions précédentes
- MINOR : Nouvelles fonctionnalités compatibles avec les versions précédentes
- PATCH : Corrections de bugs compatibles avec les versions précédentes

[Non publié]: https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/releases/tag/v1.0.0
