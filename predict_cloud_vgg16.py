import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import os

# Classes dans le même ordre que dataset.ImageFolder
class_names = ['A-Clear Sky', 'B-Patterned Clouds', 'C-Thin White Clouds',
               'D-Thick White Clouds', 'E-Thick Dark Clouds', 'F-Veil Clouds']

# Image à prédire
image_path = 'exemple_image.png'  # ⇦ Modifie ici

# 🔁 Prétraitement
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Charger modèle
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, len(class_names))
model.load_state_dict(torch.load('vgg16_cloud_classifier_best.pth', map_location=device))
model.eval()
model = model.to(device)

# 🔍 Prediction
image = Image.open(image_path).convert('RGB')
image_tensor = transform(image).unsqueeze(0).to(device)

with torch.no_grad():
    output = model(image_tensor)
    _, predicted = torch.max(output, 1)
    predicted_class = class_names[predicted.item()]

print(f"Prédiction : {predicted_class}")