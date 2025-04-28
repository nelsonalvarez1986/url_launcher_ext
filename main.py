import os
import subprocess
from pathlib import Path
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

class DevProjectsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        base_path = extension.preferences["base_path"]
        base_path = os.path.expanduser(base_path)

        if not os.path.exists(base_path):
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Error: Ruta base no encontrada",
                    description=f"La ruta {base_path} no existe",
                    highlightable=False
                )
            ])

        items = []
        try:
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                if os.path.isdir(full_path):
                    items.append(
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name=item,
                            description=f"Abrir {item} en el editor",
                            on_enter=RunScriptAction(
                                f"{extension.preferences['editor_path']} {full_path}"
                            )
                        )
                    )
        except Exception as e:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Error al listar directorios",
                    description=str(e),
                    highlightable=False
                )
            ])

        if not items:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="No se encontraron proyectos",
                    description="No hay directorios en la ruta especificada",
                    highlightable=False
                )
            ])

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        pass

if __name__ == "__main__":
    DevProjectsExtension().run() 