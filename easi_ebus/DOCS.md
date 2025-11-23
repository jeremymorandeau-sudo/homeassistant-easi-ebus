# Documentation - easi> eBUS Integration

## Table des matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Utilisation](#utilisation)
5. [Dépannage](#dépannage)
6. [API eBUS](#api-ebus)

## Introduction

Cet addon permet d'intégrer votre système de chauffage easi> (équipé de micro-ebusd) dans Home Assistant. Il récupère automatiquement toutes les données de votre installation via le protocole eBUS et les rend disponibles dans Home Assistant.

### Qu'est-ce que eBUS ?

eBUS (Energy Bus) est un protocole de communication utilisé par de nombreux systèmes de chauffage européens (Vaillant, Buderus, Junkers, etc.). Il permet de lire et contrôler divers paramètres du système de chauffage.

### Qu'est-ce que easi> ?

easi> est un contrôleur intelligent basé sur ESP32 qui se connecte au bus eBUS de votre chaudière et expose les données via une API web grâce à micro-ebusd.

## Installation

### Prérequis

Avant d'installer cet addon, assurez-vous d'avoir :

1. **Home Assistant** version 2023.1 ou supérieure
2. **Mosquitto broker** (addon MQTT) installé et démarré
3. Un dispositif **easi>** avec **micro-ebusd actif**
4. Votre dispositif easi> accessible sur votre réseau local

### Installation du dépôt

1. Ajoutez ce dépôt à Home Assistant :
   ```
   https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus
   ```

2. Recherchez "easi> eBUS Integration" dans la boutique des addons

3. Cliquez sur "Installer"

## Configuration

### Paramètres de base

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `ebusd_host` | string | 192.168.0.26 | Adresse IP de votre dispositif easi> |
| `ebusd_port` | int | 8080 | Port de l'API micro-ebusd |
| `scan_interval` | int | 30 | Intervalle de mise à jour en secondes (10-300) |

### Configuration des entités

Chaque entité est définie par :

| Paramètre | Requis | Type | Description |
|-----------|--------|------|-------------|
| `name` | ✅ | string | Nom de l'entité dans Home Assistant |
| `circuit` | ✅ | string | Circuit eBUS (ex: heating, hotwater) |
| `message` | ✅ | string | Message eBUS à récupérer |
| `unit` | ❌ | string | Unité de mesure (°C, bar, %, etc.) |
| `device_class` | ❌ | string | Classe Home Assistant (temperature, pressure, etc.) |

### Exemple de configuration

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30

entities:
  # Températures
  - name: "Température départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  
  - name: "Température retour"
    circuit: "heating"
    message: "ReturnTemp"
    unit: "°C"
    device_class: "temperature"
  
  - name: "Température ECS"
    circuit: "hotwater"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  
  # Pression
  - name: "Pression circuit"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
  
  # États
  - name: "État chaudière"
    circuit: "heating"
    message: "Status"
  
  # Puissance
  - name: "Puissance pompe"
    circuit: "heating"
    message: "PumpPower"
    unit: "%"
```

## Utilisation

### Découverte des circuits et messages

Pour découvrir quels circuits et messages sont disponibles :

#### Méthode 1 : Interface web

1. Ouvrez votre navigateur
2. Allez sur `http://[IP_EASI]:8080` (ex: http://192.168.0.26:8080)
3. Consultez l'onglet "Messages"

#### Méthode 2 : API REST

```bash
# Liste tous les circuits disponibles
curl http://192.168.0.26:8080/data

# Liste les messages d'un circuit
curl http://192.168.0.26:8080/data/heating

# Récupère la valeur d'un message spécifique
curl http://192.168.0.26:8080/data/heating/Temp
```

### Circuits courants

#### heating (chauffage)
- `Temp` - Température de départ
- `ReturnTemp` - Température de retour
- `FlowTemp` - Température d'eau
- `Pressure` - Pression du circuit
- `Status` - État du système
- `PumpPower` - Puissance de la pompe (%)
- `ModulationTemp` - Température de modulation
- `BurnerStatus` - État du brûleur

#### hotwater (eau chaude sanitaire)
- `Temp` - Température ECS
- `TempDesired` - Température souhaitée
- `Flow` - Débit d'eau
- `Status` - État ECS

#### controller (contrôleur)
- `RoomTemp` - Température ambiante
- `OutdoorTemp` - Température extérieure
- `HolidayMode` - Mode vacances
- `OperatingMode` - Mode de fonctionnement

### Dans Home Assistant

#### Entités créées

Les entités sont automatiquement créées avec le préfixe `sensor.ebus_` :

```
sensor.ebus_temperature_depart
sensor.ebus_temperature_retour
sensor.ebus_temperature_ecs
sensor.ebus_pression_circuit
sensor.ebus_etat_chaudiere
```

#### Cartes Lovelace

**Carte simple :**
```yaml
type: entities
title: Chauffage
entities:
  - sensor.ebus_temperature_depart
  - sensor.ebus_temperature_retour
  - sensor.ebus_pression_circuit
```

**Carte avec gauges :**
```yaml
type: horizontal-stack
cards:
  - type: gauge
    entity: sensor.ebus_temperature_depart
    min: 0
    max: 90
    name: Départ
    severity:
      green: 0
      yellow: 70
      red: 80
  
  - type: gauge
    entity: sensor.ebus_pression_circuit
    min: 0
    max: 3
    name: Pression
    severity:
      green: 1
      yellow: 0.8
      red: 0.5
```

**Graphique historique :**
```yaml
type: history-graph
entities:
  - sensor.ebus_temperature_depart
  - sensor.ebus_temperature_retour
  - sensor.ebus_temperature_exterieure
hours_to_show: 24
title: Températures 24h
```

#### Automatisations

**Alerte pression basse :**
```yaml
automation:
  - alias: "Alerte pression basse chauffage"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ebus_pression_circuit
        below: 1.0
        for:
          minutes: 5
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Chauffage"
          message: "Pression basse: {{ states('sensor.ebus_pression_circuit') }} bar"
          data:
            priority: high
```

**Alerte température élevée :**
```yaml
automation:
  - alias: "Alerte température élevée"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ebus_temperature_depart
        above: 80
    action:
      - service: notify.mobile_app
        data:
          title: "🔥 Alerte température"
          message: "Température départ: {{ states('sensor.ebus_temperature_depart') }}°C"
```

**Surveillance arrêt chaudière :**
```yaml
automation:
  - alias: "Notification arrêt chaudière"
    trigger:
      - platform: state
        entity_id: sensor.ebus_etat_chaudiere
        to: "off"
    action:
      - service: notify.mobile_app
        data:
          title: "ℹ️ Chauffage"
          message: "La chaudière s'est arrêtée"
```

## Dépannage

### Problèmes de connexion eBUS

**Symptôme :** "Impossible de se connecter à ebusd"

**Solutions :**
1. Vérifiez que votre dispositif easi> est allumé et connecté au réseau
2. Testez la connexion : `ping [IP_EASI]`
3. Vérifiez que micro-ebusd est actif dans l'interface easi>
4. Testez l'API : `curl http://[IP_EASI]:8080/data`
5. Vérifiez que le port 8080 n'est pas bloqué par un pare-feu

### Problèmes MQTT

**Symptôme :** "Échec de connexion MQTT"

**Solutions :**
1. Vérifiez que l'addon Mosquitto broker est démarré
2. Consultez les logs de Mosquitto
3. Redémarrez Mosquitto broker
4. Vérifiez la configuration MQTT dans Home Assistant

### Entités non visibles

**Symptôme :** Les entités n'apparaissent pas dans Home Assistant

**Solutions :**
1. Attendez 1-2 minutes pour l'auto-discovery MQTT
2. Vérifiez les logs de l'addon pour des erreurs
3. Redémarrez l'addon
4. Redémarrez Home Assistant
5. Vérifiez que les noms de circuit/message sont corrects

### Valeurs "unknown"

**Symptôme :** Les entités affichent "unknown" ou "unavailable"

**Solutions :**
1. Vérifiez les noms exacts des circuits et messages dans l'interface easi>
2. Testez manuellement : `curl http://[IP_EASI]:8080/data/[circuit]/[message]`
3. Vérifiez les logs de l'addon pour voir les erreurs spécifiques
4. Augmentez le `scan_interval` si les valeurs apparaissent puis disparaissent

### Performances

**Problème :** L'addon consomme trop de ressources

**Solutions :**
1. Augmentez le `scan_interval` (ex: 60 ou 120 secondes)
2. Réduisez le nombre d'entités configurées
3. Ne configurez que les entités essentielles

## API eBUS

### Structure de l'API

L'API micro-ebusd expose les endpoints suivants :

```
GET /data                          # Liste tous les circuits
GET /data/{circuit}                # Liste les messages d'un circuit
GET /data/{circuit}/{message}      # Récupère la valeur d'un message
```

### Exemples de réponses

**Liste des circuits :**
```json
{
  "heating": {},
  "hotwater": {},
  "controller": {}
}
```

**Messages d'un circuit :**
```json
{
  "Temp": "75.5",
  "ReturnTemp": "65.0",
  "Pressure": "1.5"
}
```

**Valeur d'un message :**
```json
{
  "value": "75.5",
  "unit": "°C",
  "lastupdate": "2025-11-23 15:30:00"
}
```

### Classes de dispositifs Home Assistant

Utilisez ces `device_class` pour un affichage correct :

- `temperature` - Pour les températures
- `pressure` - Pour les pressions
- `power` - Pour les puissances
- `energy` - Pour l'énergie
- `humidity` - Pour l'humidité
- `battery` - Pour les niveaux de batterie

### Unités recommandées

- Température : `°C`
- Pression : `bar`
- Puissance : `%` ou `W`
- Débit : `L/min`

## Support et contribution

### Obtenir de l'aide

- 🐛 [Signaler un bug](https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/issues)
- 💬 [Discussions](https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/discussions)
- 📖 [Wiki](https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/wiki)

### Contribuer

Les contributions sont bienvenues ! Consultez le [guide de contribution](../CONTRIBUTING.md).

## Ressources

- [Documentation ebusd](https://github.com/john30/ebusd)
- [Wiki eBUS](https://ebus-wiki.org/)
- [Documentation Home Assistant](https://www.home-assistant.io/)
- [Site easi>](https://easi.link/)
