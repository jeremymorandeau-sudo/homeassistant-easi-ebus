# Home Assistant easi> eBUS Integration

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

![Project Maintenance][maintenance-shield]

_Integration Home Assistant pour les systèmes de chauffage easi> avec micro-ebusd._

**Cet addon permet de connecter votre système easi> eBUS à Home Assistant et de récupérer toutes les données de votre installation de chauffage.**

![easi> Logo](https://raw.githubusercontent.com/VOTRE_USERNAME/homeassistant-easi-ebus/main/images/logo.png)

## À propos

easi> est un système de contrôle intelligent pour les installations de chauffage utilisant le protocole eBUS. Cet addon permet d'intégrer votre dispositif easi> (équipé de micro-ebusd) directement dans Home Assistant.

### Fonctionnalités

- 🌡️ **Surveillance en temps réel** de toutes les températures (départ, retour, ECS, ambiante, extérieure)
- 📊 **Monitoring** de la pression, puissance, débit
- 🔄 **Auto-discovery** automatique dans Home Assistant via MQTT
- ⚙️ **Configuration flexible** : choisissez exactement les données que vous voulez
- 📈 **Historique** : toutes les données sont enregistrées pour analyse
- 🤖 **Automatisations** : créez des alertes et automatisations basées sur vos données eBUS
- 🚀 **Léger et performant** : mise à jour configurable, faible consommation de ressources

## Installation

### Méthode 1 : Ajout du dépôt (Recommandé)

1. Cliquez sur le bouton ci-dessous pour ajouter ce dépôt à Home Assistant :

   [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FVOTRE_USERNAME%2Fhomeassistant-easi-ebus)

2. Ou manuellement :
   - Allez dans **Paramètres** → **Modules complémentaires** → **Boutique des modules complémentaires**
   - Cliquez sur les **⋮** (trois points) en haut à droite
   - Sélectionnez **Dépôts**
   - Ajoutez cette URL :
     ```
     https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus
     ```

3. Recherchez "easi> eBUS Integration" dans la boutique
4. Cliquez sur **INSTALLER**

### Méthode 2 : Installation manuelle

1. Copiez le dossier `easi_ebus` dans `/addons/`
2. Rechargez la liste des addons
3. Installez "easi> eBUS Integration"

## Prérequis

Avant d'utiliser cet addon, assurez-vous d'avoir :

- ✅ Home Assistant installé et opérationnel
- ✅ Addon **Mosquitto broker** (MQTT) installé et démarré
- ✅ Un dispositif **easi>** avec **micro-ebusd** actif
- ✅ Votre dispositif easi> accessible sur votre réseau local

## Configuration

### Configuration minimale

```yaml
ebusd_host: "192.168.0.26"  # IP de votre dispositif easi>
ebusd_port: 8080
scan_interval: 30
entities:
  - name: "Température départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
```

### Configuration complète

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30

entities:
  # Circuit de chauffage
  - name: "Température départ chaudière"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  
  - name: "Température retour chaudière"
    circuit: "heating"
    message: "ReturnTemp"
    unit: "°C"
    device_class: "temperature"
  
  - name: "Pression circuit"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
  
  # Eau chaude sanitaire
  - name: "Température ECS"
    circuit: "hotwater"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  
  # Contrôleur
  - name: "Température extérieure"
    circuit: "controller"
    message: "OutdoorTemp"
    unit: "°C"
    device_class: "temperature"
```

### Découverte des messages disponibles

Pour connaître les circuits et messages disponibles sur votre installation :

```bash
# Liste tous les circuits
curl http://192.168.0.26:8080/data

# Messages du circuit heating
curl http://192.168.0.26:8080/data/heating

# Valeur d'un message spécifique
curl http://192.168.0.26:8080/data/heating/Temp
```

Ou consultez l'interface web de votre easi> : `http://192.168.0.26`

## Utilisation

### Dans Home Assistant

Les entités seront automatiquement créées avec le préfixe `sensor.ebus_` :
- `sensor.ebus_temperature_depart_chaudiere`
- `sensor.ebus_temperature_retour_chaudiere`
- `sensor.ebus_pression_circuit`
- etc.

### Carte Lovelace

```yaml
type: entities
title: Chauffage eBUS
entities:
  - entity: sensor.ebus_temperature_depart_chaudiere
  - entity: sensor.ebus_temperature_retour_chaudiere
  - entity: sensor.ebus_pression_circuit
```

### Automatisation

```yaml
automation:
  - alias: "Alerte pression basse"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ebus_pression_circuit
        below: 1.0
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Alerte chauffage"
          message: "Pression basse détectée"
```

## Screenshots

![Dashboard](images/screenshot-dashboard.png)
![Configuration](images/screenshot-config.png)

## Support

- 📖 [Documentation complète](easi_ebus/DOCS.md)
- 🐛 [Signaler un bug](https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/issues)
- 💬 [Discussions](https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/discussions)

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des nouvelles fonctionnalités
- 🔧 Soumettre des pull requests

## Compatibilité

| Dispositif | Status |
|------------|--------|
| easi> avec micro-ebusd | ✅ Testé |
| ebusd standalone | ⚠️ Non testé (devrait fonctionner) |

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- [john30/ebusd](https://github.com/john30/ebusd) - Le daemon eBUS
- [easi>](https://easi.link/) - Le système de contrôle intelligent
- La communauté Home Assistant

---

Made with ❤️ for the Home Assistant community

[releases-shield]: https://img.shields.io/github/release/VOTRE_USERNAME/homeassistant-easi-ebus.svg
[releases]: https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/releases
[license-shield]: https://img.shields.io/github/license/VOTRE_USERNAME/homeassistant-easi-ebus.svg
[maintenance-shield]: https://img.shields.io/badge/maintainer-Votre%20Nom-blue.svg
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
