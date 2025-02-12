title: Traefik v3 mit Docker nutzen
status: published
lang: de
date: 2025-02-12 10:28:00

[TOC]


Traefik ist ein Edge Router der ankommende Anfragen an dahinterliegenden Kontainersysteme, wie z.B. Docker, weiterleitet. Hierdurch kann man mehrere Dienste hinter einer IP und Port Kombination betreiben. Dies geschieht mithilfe dynamischen Regeln bei der Konfiguration der Container Stacks. Im Fall von Docker kann man die Konfiguration nahezu vollständig mithilfe von Labels lösen. Es gibt auch eine Plugin Landschaft mit deren Hilfe nützliche Funktionen erweitert werden können. Eines davon ist das Plugin für Let's Encrypt. Hiermit können SSL Zertifikat von Let's Encrypt beantragt werden. Mit dem richtigen DNS Anbieter kann man dann auch Wildcard Zertifikate bereitstellen.

Ich nutze Traefik sowohl bei meinen Servern im Internet, aber seit kurzem Nutze ich dies auch um in meinem Heimnetz alle Diesnte hinter einem SSL Zertifikaten bereitzustellen. Dies sorgt dafür das keine Zertifikatswarnung erscheint und es somit Benutzerfreundlicher für die Benutzer im Haushalt sind.

Hier werde ich meinen aktuellen Stand der Konfiguration dokumentieren. Ich habe mir die Informationen aus vielen Quellen besorgt und weiß nicht mehr genau welche Quellen ich in welchem Umfang genutzt habe. Daher werde ich am Ende eine allgemeine Liste mit meinen Quellen anhängen.

## Server

Als Basis dient ein Debian 12 Linux mit der installierten Docker Engine + Docker Compose. Der Server besitzt eine statische IP und es wurde der SSH Dienst aktiviert. Für einige Container wurden separate Benutzer Zugänge (ohne SSH Anmeldung) eingerichtet. Bei dem Server handelt es sich um ein einer Intel(R) Core(TM) i7-5557U CPU @ 3.10GHz CPU mit 16 GB Arbeitsspeicher. Auch hier wird es zukünftig noch Anpassungen geben, aber für den Start war das die verfügbare Hardware.

## Traefik

Für die Erstellung eines Wildcard Zertifikats kann man unterschiedliche Anbieter nutzen. Ich beschreibe hier den Weg über den Hoster **netcup** da anderen Projekte gute Erfahrungen mit dem Hoster gemacht habe. Jeder Anbieter von der [Liste](https://doc.traefik.io/traefik/https/acme/#providers) kann für die Beauftragung eines Wildcard Zertifikates genutzt werden. Andere bekannte Anbieter wie Hetzner, ionos oder IPv64 sind genauso denkbar.

Für die Nutzung von Traefik wird ein Docker Netzwerk benötigt. Über dieses Netzwerk kommuniziert der Traefik Container dann mit allen anderen Frontend Containern. Der Befehl dafür lautet:


    docker network create proxy


### Konfiguration

**.env**

In dieser Datei werden alle Umgebungvariablen abgelegt, damit die Secrets und andere geheime Informationen nicht in der Compose Datei aufgeführt werden. Das ermöglich die Weitergabe der Compose Datei.

    MY_DOMAIN=example.org
    ACME_EMAIL=acme@example.org
    NETCUP_CUSTOMER_NUMBER=<Kundennummer>
    NETCUP_API_KEY=<API Key>
    NETCUP_API_PASSWORD=<API Password>


**compose.yaml**

Für die ersten Test empfiehlt sich die Zeile mit "--certificatesresolvers.letsencrypt.acme.caServer=https://acme-staging-v02.api.letsencrypt.org/directory" zu aktivieren, da man hierdurch den Let's Encrypt Staging Server nutzt. Man wird nicht geblockt, falls man in der Anfangszeit zu viele Abfragen in Richtung Let's Encrypt schickt. Daher ist das eine Empfehlung.

Die Traefik Webseite ist in diesem Beispiel ohne Passwort Abfrage über die URL **traefik.example.org** erreichbar.

Es werden nicht alle Docker Container für die Nutzung von Traefik freigeschaltet. Wenn ein Container über den Traefik Proxy erreichbar sein soll, muss das mithilfe eines Labels explizit erwähnt werden. Dazu später mehr

    services:
      proxy:
        image: traefik
        container_name: traefik
        restart: unless-stopped
        command:
          - "--log.level=INFO"
          - "--api.insecure=true"
          - "--api.dashboard=true"
          - "--serversTransport.insecureSkipVerify=true"
          - "--providers.docker=true"
          - "--providers.docker.exposedbydefault=false"
          - "--providers.docker.endpoint=unix:///var/run/docker.sock"
          - "--providers.file.filename=/config.yml"
          - "--certificatesresolvers.letsencrypt.acme.dnschallenge=true"
          - "--certificatesresolvers.letsencrypt.acme.dnschallenge.provider=netcup"
          - "--certificatesresolvers.letsencrypt.acme.dnschallenge.disablePropagationCheck=true"
          - "--certificatesresolvers.letsencrypt.acme.dnschallenge.resolvers=1.1.1.1:53,8.8.8.8:53"
          - "--certificatesresolvers.letsencrypt.acme.dnschallenge.delayBeforeCheck=600s"
          - "--certificatesresolvers.letsencrypt.acme.dnschallenge.disablePropagationCheck=true"
          - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"
          - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    #      - "--certificatesresolvers.letsencrypt.acme.caServer=https://acme-staging-v02.api.letsencrypt.org/directory"
          - "--entrypoints.web.address=:80"
          - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
          - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
          - "--entrypoints.websecure.address=:443"
          - "--entrypoints.websecure.http.tls=true"
          - "--entrypoints.websecure.http.tls.certResolver=letsencrypt"
          - "--entrypoints.websecure.http.tls.domains[0].main=${MY_DOMAIN}"
          - "--entrypoints.websecure.http.tls.domains[0].sans=*.${MY_DOMAIN}"
        volumes:
          - "./data/letsencrypt:/letsencrypt"
          - "./data/config.yml:/config.yml:ro"
          - "/var/run/docker.sock:/var/run/docker.sock:ro"
          - "/etc/localtime:/etc/localtime:ro"
        labels:
          - 'traefik.enable=true'
          - 'traefik.http.routers.api.rule=Host(`traefik.${MY_DOMAIN}`)'
          - 'traefik.http.routers.api.entryPoints=websecure'
          - 'traefik.http.routers.api.service=api@internal'
        ports:
          - "443:443"
          - "80:80"
        environment:
          NETCUP_CUSTOMER_NUMBER: "${NETCUP_CUSTOMER_NUMBER}"
          NETCUP_API_KEY: "${NETCUP_API_KEY}"
          NETCUP_API_PASSWORD: "${NETCUP_API_PASSWORD}"
          ACME_EMAIL: "${ACME_EMAIL}"
          TZ: "Europe/Berlin"
        networks:
          - proxy

    networks:
      proxy:
        external: true


**data/config.yml**

Die **config.yml** wird genutzt um einige bestimmte Optionen zu setzen. Zusätzlich habe ich Dienste konfiguriert wofür ich keine Container definiert habe. Darunter ist die Administrationsoberfläche von dem Proxmox, der NAS, der PiHole und dem Home Assistant. Die Header Informationen habe ich von einer der unten genannten Quellen übernommen. Gerade für die Proxmox Console sind diese Anpassungen notwendig.

    http:
      routers:
        proxmox:
          entrypoints:
            - "websecure"
          rule: "Host(`proxmox.example.org`)"
          middlewares:
            - default-headers
            - https-redirectscheme
          tls: {}
          service: proxmox
        homeassistant:
          entrypoints:
            - "websecure"
          rule: "Host(`home.example.org`)"
          middlewares:
            - default-headers
            - https-redirectscheme
          service: homeassistant
        storage:
          entrypoints:
            - "websecure"
          rule: "Host(`storage.example.org)"
          middlewares:
            - default-headers
            - https-redirectscheme
          service: storage
        pihole:
          entrypoints:
            - "websecure"
          rule: "Host(`pihole.example.org`)"
          middlewares:
            - default-headers
            - https-redirectscheme
          service: pihole
        piholeAdmin:
          entrypoints:
            - "websecure"
          rule: "Host(`pihole.example.org`) && Path(`/`)"
          middlewares:
            - default-headers
            - pihole-admin-redirect
          service: pihole

      services:
        proxmox:
          loadBalancer:
            servers:
              - url: "https://192.168.x.201:8006"
            passHostHeader: true
        homeassistant:
          loadBalancer:
            servers:
              - url: "http://192.168.x.202:8123"
            passHostHeader: true
        storage:
          loadBalancer:
            servers:
              - url: "http://192.168.x.28:9999"
            passHostHeader: true
        pihole:
          loadBalancer:
            servers:
              - url: "http://192.168.x.254:80/admin/"
            passHostHeader: true

      middlewares:
        pihole-admin-redirect:
          redirectRegex:
            regex: "/$"
            replacement: "/admin/"
        https-redirectscheme:
          redirectScheme:
            scheme: https
            permanent: true
        default-headers:
          headers:
            frameDeny: true
            browserXssFilter: true
            contentTypeNosniff: true
            forceSTSHeader: true
            stsIncludeSubdomains: true
            stsPreload: true
            stsSeconds: 15552000
            customFrameOptionsValue: SAMEORIGIN
            customRequestHeaders:
            X-Forwarded-Proto: https

        secured:
          chain:
            middlewares:
            - default-whitelist
            - default-headers


An dieser Stelle sind alle notwendigen Einstellungen durchgeführt und der Container kann gestartet werden. Bei der ersten Einrichtung wird nun die Kommunikation mit dem DNS Hoster hergestellt und das Let's Encrypt Zertifikat beantragt. Im Log wird das erfolgreiche Beauftragen des Zertifikats angezeigt.

## Container Konfiguration

Die Konfiguration bei einem Container zeige ich beispielhaft anhand des [Dashboard](https://heimdall.site/) Containers den ich für die Benutzer hier eingerichtet habe. Zusätzlich zeige ich noch eine Konfiguration mit mehr als einem Container, da sich die Nutzung der Netzwerke hier unterscheidet. Das hatte mich in der Anfangszeit etwas zurückgeworfen.

### Heimdall (Dashboard) Container

**.env**

    MY_DOMAIN=example.org


**compose.yaml**

Zeile 2: interner Servicename
Zeile 4: Systemweiter Container Name

Über die Labels wird nun die Nutzung von Traefik aktiviert. Der Name des Routers (traefik.http.routers.**heimdall**.xxx) muss über die gesamte Infrastruktur einzigartig sein. Andernfalls kann Traefik keine Zuordnung zwischen Name und Container herstellen. Für die Nutzung von Traefik ist zusätzlich die angabe des Proxy Netzwerk notwendig. Das geschieht an unterschiedlichen Stellen im

    services:
      heimdall:
        image: lscr.io/linuxserver/heimdall:latest
        container_name: heimdall
        restart: unless-stopped
        volumes:
          - "./data/config:/config"
        labels:
          - 'traefik.enable=true'
          - 'traefik.http.routers.heimdall.rule=Host(`www.${MY_DOMAIN}`)'
          - 'traefik.http.routers.heimdall.entryPoints=websecure'
          - 'traefik.docker.network=proxy'
        environment:
          PUID: 1000
          PGID: 1000
          TZ: "Europe/Berlin"
        networks:
          - proxy

    networks:
      proxy:
        external: true


### SearXNG (Suchmaschine Aggregator)

**.env**

    MY_DOMAIN=example.org


**compose.yaml**

An dieser Stelle ist auf die Konfiguratonsoption *networks* hinzuweisen. Sollten sich innerhalb eines Deployments mehr als ein Container befinden, welche alle miteinander kommunizieren, musste ich das default Netzwerk explizit überall angegeben. Der Container, welcher von außen erreichbar sein soll, muss zusätzlich noch das Proxy Netzwerk bekommen.

    services:
      redis:
        image: docker.io/valkey/valkey:8-alpine
        container_name: searxngredis
        restart: unless-stopped
        volumes:
          - "./data/redis:/data"
        environment:
          TZ: "Europe/Berlin"
        cap_drop:
          - ALL
        cap_add:
          - SETGID
          - SETUID
          - DAC_OVERRIDE
        networks:
          - default

      searxng:
        image: docker.io/searxng/searxng:latest
        container_name: searxng
        restart: unless-stopped
        volumes:
          - "./config/searxng:/etc/searxng:rw"
        environment:
          SEARXNG_HOSTNAME: https://search.example.org
          TZ: "Europe/Berlin"
          # SEARXNG_UWSGI_WORKERS: 4
          # SEARXNG_UWSGI_THREADS: 4
        cap_drop:
          - ALL
        cap_add:
          - CHOWN
          - SETGID
          - SETUID
        labels:
          - 'traefik.enable=true'
          - 'traefik.http.routers.searxng.rule=Host(`search.${MY_DOMAIN}`)'
          - 'traefik.http.routers.searxng.entryPoints=websecure'
          - 'traefik.docker.network=proxy'
        networks:
          - default
          - proxy

    networks:
      proxy:
        external: true
