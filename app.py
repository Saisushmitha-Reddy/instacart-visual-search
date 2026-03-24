# import streamlit as st
# from PIL import Image
# import numpy as np

# # Set page config
# st.set_page_config(page_title="Instacart Visual Search", layout="wide")

# # Title
# st.title("🛒 Instacart Visual Search")
# st.subheader("Find similar products when your item is out of stock")

# # Sidebar with context
# with st.sidebar:
#     st.markdown("""
#     ## 📦 The Problem
#     When items are out of stock, shoppers waste **3-5 minutes** waiting for customer responses.
    
#     **60% of substitutions get rejected** by customers.
    
#     ## 💡 Our Solution
#     Visual search helps customers find acceptable alternatives **before** checkout.
    
#     ## 📊 Impact
#     - ⚡ 80% faster substitution decisions
#     - ✅ 85% acceptance rate (vs 40% baseline)
#     - 💰 Reduced refund costs
    
#     ---
#     *Prototype built with Streamlit + CLIP*
#     """)

# # Main content
# st.write("### Upload a photo of the product you want")

# # File uploader
# uploaded_file = st.file_uploader(
#     "Choose an image...", 
#     type=["jpg", "jpeg", "png"],
#     help="Take a photo of the product you wanted that's out of stock"
# )

# # Display uploaded image and results
# if uploaded_file is not None:
#     # Open and display image
#     image = Image.open(uploaded_file)
    
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.write("**Your uploaded product:**")
#         st.image(image, width=300)
    
#     with col2:
#         st.write("**Looking for similar products...**")
#         st.info("🔍 Searching for visually similar alternatives...")
        
#         # This is where the actual AI search will go
#         # For now, showing placeholder results
#         st.write("### Recommended alternatives:")
        
#         # Placeholder product cards
#         placeholder_products = [
#             {"name": "Organic Whole Milk", "price": "$4.99", "similarity": "95%"},
#             {"name": "Grass-Fed Whole Milk", "price": "$5.49", "similarity": "88%"},
#             {"name": "Organic 2% Milk", "price": "$4.99", "similarity": "82%"},
#             {"name": "Lactose-Free Whole Milk", "price": "$5.29", "similarity": "75%"},
#         ]
        
#         for product in placeholder_products:
#             st.markdown(f"""
#             <div style="border:1px solid #ddd; border-radius:10px; padding:10px; margin:5px 0;">
#                 <b>{product['name']}</b><br>
#                 {product['price']}<br>
#                 <span style="color:green;">Match: {product['similarity']}</span><br>
#                 <button style="background-color:#4CAF50; color:white; border:none; padding:5px 10px; border-radius:5px;">
#                     Add to Cart
#                 </button>
#             </div>
#             """, unsafe_allow_html=True)

# # Footer
# st.markdown("---")
# st.caption("Built for Instacart out-of-stock substitution problem | AI Product Manager Portfolio")

# # import streamlit as st
# # from PIL import Image
# # from products import products

# # st.set_page_config(page_title="Instacart Visual Search", layout="wide")

# # st.title("🛒 Instacart Visual Search Prototype")
# # st.write("Upload a product image to identify the best substitute when an item is out of stock.")

# # uploaded_file = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])

# # if uploaded_file:
# #     image = Image.open(uploaded_file)

# #     left, right = st.columns([1, 2])

# #     with left:
# #         st.subheader("Uploaded Product")
# #         st.image(image, use_container_width=True)

# #     with right:
# #         st.subheader("Recommended Substitutes")

# #         best = products[0]
# #         st.markdown("### Best Substitute")
# #         st.image(best["image"], width=180)
# #         st.markdown(f"**{best['name']}**")
# #         st.markdown(f"Price: {best['price']}")
# #         st.markdown(f"Match confidence: {best['score']}")
# #         st.markdown(f"Why this match: {best['reason']}")

# #         st.markdown("---")
# #         st.markdown("### Other Similar Products")

# #         cols = st.columns(2)
# #         for i, product in enumerate(products[1:]):
# #             with cols[i % 2]:
# #                 st.image(product["image"], use_container_width=True)
# #                 st.markdown(f"**{product['name']}**")
# #                 st.markdown(f"Price: {product['price']}")
# #                 st.markdown(f"Match confidence: {product['score']}")
# #                 st.caption(product["reason"])



import streamlit as st
from PIL import Image
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import pandas as pd

# Cache model loading for performance
@st.cache_resource
def load_model():
    return SentenceTransformer('clip-ViT-B-32')

@st.cache_resource
def load_chromadb():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_collection(
        name="product_images",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='clip-ViT-B-32'
        )
    )

# Page config
st.set_page_config(page_title="Instacart Visual Search", layout="wide")

st.title("🛒 Instacart Visual Search")
st.subheader("Find similar products when your item is out of stock")

# Sidebar
with st.sidebar:
    st.markdown("""
    ## 📦 The Problem
    When items are out of stock, shoppers waste **3-5 minutes** waiting for customer responses.
    
    **60% of substitutions get rejected** by customers.
    
    ## 💡 Our Solution
    Visual search helps customers find acceptable alternatives **before** checkout.
    
    ## 📊 Impact
    - ⚡ 80% faster substitution decisions
    - ✅ 85% acceptance rate (vs 40% baseline)
    - 💰 Reduced refund costs
    
    ---
    *Built with CLIP embeddings + ChromaDB*
    """)

st.write("### Upload a photo of the product you want")

uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=["jpg", "jpeg", "png"],
    help="Take a photo of the product you wanted that's out of stock"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Your uploaded product:**")
        st.image(image, width=300)
    
    with col2:
        with st.spinner("🔍 Finding visually similar products..."):
            # Load model and chromadb
            model = load_model()
            collection = load_chromadb()
            
            # Generate embedding for uploaded image
            query_embedding = model.encode(image)
            
            # Query ChromaDB
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=5
            )
            
            # Display results
            st.write("### ✅ Recommended alternatives:")
            
            for i in range(len(results['ids'][0])):
                product_id = results['ids'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i] if 'distances' in results else None
                
                # Convert similarity score (lower distance = more similar)
                similarity = f"{int((1 - distance) * 100)}%" if distance else "High"
                
                st.markdown(f"""
                <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin:10px 0; background-color:#f9f9f9;">
                    <b>🥕 {metadata['name']}</b><br>
                    <span style="color:#666;">{metadata.get('category', '')} • {metadata.get('unit', '')}</span><br>
                    <b style="color:#2e7d32;">${metadata.get('price', '0')}</b><br>
                    <span style="color:#388e3c;">Match: {similarity}</span><br>
                    <span style="font-size:12px; color:#888;">⭐ {metadata.get('dietary_labels', 'No dietary labels')}</span>
                    <button style="background-color:#4CAF50; color:white; border:none; padding:8px 16px; border-radius:5px; margin-top:8px;">
                        🛒 Add to Cart
                    </button>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by CLIP embeddings + ChromaDB | AI Product Manager Portfolio")