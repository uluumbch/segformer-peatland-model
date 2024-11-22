import json

colorandlabeltoID = [
    {"color": [255, 0, 0], "label": "vegetasi dengan kerapatan 15 hingga 30 meter", "id": 0},   # Red
    {"color": [255, 0, 102], "label": "semak yang berjarak 5 hingga 6 meter", "id": 1},         # Pink
    {"color": [112, 48, 160], "label": "semak baru yang tumbuh hingga maksimum 3 meter", "id": 2}, # Purple
    {"color": [237, 125, 49], "label": "semak kering", "id": 3},                                # Orange
    {"color": [131, 60, 12], "label": "tanah", "id": 4},                                        # Brown
    {"color": [0, 102, 255], "label": "air", "id": 5},                                          # Blue
    {"color": [255, 255, 0], "label": "rumah", "id": 6},                                        # Yellow
]

id2label = {entry["id"]: entry["label"] for entry in colorandlabeltoID}
label2id = {entry["label"]: entry["id"] for entry in colorandlabeltoID}

# Save id2label to a JSON file
with open('id2label.json', 'w') as f:
    json.dump(id2label, f)

# Save label2id to a JSON file
with open('label2id.json', 'w') as f:
    json.dump(label2id, f)

# Save colorandlabeltoID to a JSON file
with open('colorandlabeltoID.json', 'w') as f:
    json.dump(colorandlabeltoID, f)