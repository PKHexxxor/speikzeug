"""
MCP-Server-Connector für Speikzeug
==================================

Diese Datei enthält eine Beispielimplementierung des MCP-Connectors,
der die Verbindung zu MCP-Servern herstellt und verwaltet.

Verwendung:
-----------
```python
from mcp_connector_template import MCPConnector

# Connector initialisieren
connector = MCPConnector(config_path="config/mcp_config.yaml")

# Verbindung testen
if connector.test_connection():
    print("MCP-Server-Verbindung erfolgreich!")
    
    # Daten senden
    data = {"operation": "process", "payload": {"key": "value"}}
    response = connector.send_data("/api/v1/process", data)
    print(f"Antwort: {response}")
else:
    print("MCP-Server-Verbindung fehlgeschlagen!")
```
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import httpx

class MCPConnector:
    """MCP-Server-Connector für Speikzeug"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialisiert den MCP-Connector.
        
        Args:
            config_path: Pfad zur YAML-Konfigurationsdatei
        """
        self.logger = logging.getLogger("speikzeug.mcp")
        self.config = self._load_config(config_path)
        self.client = self._init_client()
        self.logger.info("MCP-Connector initialisiert")
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Lädt die MCP-Konfiguration aus einer YAML-Datei."""
        if config_path is None:
            base_dir = Path(__file__).parent
            config_path = base_dir / "config" / "mcp_config.yaml"
            
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config['mcp']
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der MCP-Konfiguration: {e}")
            raise
    
    def _init_client(self) -> httpx.Client:
        """Initialisiert den HTTP-Client für MCP-Kommunikation."""
        return httpx.Client(
            base_url=f"{'https' if self.config['connection']['useSSL'] else 'http'}://"
                    f"{self.config['server']['host']}:{self.config['server']['port']}",
            timeout=self.config['connection']['timeout'],
            headers={"X-API-Key": self.config['server']['apiKey']}
        )
    
    def test_connection(self) -> bool:
        """Testet die Verbindung zum MCP-Server."""
        try:
            response = self.client.get("/health")
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"MCP-Verbindungsfehler: {e}")
            return False
    
    def send_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sendet Daten an einen MCP-Server-Endpoint."""
        try:
            response = self.client.post(endpoint, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Fehler beim Senden von Daten an MCP-Server: {e}")
            raise

    def get_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ruft Daten von einem MCP-Server-Endpoint ab."""
        try:
            response = self.client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Daten vom MCP-Server: {e}")
            raise
    
    def close(self) -> None:
        """Schließt die Verbindung zum MCP-Server."""
        try:
            self.client.close()
            self.logger.info("MCP-Verbindung geschlossen")
        except Exception as e:
            self.logger.error(f"Fehler beim Schließen der MCP-Verbindung: {e}")

# Einfaches Test-Skript für den Connector
if __name__ == "__main__":
    # Basis-Logging-Konfiguration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Beispiel für eine MCP-Konfiguration
    example_config = {
        'mcp': {
            'server': {
                'host': 'localhost',
                'port': 8080,
                'apiKey': 'test-api-key'
            },
            'connection': {
                'timeout': 30,
                'retries': 3,
                'useSSL': False
            }
        }
    }
    
    # Speichere Beispielkonfiguration in temporärer Datei
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / 'mcp_config_example.yaml'
    
    with open(config_path, 'w') as f:
        yaml.dump(example_config, f)
    
    try:
        print("🔄 Initialisiere MCP-Connector...")
        connector = MCPConnector(config_path=str(config_path))
        
        print("🔄 Teste MCP-Server-Verbindung...")
        # Hinweis: Dies wird fehlschlagen, da kein echter MCP-Server läuft
        if connector.test_connection():
            print("✅ MCP-Server-Verbindung erfolgreich hergestellt!")
        else:
            print("❌ MCP-Server-Verbindung fehlgeschlagen - überprüfen Sie die Server-Konfiguration.")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        # Temporäre Datei aufräumen
        if config_path.exists():
            config_path.unlink()
        
        print("✅ MCP-Connector-Test abgeschlossen.")