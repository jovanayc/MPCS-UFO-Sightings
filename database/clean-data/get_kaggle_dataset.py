import kagglehub

# Download latest version
path = kagglehub.dataset_download("NUFORC/ufo-sightings")

print("Path to dataset files:", path)

# to move:
# mv ~/.cache/kagglehub/datasets/NUFORC/ufo-sightings/versions/2 [YOUR PATH HERE]