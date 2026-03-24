import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Create sample product catalog
products = [
    {"name": "Organic Whole Milk", "category": "Dairy", "price": 4.99, "unit": "1 gallon", "dietary": ["organic"]},
    {"name": "Grass-Fed Whole Milk", "category": "Dairy", "price": 5.49, "unit": "0.5 gallon", "dietary": ["grass-fed"]},
    {"name": "Almond Milk Unsweetened", "category": "Dairy Alternative", "price": 3.99, "unit": "0.5 gallon", "dietary": ["vegan", "dairy-free"]},
    {"name": "Oat Milk Barista Edition", "category": "Dairy Alternative", "price": 4.49, "unit": "0.5 gallon", "dietary": ["vegan"]},
    {"name": "Greek Yogurt Plain", "category": "Dairy", "price": 5.99, "unit": "32 oz", "dietary": ["high-protein"]},
    {"name": "Organic Strawberries", "category": "Produce", "price": 4.99, "unit": "1 lb", "dietary": ["organic"]},
    {"name": "Blueberries Fresh", "category": "Produce", "price": 3.99, "unit": "6 oz", "dietary": []},
    {"name": "Bananas Organic", "category": "Produce", "price": 1.99, "unit": "1 bunch", "dietary": ["organic"]},
    {"name": "Sourdough Bread", "category": "Bakery", "price": 4.49, "unit": "1 loaf", "dietary": ["vegan"]},
    {"name": "Whole Wheat Bread", "category": "Bakery", "price": 3.49, "unit": "1 loaf", "dietary": ["vegan"]},
    {"name": "Free Range Eggs", "category": "Eggs", "price": 5.99, "unit": "12 count", "dietary": ["cage-free"]},
    {"name": "Organic Eggs", "category": "Eggs", "price": 6.49, "unit": "12 count", "dietary": ["organic"]},
    {"name": "Cheddar Cheese Block", "category": "Cheese", "price": 4.99, "unit": "8 oz", "dietary": []},
    {"name": "Mozzarella Cheese", "category": "Cheese", "price": 3.99, "unit": "8 oz", "dietary": []},
    {"name": "Chicken Breast Boneless", "category": "Meat", "price": 7.99, "unit": "1 lb", "dietary": ["high-protein"]},
    {"name": "Salmon Fillet", "category": "Seafood", "price": 12.99, "unit": "1 lb", "dietary": ["omega-3"]},
    {"name": "Coffee Beans Medium Roast", "category": "Beverages", "price": 9.99, "unit": "12 oz", "dietary": ["vegan"]},
    {"name": "Green Tea Bags", "category": "Beverages", "price": 3.99, "unit": "20 count", "dietary": ["vegan"]},
    {"name": "Potato Chips Classic", "category": "Snacks", "price": 3.49, "unit": "8 oz", "dietary": []},
    {"name": "Dark Chocolate Bar", "category": "Snacks", "price": 2.99, "unit": "3.5 oz", "dietary": ["vegan"]},
]

# Generate simple colored images for each product (for demo)
def create_placeholder_image(product_name, color):
    img = Image.new('RGB', (300, 300), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    text = product_name[:20]  # Truncate long names
    try:
        draw.text((20, 140), text, fill='white')
    except:
        pass
    
    return img

# Colors for different categories
colors = {
    "Dairy": (100, 150, 200),
    "Dairy Alternative": (150, 180, 150),
    "Produce": (100, 180, 100),
    "Bakery": (200, 160, 100),
    "Eggs": (220, 200, 120),
    "Cheese": (210, 170, 100),
    "Meat": (180, 100, 100),
    "Seafood": (130, 170, 200),
    "Beverages": (140, 100, 160),
    "Snacks": (200, 130, 100),
}

# Generate images and create catalog
catalog_data = []
for i, product in enumerate(products):
    # Get color for category
    color = colors.get(product["category"], (150, 150, 150))
    
    # Create image
    img = create_placeholder_image(product["name"], color)
    
    # Save image
    filename = f"product_{i:03d}.jpg"
    img.save(f"images/{filename}")
    
    # Add to catalog
    catalog_data.append({
        "product_id": i,
        "name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "unit": product["unit"],
        "dietary_labels": ", ".join(product["dietary"]) if product["dietary"] else "",
        "image_filename": filename
    })

# Save catalog to CSV
df = pd.DataFrame(catalog_data)
df.to_csv("data/grocery_catalog.csv", index=False)

print(f"✅ Created {len(products)} product images in 'images/' folder")
print(f"✅ Saved catalog to 'data/grocery_catalog.csv'")
print("\nProducts created:")
for p in products[:5]:
    print(f"  - {p['name']}")
print(f"  ... and {len(products)-5} more")