import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from PIL import Image
import numpy as np

print("🔄 Loading CLIP model...")
# Load CLIP model via sentence-transformers
model = SentenceTransformer('clip-ViT-B-32')

print("📊 Loading catalog...")
df = pd.read_csv("data/grocery_catalog.csv")

print("🎨 Generating embeddings for product images...")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection_name = "product_images"
try:
    chroma_client.delete_collection(collection_name)
except:
    pass

collection = chroma_client.create_collection(
    name=collection_name,
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name='clip-ViT-B-32')
)

# Generate embeddings for each product
ids = []
embeddings = []
metadatas = []

for idx, row in df.iterrows():
    image_path = f"images/{row['image_filename']}"
    
    if os.path.exists(image_path):
        # Load and preprocess image
        image = Image.open(image_path)
        
        # Generate embedding
        embedding = model.encode(image)
        
        ids.append(str(row['product_id']))
        embeddings.append(embedding.tolist())
        metadatas.append({
            "name": row['name'],
            "price": str(row['price']),
            "category": row['category'],
            "unit": row['unit'],
            "dietary_labels": row['dietary_labels']
        })
        
        print(f"  ✅ Processed: {row['name']}")
    else:
        print(f"  ❌ Image not found: {image_path}")

# Add to ChromaDB
collection.add(
    ids=ids,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"\n✅ Stored {len(ids)} product embeddings in ChromaDB")
print(f"📁 ChromaDB saved to './chroma_db'")