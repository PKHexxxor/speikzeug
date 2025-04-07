# Speikzeug

## Modernes Toolset mit MCP-Server-Integration

Modulares Werkzeug zur automatisierten Datenverarbeitung mit direkter Anbindung an MCP-Server-Infrastruktur für verbesserte Systemanonymisierung und skalierbares Datenmanagement.

## 🔧 Kernfunktionalitäten

- **MCP-Server-Konnektivität**: Standardisierte Kommunikationsschnittstellen zur nahtlosen Integration in bestehende MCP-Landschaften
- **Modulares Design**: Erweiterbare Architektur für benutzerspezifische Anpassungen
- **Datenverarbeitungs-Pipeline**: Optimierte Verarbeitungsstruktur für große Datenmengen
- **Automatisierte Anonymisierung**: Compliance-konforme Maskierungsroutinen

## 📋 Systemvoraussetzungen

- Windows 10/11 (64-bit)
- Python 3.11+
- MCP-Server 2.4 oder höher
- PowerShell 5.1+

## 🚀 Installation

```powershell
# Repository klonen
git clone https://github.com/PKHexxxor/speikzeug.git
cd speikzeug

# Initialisierung ausführen
.\tools\setup.ps1
```

## ⚙️ Konfiguration

Die MCP-Server-Verbindung wird über die `config\mcp_config.yaml` konfiguriert:

```yaml
mcp:
  server:
    host: localhost
    port: 8080
    apiKey: %%MCP_API_KEY%%
  connection:
    timeout: 30
    retries: 3
    useSSL: true
```

## 📊 Architekturübersicht

```
speikzeug/
├── core/            # Kernkomponenten
├── services/        # Dienstmodule
├── connectors/      # MCP-Server-Connector
├── processors/      # Datenverarbeitungsmodule
├── utils/           # Hilfsfunktionen
├── config/          # Konfigurationsdateien
└── tools/           # Installationswerkzeuge
```

## 🔄 Integration mit MCP-Server

Die Integration mit MCP-Server erfolgt über das standardisierte Protokoll und ermöglicht:

- Echtzeit-Datenverarbeitung
- Ereignisbasierte Trigger
- Verschlüsselte Kommunikationskanäle
- Zentralisiertes Logging und Monitoring

## 📄 Lizenz

MIT