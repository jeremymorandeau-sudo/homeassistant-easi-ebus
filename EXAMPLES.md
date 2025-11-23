# Exemples de configuration

Ce fichier contient différents exemples de configuration pour divers cas d'usage.

## Configuration minimale

Pour une installation simple avec les données essentielles :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30
entities:
  - name: "Température départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "Pression circuit"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
```

## Configuration complète (chauffage uniquement)

Pour surveiller en détail votre système de chauffage :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30
entities:
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
  - name: "Température eau circuit"
    circuit: "heating"
    message: "FlowTemp"
    unit: "°C"
    device_class: "temperature"
  - name: "Pression circuit chauffage"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
  - name: "Puissance pompe chauffage"
    circuit: "heating"
    message: "PumpPower"
    unit: "%"
  - name: "État chaudière"
    circuit: "heating"
    message: "Status"
  - name: "État brûleur"
    circuit: "heating"
    message: "BurnerStatus"
  - name: "Modulation brûleur"
    circuit: "heating"
    message: "ModulationTemp"
    unit: "°C"
    device_class: "temperature"
```

## Configuration multi-circuits

Pour surveiller chauffage, ECS et contrôleur :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30
entities:
  # Circuit de chauffage
  - name: "CH - Température départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "CH - Température retour"
    circuit: "heating"
    message: "ReturnTemp"
    unit: "°C"
    device_class: "temperature"
  - name: "CH - Pression"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
  - name: "CH - État"
    circuit: "heating"
    message: "Status"
  
  # Eau chaude sanitaire
  - name: "ECS - Température actuelle"
    circuit: "hotwater"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "ECS - Température souhaitée"
    circuit: "hotwater"
    message: "TempDesired"
    unit: "°C"
    device_class: "temperature"
  - name: "ECS - Débit"
    circuit: "hotwater"
    message: "Flow"
    unit: "L/min"
  - name: "ECS - État"
    circuit: "hotwater"
    message: "Status"
  
  # Contrôleur
  - name: "Température pièce"
    circuit: "controller"
    message: "RoomTemp"
    unit: "°C"
    device_class: "temperature"
  - name: "Température extérieure"
    circuit: "controller"
    message: "OutdoorTemp"
    unit: "°C"
    device_class: "temperature"
  - name: "Mode vacances"
    circuit: "controller"
    message: "HolidayMode"
  - name: "Mode fonctionnement"
    circuit: "controller"
    message: "OperatingMode"
```

## Configuration haute fréquence

Pour des mises à jour très fréquentes (consomme plus de ressources) :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 10  # Toutes les 10 secondes
entities:
  - name: "Température départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "Puissance instantanée"
    circuit: "heating"
    message: "PumpPower"
    unit: "%"
```

## Configuration basse fréquence

Pour économiser les ressources :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 120  # Toutes les 2 minutes
entities:
  - name: "Température départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "Pression circuit"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
```

## Configuration pour Vaillant

Exemple pour chaudière Vaillant :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30
entities:
  - name: "Vaillant - T° départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "Vaillant - T° retour"
    circuit: "heating"
    message: "ReturnTemp"
    unit: "°C"
    device_class: "temperature"
  - name: "Vaillant - Pression"
    circuit: "heating"
    message: "Pressure"
    unit: "bar"
    device_class: "pressure"
  - name: "Vaillant - Débit"
    circuit: "heating"
    message: "WaterFlow"
    unit: "L/min"
  - name: "Vaillant - T° ECS"
    circuit: "hotwater"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
```

## Configuration avec plusieurs zones

Pour systèmes multi-zones :

```yaml
ebusd_host: "192.168.0.26"
ebusd_port: 8080
scan_interval: 30
entities:
  # Chaudière principale
  - name: "Chaudière - T° départ"
    circuit: "heating"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  
  # Zone 1 (RDC)
  - name: "Zone RDC - T° départ"
    circuit: "zone1"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "Zone RDC - Vanne"
    circuit: "zone1"
    message: "ValvePosition"
    unit: "%"
  
  # Zone 2 (Étage)
  - name: "Zone Étage - T° départ"
    circuit: "zone2"
    message: "Temp"
    unit: "°C"
    device_class: "temperature"
  - name: "Zone Étage - Vanne"
    circuit: "zone2"
    message: "ValvePosition"
    unit: "%"
```

## Conseils

### Scan Interval
- **10-15s** : Pour surveillance en temps réel (haute consommation)
- **30s** : Bon équilibre performance/réactivité (recommandé)
- **60s** : Pour économiser les ressources
- **120-300s** : Pour données peu variables (température extérieure, etc.)

### Nommage
- Utilisez des préfixes clairs (CH, ECS, Zone, etc.)
- Gardez les noms courts et descriptifs
- Évitez les caractères spéciaux

### Performance
- Ne configurez que les entités dont vous avez besoin
- Augmentez le scan_interval pour les données peu variables
- Testez avec une configuration minimale d'abord
