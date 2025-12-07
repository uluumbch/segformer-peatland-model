## Segformer UI

This is a simple UI for the Segformer model. The model is used for segmenting Peatland Vegetation Density. The model is trained on the [Segmented Vegetation-Density Drone Dataset for Peatland Vegetation Classification](https://data.mendeley.com/datasets/fss67tz8w8/1).

## Run
### using streamlit
```bash
streamlit run app.py
```

### using Dockerfile
```
docker build -t segformer-peatland-model:latest .
# and then run
docker run segformer-peatland-model:latest -p 8501:8501
```

### using prebuilt images
```
docker run -p 8501:8501 ghcr.io/uluumbch/segformer-peatland-model:latest
```



Built with [Streamlit](https://www.streamlit.io/).
