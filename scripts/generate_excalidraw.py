import json
import uuid

def gen_id():
    return str(uuid.uuid4())

elements = []

def add_rect(x, y, w, h, text):
    rect_id = gen_id()
    text_id = gen_id()
    
    rect = {
        "id": rect_id,
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "strokeSharpness": "sharp",
        "seed": 1234,
        "version": 1,
        "versionNonce": 1234,
        "isDeleted": False,
        "boundElements": [{"id": text_id, "type": "text"}],
        "updated": 1
    }
    
    txt = {
        "id": text_id,
        "type": "text",
        "x": x + 10,
        "y": y + (h - 24) / 2,
        "width": w - 20,
        "height": 24,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "strokeSharpness": "sharp",
        "seed": 1234,
        "version": 1,
        "versionNonce": 1234,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "text": text,
        "fontSize": 20,
        "fontFamily": 1,
        "textAlign": "center",
        "verticalAlign": "middle",
        "baseline": 18,
        "containerId": rect_id
    }
    
    elements.extend([rect, txt])
    return rect_id

def add_arrow(start_x, start_y, end_x, end_y, start_id=None, end_id=None, text=None):
    arrow_id = gen_id()
    
    arrow = {
        "id": arrow_id,
        "type": "arrow",
        "x": start_x,
        "y": start_y,
        "width": abs(end_x - start_x),
        "height": abs(end_y - start_y),
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "strokeSharpness": "round",
        "seed": 1234,
        "version": 1,
        "versionNonce": 1234,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "points": [
            [0, 0],
            [end_x - start_x, end_y - start_y]
        ],
        "startBinding": {"elementId": start_id, "focus": -0.5, "gap": 5} if start_id else None,
        "endBinding": {"elementId": end_id, "focus": -0.5, "gap": 5} if end_id else None,
        "startArrowhead": None,
        "endArrowhead": "arrow"
    }

    if text:
        text_id = gen_id()
        txt = {
            "id": text_id,
            "type": "text",
            "x": start_x + (end_x - start_x) / 2 - 50,
            "y": start_y + (end_y - start_y) / 2 - 20,
            "width": 100,
            "height": 20,
            "angle": 0,
            "strokeColor": "#e03131",
            "backgroundColor": "transparent",
            "fillStyle": "hachure",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "strokeSharpness": "sharp",
            "seed": 1234,
            "version": 1,
            "versionNonce": 1234,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "text": text,
            "fontSize": 16,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "baseline": 14,
            "containerId": arrow_id
        }
        arrow["boundElements"] = [{"id": text_id, "type": "text"}]
        elements.extend([arrow, txt])
    else:
        elements.append(arrow)

# Nodes
w, h = 240, 60
d_id = add_rect(300, 100, w, h, "DataHub (Glossary)")
k_id = add_rect(300, 250, w, h, "Kafka (MCL Event)")
dz_id = add_rect(100, 450, w, h, "DozerDB (Graph DB)")
v_id = add_rect(500, 450, w, h, "Vanna (RAG Store)")
ar_id = add_rect(700, 100, w, h, "ApeRAG (Extraction)")

# Edges
add_arrow(420, 160, 420, 250, d_id, k_id, "Term Changed")
add_arrow(360, 310, 220, 450, k_id, dz_id, "Real-time sync")
add_arrow(480, 310, 620, 450, k_id, v_id, "Context update")
add_arrow(700, 130, 540, 130, ar_id, d_id, "Taxonomy reference")

excalidraw_data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "#ffffff"
    },
    "files": {}
}

with open(r"d:\OneDrive\Documents\0.Projects\DataNexus-Blog-Source\static\images\datanexus\metadata-sync.excalidraw", "w", encoding="utf-8") as f:
    json.dump(excalidraw_data, f, indent=2, ensure_ascii=False)

print("Excalidraw JSON generated.")
