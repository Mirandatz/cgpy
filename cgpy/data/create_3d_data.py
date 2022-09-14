# Author: Matheus Ramos de Carvalho
# GitHub: https://github.com/OakBranches

import csv
import sys

import trimesh

# Os arquivos stl podem ser encontrados em sites de modelos 3d
# por exemplo: https://thingiverse.com, https://thangs.com/
# Esses arquivos podem ser feitos com softwares tipo Blender


def create_data() -> None:

    if len(sys.argv) < 2:
        print("você deve passar o caminho para o arquivo stl")
        return

    myobj = None

    try:
        name = sys.argv[1]

        myobj = trimesh.load_mesh(name, enable_post_processing=True, solid=True)
    except Exception as e:
        print("Não foi possivel encontrar o arquivo stl\n", e)
        return

    with open("cgpy/data/faces.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["face_index", "first_vertex", "second_vertex", "third_vertex"])

        for r in range(len(myobj.faces)):
            writer.writerow([r, *myobj.faces[r]])

    with open("cgpy/data/vertices.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["vertice_index", "x", "y", "z"])

        for r in range(len(myobj.vertices)):
            writer.writerow([r, *myobj.vertices[r]])


create_data()
