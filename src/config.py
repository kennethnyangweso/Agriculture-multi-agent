import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the Agriculture Multi-Agent system."""
    
    # ============================================
    # Paths
    # ============================================
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    PDF_DIR = os.path.join(DATA_DIR, 'agriculture_data')
    VECTOR_STORE_DIR = os.path.join(DATA_DIR, 'chroma_db')
    
    # ============================================
    # Model Settings
    # ============================================
    # Embedding model - supports English & Swahili
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # Groq settings
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast, high-quality model
    
    # ============================================
    # RAG Settings
    # ============================================
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVAL_K = 5
    
    # ============================================
    # Crop Terms for Detection
    # ============================================
    CROP_TERMS = [
        # English
        'maize', 'corn', 'bean', 'beans', 'coffee', 'tea', 'wheat', 
        'sweet potato', 'cassava', 'rice', 'sugarcane', 'tomato', 
        'onion', 'cabbage', 'kale', 'spinach', 'carrot', 'potato',
        'groundnut', 'peanut', 'sunflower', 'soya', 'soybean',
        # Swahili
        'mahindi', 'maharagwe', 'kahawa', 'chai', 'ngano', 
        'viazi', 'muhogo', 'mpunga', 'miwa', 'nyanya',
        'kitunguu', 'kabichi', 'sukuma', 'mchicha', 'karoti',
        'karanga', 'alizeti', 'soya'
    ]
    
    # ============================================
    # Disease Terms for Detection
    # ============================================
    DISEASE_TERMS = [
        # English
        'lethal necrosis', 'mln', 'rust', 'blight', 'wilt', 
        'spot', 'canker', 'mosaic', 'rot', 'mildew', 
        'anthracnose', 'smut', 'streak', 'mottle', 'curl',
        'leaf spot', 'downy mildew', 'powdery mildew', 'fusarium',
        'verticillium', 'bacterial', 'viral', 'fungal',
        'coccidiosis', 'newcastle', 'salmonella', 'fowl pox',
        'mastitis', 'foot and mouth', 'lumpy skin', 'anthrax',
        'brucellosis', 'east coast fever', 'ecf',
        # Swahili
        'ugonjwa', 'dalili', 'kutu', 'madoa', 'kuoza',
        'milozi', 'mildew', 'kichomi'
    ]
    
    # ============================================
    # Management Terms for Detection
    # ============================================
    MANAGEMENT_TERMS = [
        # English
        'fertilizer', 'fertilizers', 'pest', 'pesticide', 'insecticide',
        'fungicide', 'herbicide', 'treat', 'treatment', 'control',
        'manage', 'management', 'prevent', 'prevention', 'cure',
        'feed', 'feeding', 'nutrition', 'supplement', 'vaccination',
        'vaccinate', 'deworm', 'deworming', 'spray', 'application',
        'drench', 'inoculate', 'quarantine', 'isolation',
        # Swahili
        'mbolea', 'dawa', 'matibabu', 'kudhibiti', 'kuzuia',
        'lisha', 'lishe', 'chanjo', 'chanja', 'minyoo',
        'dawa ya wadudu', 'dawa ya kuvu'
    ]
    
    # ============================================
    # Domain Keywords for Routing
    # ============================================
    DOMAIN_KEYWORDS = {
        'crops': [
            # English
            'maize', 'corn', 'bean', 'beans', 'coffee', 'tea', 'wheat',
            'sweet potato', 'cassava', 'rice', 'sugarcane', 'tomato',
            'onion', 'cabbage', 'kale', 'spinach', 'carrot', 'potato',
            'groundnut', 'peanut', 'sunflower', 'soya', 'soybean',
            'crop', 'seed', 'fertilizer', 'pesticide', 'herbicide',
            'fungicide', 'harvest', 'plant', 'leaf', 'root', 'stem',
            'blight', 'rust', 'mosaic', 'wilt', 'rot', 'pest', 'weed',
            'insecticide', 'fungicide', 'herbicide',
            # Swahili
            'mahindi', 'maharagwe', 'kahawa', 'chai', 'ngano',
            'viazi', 'muhogo', 'mpunga', 'miwa', 'nyanya',
            'kitunguu', 'kabichi', 'sukuma', 'mchicha', 'karoti',
            'karanga', 'alizeti', 'soya', 'mazao', 'mbegu',
            'mbolea', 'dawa', 'mmea', 'jani', 'mzizi', 'mavuno',
            'wadudu', 'magugu', 'ugonjwa', 'dalili'
        ],
        'livestock': [
            # English
            'cattle', 'goat', 'sheep', 'cow', 'bull', 'calf', 'heifer',
            'milk', 'meat', 'beef', 'dairy', 'fodder', 'pasture',
            'silage', 'mastitis', 'foot and mouth', 'lumpy skin',
            'anthrax', 'brucellosis', 'vaccination', 'deworming',
            'breed', 'reproduction', 'calving', 'herd', 'livestock',
            # Swahili
            'ngombe', 'mbuzi', 'kondoo', 'ng\'ombe', 'ndama',
            'maziwa', 'nyama', 'malisho', 'chanjo', 'minyoo',
            'uzazi', 'mfugo'
        ],
        'poultry': [
            # English
            'chicken', 'egg', 'broiler', 'layer', 'kienyeji',
            'chick', 'poultry', 'coccidiosis', 'newcastle',
            'avian', 'salmonella', 'fowl', 'feed', 'coop',
            'hatchery', 'vaccination', 'flock', 'free-range',
            # Swahili
            'kuku', 'yai', 'mayai', 'kifaranga', 'ugonjwa',
            'dalili', 'matibabu', 'chanjo', 'lishe',
            'kuku wa kienyeji'
        ],
        'general': [
            # English
            'agriculture', 'farming', 'climate', 'weather', 'rainfall',
            'season', 'market', 'price', 'policy', 'loan',
            'cooperative', 'extension', 'training',
            # Swahili
            'kilimo', 'ukulima', 'shamba', 'hali ya hewa',
            'mvua', 'msimu', 'soko', 'bei', 'mkopo', 'ushirika'
        ]
    }
    
    # ============================================
    # Query Expansion Terms
    # ============================================
    QUERY_EXPANSIONS = {
        # Crops
        'maize': 'maize corn crop disease symptoms pest management farming agriculture fertilizer planting harvest',
        'corn': 'maize corn crop disease symptoms pest management farming agriculture fertilizer planting harvest',
        'mahindi': 'maize corn crop disease symptoms pest management farming agriculture fertilizer planting harvest',
        'bean': 'bean legume crop disease pest management farming agriculture fertilizer planting harvest',
        'beans': 'bean legume crop disease pest management farming agriculture fertilizer planting harvest',
        'maharagwe': 'bean legume crop disease pest management farming agriculture fertilizer planting harvest',
        'coffee': 'coffee berry disease leaf rust management farming fertilizer pruning harvesting',
        'kahawa': 'coffee berry disease leaf rust management farming fertilizer pruning harvesting',
        'tea': 'tea crop disease management farming fertilizer plucking harvesting',
        'chai': 'tea crop disease management farming fertilizer plucking harvesting',
        'wheat': 'wheat crop disease management farming fertilizer planting harvesting',
        'ngano': 'wheat crop disease management farming fertilizer planting harvesting',
        
        # Livestock
        'cattle': 'cattle livestock disease health management farming feeding breeding',
        'ngombe': 'cattle livestock disease health management farming feeding breeding',
        'goat': 'goat livestock disease health management farming feeding breeding',
        'mbuzi': 'goat livestock disease health management farming feeding breeding',
        'sheep': 'sheep livestock disease health management farming feeding breeding',
        'kondoo': 'sheep livestock disease health management farming feeding breeding',
        
        # Poultry
        'chicken': 'chicken poultry disease health management kuku feeding breeding vaccination',
        'kuku': 'chicken poultry disease health management feeding breeding vaccination',
        
        # Management
        'fertilizer': 'fertilizer fertilizer application crop nutrition soil fertility manure compost',
        'fertilizers': 'fertilizer fertilizer application crop nutrition soil fertility manure compost',
        'mbolea': 'fertilizer fertilizer application crop nutrition soil fertility manure compost',
        'pest': 'pest control management insecticide pesticide crop protection',
        'disease': 'disease symptoms signs diagnosis treatment control management prevention',
        'treat': 'treatment control management cure prevention remedy',
        'manage': 'management control treatment prevention farming practice',
    }
    
    # ============================================
    # Swahili Detection Words
    # ============================================
    SWAHILI_WORDS = [
        'ni', 'ya', 'wa', 'na', 'kwa', 'kwenye', 'shamba', 'mmea', 'mgonjwa',
        'mahindi', 'kuku', 'ngombe', 'mbuzi', 'samaki', 'nyuki', 'ugonjwa',
        'dalili', 'matibabu', 'mbolea', 'pembejeo', 'mavuno', 'kilimo',
        'mfugaji', 'mlima', 'ukulima', 'kifaranga', 'jinsi', 'gani'
    ]
    
    # ============================================
    # Groq Prompt Template - Always in English
    # ============================================
    # In src/config.py - Updated PROMPT_TEMPLATE

    PROMPT_TEMPLATE = """
You are an agricultural advisor for Kenyan farmers. Answer the question based on the information provided.

CONTEXT:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Answer in clear, simple English
- Be specific to Kenyan agriculture
- If the context has related information, use reasoning to provide a helpful answer
- Keep the answer concise (2-3 paragraphs max)
- Use bullet points where appropriate

ANSWER:
"""
