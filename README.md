# pyday-freecad-cad-automatización
Charla dada durante el PyDay La Plata, Edición 2026: "De Catálogos a Código: Modelado CAD Paramétrico con Python y FreeCAD"

## 🚀 Instrucciones de ejecución

Para generar los archivos `.FCStd` y `.stl` de los rodamientos detallados en `catalogo_rodamientos.csv`:

### Opción A: Desde la terminal con FreeCAD
```bash
freecad --console crear_rodamientos.py
```
### Opción B: Con el intérprete estándar de Python

Si ejecutas el script con la instalación global de Python de tu sistema, descomenta las siguientes líneas al inicio de `crear_rodamientos.py` y ajusta la ruta hacia la librería de FreeCAD según tu SO:
```python
import sys
sys.path.append("/usr/lib64/freecad/lib64") # Reemplazar con la ruta local a FreeCAD
```
