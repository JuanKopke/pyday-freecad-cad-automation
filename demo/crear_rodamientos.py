#import sys
#sys.path.append("/usr/lib64/freecad/lib64")

import FreeCAD as App
import Part
import Draft
import MeshPart
from BOPTools import BOPFeatures
import pandas as pd
import os

def crear_tubo(doc, label, r_int, r_ext, h):
    c_ext = Part.makeCylinder(r_ext, h)
    c_int = Part.makeCylinder(r_int, h)
    tubo = doc.addObject("Part::Feature", label)
    tubo.Shape = c_ext.cut(c_int)
    return tubo

def crear_cad_rodamiento(row):
    
    # Desestructuración directa de medidas geométricas
    B  = row['B']
    d  = row['d']
    d1 = row['d1']
    D  = row['D']
    D1 = row['D1']
    r  = row['r']
    
    # Documento FreeCAD
    App.newDocument('doc')
    doc = App.ActiveDocument
    bp = BOPFeatures.BOPFeatures(doc)
    
    # Anillos interior y exterior
    crear_tubo(doc, 'AnilloInt', d / 2.0, d1 / 2.0, B)
    crear_tubo(doc, 'AnilloExt', D1 / 2.0, D / 2.0, B)
    Fusion = bp.make_multi_fuse(["AnilloInt", "AnilloExt"])
    
    # Redondeo (Fillet)
    fillet = doc.addObject("Part::Fillet", "Fillet")
    fillet.Base = doc.Fusion
    fillet.Edges = [(4, r, r), (5, r, r), (7, r, r), (9, r, r)]
    
    # Pista de rodamientos (Toroide)
    torus = doc.addObject("Part::Torus", "Torus")
    torus.Radius1 = (D1 + d1) / 4.0
    torus.Radius2 = (D1 - d1) / 2.0
    torus.Placement.Base = App.Vector(0, 0, B / 2.0)
    
    Corte = bp.make_cut(["Fillet", "Torus"])
    
    # Elementos rodantes (Esferas)
    esfera = doc.addObject("Part::Sphere", "Sphere")
    esfera.Radius = (D1 - d1) / 2.0
    esfera.Placement.Base = App.Vector(0, (d1 + D1) / 4.0, B / 2.0)
    
    # Arreglo de esferas
    n_bolas = round(5.0 * (d1 + D1) / (4.0 * (D1 - d1)))
    array_bolas = Draft.make_polar_array(esfera, number=n_bolas, angle=360.0)
    
    doc.recompute()
    
    # Contenedor Part
    part_container = doc.addObject('App::Part', 'Part')
    part_container.addObject(array_bolas)
    part_container.addObject(Corte)
    doc.recompute()
    
    
    # Guardado y exportación
    desig = str(row['Designacion 1']).replace('/', '-')
    os.makedirs('output/FCStd', exist_ok=True)
    os.makedirs('output/STL', exist_ok=True)
    ruta_fcstd = f'output/FCStd/SKF_{desig}.FCStd'
    ruta_stl   = f'output/STL/SKF_{desig}.stl'
    
    forma = Part.makeCompound([Corte.Shape, array_bolas.Shape])
    malla = MeshPart.meshFromShape(Shape=forma, LinearDeflection=0.001, AngularDeflection=0.314, Relative=True)
    malla.write(ruta_stl)
    
    doc.saveAs(ruta_fcstd)
    App.closeDocument('doc')
    
    print(f'Rodamiento creado con éxito: SKF_{desig}')


# Carga de datos
df = pd.read_csv('catalogo_rodamientos.csv')

# Bucle principal
for _, row in df.iterrows():
    crear_cad_rodamiento(row)
