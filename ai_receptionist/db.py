from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from ai_receptionist.chatgpt import gpt_response

client = QdrantClient("http://localhost:6333")

def setup_emergency_collection():
    client.recreate_collection(
        collection_name="emergencies",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

def add_emergency_data():
    emergencies = {
        "not breathing": "Start CPR immediately. CPR involves chest compressions and rescue breathing",
        "bleeding": "Apply pressure to the wound and keep the injured area elevated",
    }

    points = []
    for idx, (description, response) in enumerate(emergencies.items()):
        vector = get_vector(description)
        vector = pad_or_truncate_vector(vector)
        
        points.append(PointStruct(id=idx, vector=vector, payload={"description": description, "response": response}))

    client.upsert(collection_name="emergencies", points=points)

def get_vector(text):
    return gpt_response(text)

def pad_or_truncate_vector(vector):
    target_size = 768
    if len(vector) < target_size:
        return vector + [0] * (target_size - len(vector))
    elif len(vector) > target_size:
        return vector[:target_size]
    return vector

def query_emergency_db(emergency_description):
    vector = get_vector(emergency_description)
    vector = pad_or_truncate_vector(vector)
    
    response = client.search(
        collection_name="emergencies",
        query_vector=vector,
        limit=1,
    )
    
    if response and len(response) > 0:
        return response[0].payload["response"]
    else:
        return "Sorry, I don't have instructions for that emergency."
    
def close_db():
    client.close()

setup_emergency_collection()
add_emergency_data()
