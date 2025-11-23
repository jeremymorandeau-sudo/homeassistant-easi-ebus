ARG BUILD_FROM
FROM $BUILD_FROM

# Définir les variables d'environnement
ENV LANG C.UTF-8

# Installation de Python et des dépendances système
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    gcc \
    musl-dev

# Installation des packages Python
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir \
    requests==2.31.0 \
    paho-mqtt==1.6.1

# Copie des fichiers de l'addon
COPY run.sh /
COPY ebus_integration.py /

# Rendre le script exécutable
RUN chmod a+x /run.sh

# Labels
LABEL \
    io.hass.name="easi> eBUS Integration" \
    io.hass.description="Integration pour systèmes easi> eBUS" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"

CMD [ "/run.sh" ]
