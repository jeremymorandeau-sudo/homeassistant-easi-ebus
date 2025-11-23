#!/usr/bin/env python3
"""
easi> eBUS Integration pour Home Assistant
Récupère les données depuis micro-ebusd et les publie via MQTT
"""

import json
import logging
import time
import sys
import requests
from typing import Dict, List, Optional
import paho.mqtt.client as mqtt

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EBusClient:
    """Client pour communiquer avec micro-ebusd"""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        
    def get_data(self, circuit: str, message: str) -> Optional[Dict]:
        """Récupère une donnée spécifique depuis eBUS"""
        try:
            url = f"{self.base_url}/data/{circuit}/{message}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Erreur HTTP {response.status_code} pour {circuit}/{message}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de connexion à ebusd: {e}")
            return None
    
    def get_all_circuits(self) -> Optional[List[str]]:
        """Récupère la liste de tous les circuits disponibles"""
        try:
            url = f"{self.base_url}/data"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return list(data.keys()) if isinstance(data, dict) else []
            else:
                logger.warning(f"Erreur HTTP {response.status_code} lors de la récupération des circuits")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de connexion à ebusd: {e}")
            return None


class HomeAssistantMQTT:
    """Gestion de la communication MQTT avec Home Assistant"""
    
    def __init__(self, broker: str = "core-mosquitto", port: int = 1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback de connexion MQTT"""
        if rc == 0:
            logger.info("Connecté au broker MQTT")
            self.connected = True
        else:
            logger.error(f"Échec de connexion MQTT, code: {rc}")
            self.connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """Callback de déconnexion MQTT"""
        logger.warning("Déconnecté du broker MQTT")
        self.connected = False
    
    def connect(self):
        """Établit la connexion MQTT"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # Attendre la connexion
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
                
            return self.connected
            
        except Exception as e:
            logger.error(f"Erreur de connexion MQTT: {e}")
            return False
    
    def publish_discovery(self, entity_config: Dict):
        """Publie la configuration d'auto-discovery pour Home Assistant"""
        entity_name = entity_config['name']
        entity_id = entity_name.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
        
        # Configuration pour Home Assistant MQTT Discovery
        discovery_topic = f"homeassistant/sensor/ebus_{entity_id}/config"
        
        config = {
            "name": entity_name,
            "unique_id": f"ebus_{entity_id}",
            "state_topic": f"homeassistant/sensor/ebus_{entity_id}/state",
            "value_template": "{{ value_json.value }}",
            "device": {
                "identifiers": ["easi_ebus"],
                "name": "easi> eBUS",
                "model": "micro-ebusd",
                "manufacturer": "easi>"
            }
        }
        
        # Ajout des attributs optionnels
        if 'unit' in entity_config:
            config['unit_of_measurement'] = entity_config['unit']
        if 'device_class' in entity_config:
            config['device_class'] = entity_config['device_class']
        
        self.client.publish(discovery_topic, json.dumps(config), retain=True)
        logger.info(f"Configuration publiée pour {entity_name}")
    
    def publish_state(self, entity_name: str, value: any, attributes: Dict = None):
        """Publie l'état d'une entité"""
        entity_id = entity_name.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
        state_topic = f"homeassistant/sensor/ebus_{entity_id}/state"
        
        payload = {
            "value": value
        }
        
        if attributes:
            payload.update(attributes)
        
        self.client.publish(state_topic, json.dumps(payload))


class EBusIntegration:
    """Intégration principale eBUS pour Home Assistant"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.ebus = EBusClient(config['ebusd_host'], config['ebusd_port'])
        self.mqtt = HomeAssistantMQTT()
        self.scan_interval = config.get('scan_interval', 30)
        
    def setup(self):
        """Initialisation de l'intégration"""
        logger.info("Démarrage de l'intégration easi> eBUS")
        logger.info(f"Configuration: Host={self.config['ebusd_host']}, Port={self.config['ebusd_port']}")
        
        # Connexion MQTT
        if not self.mqtt.connect():
            logger.error("Impossible de se connecter à MQTT")
            return False
        
        # Test de connexion eBUS
        circuits = self.ebus.get_all_circuits()
        if circuits is None:
            logger.error(f"Impossible de se connecter à ebusd sur {self.config['ebusd_host']}:{self.config['ebusd_port']}")
            return False
        
        logger.info(f"Circuits eBUS détectés: {circuits}")
        
        # Publication des configurations d'auto-discovery
        for entity_config in self.config.get('entities', []):
            self.mqtt.publish_discovery(entity_config)
        
        return True
    
    def update_entities(self):
        """Met à jour toutes les entités configurées"""
        for entity_config in self.config.get('entities', []):
            circuit = entity_config['circuit']
            message = entity_config['message']
            name = entity_config['name']
            
            # Récupération des données
            data = self.ebus.get_data(circuit, message)
            
            if data:
                # Extraction de la valeur
                value = data.get('value', data.get('data', 'unknown'))
                
                # Publication de l'état
                attributes = {
                    'circuit': circuit,
                    'message': message,
                    'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                self.mqtt.publish_state(name, value, attributes)
                logger.debug(f"{name}: {value}")
            else:
                logger.warning(f"Pas de données pour {circuit}/{message}")
    
    def run(self):
        """Boucle principale"""
        if not self.setup():
            logger.error("Échec de l'initialisation")
            return
        
        logger.info(f"Démarrage de la surveillance (intervalle: {self.scan_interval}s)")
        
        try:
            while True:
                self.update_entities()
                time.sleep(self.scan_interval)
                
        except KeyboardInterrupt:
            logger.info("Arrêt demandé")
        except Exception as e:
            logger.error(f"Erreur dans la boucle principale: {e}", exc_info=True)
        finally:
            self.mqtt.client.loop_stop()
            self.mqtt.client.disconnect()


def load_config() -> Dict:
    """Charge la configuration depuis les options de l'addon"""
    try:
        with open('/data/options.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Fichier de configuration non trouvé")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de lecture de la configuration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    config = load_config()
    integration = EBusIntegration(config)
    integration.run()
