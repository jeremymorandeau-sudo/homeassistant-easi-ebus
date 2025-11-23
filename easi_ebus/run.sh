#!/usr/bin/with-contenv bashio

bashio::log.info "Démarrage de l'addon easi> eBUS Integration..."

# Récupération de la configuration
EBUSD_HOST=$(bashio::config 'ebusd_host')
EBUSD_PORT=$(bashio::config 'ebusd_port')
SCAN_INTERVAL=$(bashio::config 'scan_interval')

bashio::log.info "Configuration:"
bashio::log.info "  Host: ${EBUSD_HOST}"
bashio::log.info "  Port: ${EBUSD_PORT}"
bashio::log.info "  Intervalle de scan: ${SCAN_INTERVAL}s"

# Vérification de la connectivité
bashio::log.info "Vérification de la connexion à ebusd..."
if ! bashio::net.wait_for ${EBUSD_HOST} ${EBUSD_PORT} 30; then
    bashio::log.warning "Impossible de se connecter à ${EBUSD_HOST}:${EBUSD_PORT}"
    bashio::log.warning "Vérifiez que micro-ebusd est actif sur votre dispositif easi>"
fi

# Démarrage du script Python
bashio::log.info "Démarrage du service..."
exec python3 /ebus_integration.py
