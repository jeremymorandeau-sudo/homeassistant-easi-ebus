# Guide de démarrage rapide

## Installation en 5 minutes

### 1. Ajoutez le dépôt (1 min)

Dans Home Assistant :
1. Allez dans **Paramètres** → **Modules complémentaires** → **Boutique**
2. Cliquez sur **⋮** (trois points) → **Dépôts**
3. Ajoutez :
   ```
   https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus
   ```

### 2. Installez l'addon (2 min)

1. Recherchez "easi> eBUS Integration"
2. Cliquez sur **INSTALLER**
3. Attendez la fin de l'installation

### 3. Configurez (1 min)

Allez dans l'onglet **Configuration** et modifiez :

```yaml
ebusd_host: "192.168.0.26"  # ⚠️ Changez par VOTRE IP
```

### 4. Démarrez (30 secondes)

1. Allez dans l'onglet **Informations**
2. Cliquez sur **DÉMARRER**
3. Activez **Démarrer au boot**

### 5. Vérifiez (30 secondes)

1. Consultez l'onglet **Journal**
2. Vous devriez voir :
   ```
   [INFO] Connecté au broker MQTT
   [INFO] Circuits eBUS détectés: ['heating', ...]
   ```

## C'est prêt !

Vos entités sont maintenant disponibles :
- `sensor.ebus_temperature_depart`
- `sensor.ebus_temperature_retour`
- `sensor.ebus_pression_circuit`

## Prochaines étapes

1. **Personnalisez** : Ajoutez plus d'entités dans la configuration
2. **Visualisez** : Créez une carte Lovelace
3. **Automatisez** : Créez des alertes

## Besoin d'aide ?

- 📖 [Documentation complète](easi_ebus/DOCS.md)
- 🐛 [Signaler un problème](https://github.com/VOTRE_USERNAME/homeassistant-easi-ebus/issues)
