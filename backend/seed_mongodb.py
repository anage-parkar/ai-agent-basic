"""
MongoDB Sample Data Seeder
Run this script to populate your MongoDB with sample data for testing
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "analytics"

def seed_events_collection():
    """Seed the events collection with sample data"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    events = db.events
    
    # Clear existing data
    print("Clearing existing events...")
    events.delete_many({})
    
    # Generate sample data
    print("Generating sample events...")
    
    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Clothing", "Food", "Books", "Sports"]
    products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    
    documents = []
    
    # Generate 365 days of data (full year 2025)
    start_date = datetime(2025, 1, 1)
    
    for day in range(365):
        current_date = start_date + timedelta(days=day)
        
        # Generate 10-30 events per day
        num_events = random.randint(10, 30)
        
        for _ in range(num_events):
            event = {
                "ts": current_date + timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                ),
                "amount": round(random.uniform(10, 500), 2),
                "region": random.choice(regions),
                "category": random.choice(categories),
                "product": random.choice(products),
                "quantity": random.randint(1, 10),
                "customer_id": f"CUST{random.randint(1000, 9999)}",
                "status": random.choice(["completed", "pending", "cancelled"])
            }
            documents.append(event)
    
    # Insert all documents
    print(f"Inserting {len(documents)} events...")
    events.insert_many(documents)
    
    # Create indexes for better query performance
    print("Creating indexes...")
    events.create_index("ts")
    events.create_index("region")
    events.create_index("category")
    
    print(f"✓ Successfully seeded {len(documents)} events")
    print(f"  Date range: {start_date.date()} to {(start_date + timedelta(days=364)).date()}")
    print(f"  Total revenue: ${sum(doc['amount'] for doc in documents):,.2f}")
    
    # Show sample query
    print("\nSample query to try:")
    print("""
{
  "collection": "events",
  "pipeline": [
    {"$match": {"ts": {"$gte": {"$date": "2025-01-01"}, "$lte": {"$date": "2025-12-31"}}}},
    {"$group": {
      "_id": {
        "month": {"$month": "$ts"},
        "region": "$region"
      },
      "revenue": {"$sum": "$amount"},
      "orders": {"$sum": 1}
    }},
    {"$sort": {"_id.month": 1}}
  ]
}
    """)


def seed_users_collection():
    """Seed a users collection with sample data"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users = db.users
    
    print("\nSeeding users collection...")
    users.delete_many({})
    
    first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
    
    user_docs = []
    for i in range(100):
        user = {
            "user_id": f"USER{1000+i}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "email": f"user{i}@example.com",
            "age": random.randint(18, 70),
            "signup_date": datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365)),
            "total_spent": round(random.uniform(100, 5000), 2),
            "orders_count": random.randint(1, 50),
            "region": random.choice(["North", "South", "East", "West"]),
            "premium": random.choice([True, False])
        }
        user_docs.append(user)
    
    users.insert_many(user_docs)
    users.create_index("user_id", unique=True)
    users.create_index("email", unique=True)
    
    print(f"✓ Successfully seeded {len(user_docs)} users")


if __name__ == "__main__":
    print("🌱 MongoDB Sample Data Seeder")
    print("=" * 50)
    
    try:
        # Test connection
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        print(f"✓ Connected to MongoDB at {MONGO_URI}")
        print(f"  Database: {DB_NAME}\n")
        
        # Seed collections
        seed_events_collection()
        seed_users_collection()
        
        print("\n" + "=" * 50)
        print("✨ All done! Your database is ready for testing.")
        print("\nYou can now query this data using the DataPilot agent!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure MongoDB is running:")
        print("  brew services start mongodb-community  # macOS")
        print("  sudo systemctl start mongod            # Linux")
        print("  # Or run: mongod --dbpath /path/to/data")
