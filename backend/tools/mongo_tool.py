from pymongo import MongoClient
from typing import Dict, Any, List
from core.config import settings
import json
from datetime import datetime


class MongoTool:
    """Execute MongoDB queries"""
    
    def __init__(self):
        self.name = "mongo"
        self.description = """Query MongoDB database.
Supports find() and aggregate() operations.
Input format: 
  For find: {"collection": "name", "query": {...}, "limit": 100}
  For aggregate: {"collection": "name", "pipeline": [...]}
Returns: Query results as JSON"""
        
        try:
            self.client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[settings.mongo_db]
            # Test connection
            self.client.server_info()
            self.connected = True
        except Exception as e:
            print(f"MongoDB connection failed: {str(e)}")
            self.connected = False
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute MongoDB query"""
        if not self.connected:
            return {"error": "MongoDB not connected. Check MONGO_URI in .env"}
        
        collection_name = input_data.get("collection")
        if not collection_name:
            return {"error": "Collection name required"}
        
        try:
            collection = self.db[collection_name]
            
            # Check if this is an aggregation pipeline
            if "pipeline" in input_data:
                pipeline = input_data["pipeline"]
                results = list(collection.aggregate(pipeline))
            else:
                # Regular find query
                query = input_data.get("query", {})
                limit = input_data.get("limit", 100)
                projection = input_data.get("projection")
                
                cursor = collection.find(query, projection).limit(limit)
                results = list(cursor)
            
            # Convert ObjectId and datetime to strings
            results = self._serialize_results(results)
            
            return {
                "success": True,
                "count": len(results),
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"MongoDB error: {str(e)}"
            }
    
    def _serialize_results(self, results: List[Dict]) -> List[Dict]:
        """Convert MongoDB results to JSON-serializable format"""
        from bson import ObjectId
        
        def convert_value(val):
            if isinstance(val, ObjectId):
                return str(val)
            elif isinstance(val, datetime):
                return val.isoformat()
            elif isinstance(val, dict):
                return {k: convert_value(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [convert_value(v) for v in val]
            return val
        
        return [convert_value(doc) for doc in results]


# Global instance
mongo_tool = MongoTool()
