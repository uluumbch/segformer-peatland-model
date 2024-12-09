import streamlit as st
import torch
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
from PIL import Image
import numpy as np

# Define color mapping and labels
colorandlabeltoID = [
    {"color": [255, 0, 0], "label": "vegetation with a density of 15 to 30 meters", "id": 0},  
    {"color": [255, 0, 102], "label": "shrubs that are 5 to 6 meters away", "id": 1},        
    {"color": [112, 48, 160], "label": "new shrubs that grow to a maximum of 3 meters", "id": 2},
    {"color": [237, 125, 49], "label": "dry bush", "id": 3},                               
    {"color": [131, 60, 12], "label": "land", "id": 4},                                       
    {"color": [0, 102, 255], "label": "water", "id": 5},                                         
    {"color": [255, 255, 0], "label": "house", "id": 6},                                       
]

@st.cache_resource
def load_model():
    # Get id2label from colorandlabeltoID
    id2label = {entry["id"]: entry["label"] for entry in colorandlabeltoID}
    label2id = {entry["label"]: entry["id"] for entry in colorandlabeltoID}
    
    # Load model and processor
    image_processor = SegformerImageProcessor()
    model = SegformerForSemanticSegmentation.from_pretrained(
        "nvidia/mit-b0",
        num_labels=len(id2label),
        id2label=id2label,
        label2id=label2id,
    )
    
    # Load trained weights
    model.load_state_dict(torch.load("./model/segformer_model_state_dict.pth", map_location=torch.device('cpu')))
    model.eval()
    
    return model, image_processor

def get_palette():
    return [entry["color"] for entry in colorandlabeltoID]

def process_image(image, model, image_processor):
    # Prepare image for model
    pixel_values = image_processor(image, return_tensors="pt").pixel_values
    
    # Forward pass
    with torch.no_grad():
        outputs = model(pixel_values=pixel_values)

    # Get segmentation map
    predicted_segmentation_map = image_processor.post_process_semantic_segmentation(
        outputs, target_sizes=[image.size[::-1]]
    )[0]
    
    return predicted_segmentation_map

def create_overlay(image, segmentation_map, opacity):
    # Create colored segmentation map
    color_seg = np.zeros((segmentation_map.shape[0], segmentation_map.shape[1], 3), dtype=np.uint8)
    palette = np.array(get_palette())
    for label, color in enumerate(palette):
        color_seg[segmentation_map == label] = color
    
    # Create overlay with adjustable opacity
    img = np.array(image) * (1 - opacity) + color_seg * opacity
    img = img.astype(np.uint8)
    
    return img

def main():
    st.title("PEATLAND SEGMENTATION")
    st.write("Upload an image to start segmenting peatland.")
    
    # Load model
    model, image_processor = load_model()
    
    # File uploader
    uploaded_file = st.file_uploader("Choose picture...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display original image and segmentation result side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Image:")
            image = Image.open(uploaded_file)
            st.image(image)
        
        with col2:
            # Process image
            predicted_segmentation_map = process_image(image, model, image_processor)
            
            # Create and display overlay with default opacity
            overlay = create_overlay(image, predicted_segmentation_map, 0.5)
            st.write("Segmentation Result:")
            segmentation_image = st.image(overlay)
            
            # Add opacity slider below the image
            opacity = st.slider("Segmentation Opacity", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
            
            # Update overlay with selected opacity
            overlay = create_overlay(image, predicted_segmentation_map, opacity)
            segmentation_image.image(overlay)
        
        # Display legend for only the classes present in the segmentation map
        st.write("Description:")
        classes_map = np.unique(predicted_segmentation_map).tolist()
        
        for entry in colorandlabeltoID:
            if entry["id"] in classes_map:
                color = entry["color"]
                label = entry["label"]
                st.markdown(
                    f'<div style="display: flex; align-items: center;">'
                    f'<div style="width: 20px; height: 20px; background-color: rgb({color[0]}, {color[1]}, {color[2]}); margin-right: 10px;"></div>'
                    f'<div>{label}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()