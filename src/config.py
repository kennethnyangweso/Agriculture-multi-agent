import os

class Config:
    """Configuration settings for the Agriculture Multi-Agent System (AgriMAS) project."""

    # Paths

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    PDF_DIR = os.path.join(DATA_DIR, 'pdfs')
    VECTOR_STORE_DIR = os.path.join(DATA_DIR, 'chroma_db')

    # Model settings( Supports English and Swahili)

    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # Embedding model for vector representation

    # RAG settings
    CHUNK_SIZE = 1000  # Size of text chunks for retrieval
    CHUNK_OVERLAP = 200  # Overlap size between text chunks
    RETRIEVAL_TOP_K = 5  # Number of top documents to retrieve for RAG  

    # Swahi detection words

    SWAHILI_WORDS = [
        'ni', 'ya', 'wa', 'na', 'kwa', 'kwenye', 'shamba', 'mmea', 'mgonjwa',
        'mahindi', 'kuku', 'ngombe', 'mbuzi', 'samaki', 'nyuki', 'ugonjwa',
        'dalili', 'matibabu', 'mbolea', 'pembejeo', 'mavuno', 'kilimo',
        'mfugaji', 'mlima', 'ukulima', 'kifaranga', 'jinsi', 'gani'
    ]

    # Domain keywords (English and Swahili)

    DOMAIN_KEYWORDS = {
        'crops': [
            'maize', 'bean', 'wheat', 'coffee', 'tea', 'crop', 'seed', 'fertilizer',
            'pesticide', 'harvest', 'plant', 'leaf', 'root', 'stem', 'blight', 'rust',
            'mahindi', 'maharagwe', 'kahawa', 'chai', 'mbegu', 'mbolea', 'dawa',
            'mmea', 'jani', 'mzizi', 'mavuno', 'ugonjwa', 'wadudu'
        ],
        'livestock': [
            'cattle', 'goat', 'sheep', 'cow', 'bull', 'calf', 'milk', 'meat',
            'fodder', 'pasture', 'herd', 'mastitis', 'foot and mouth',
            'ngombe', 'mbuzi', 'kondoo', 'nyama', 'maziwa', 'malisho',
            'ugonjwa', 'ng\'ombe', 'ndama'
        ],
        'poultry': [
            'chicken', 'egg', 'broiler', 'layer', 'kienyeji', 'chick', 'poultry',
            'coccidiosis', 'newcastle', 'fowl', 'salmonella', 'kuku', 'yai',
            'kifaranga', 'mayai', 'kienyeji', 'ugonjwa'
        ],
        'general': [
            'agriculture', 'farming', 'climate', 'weather', 'market', 'price',
            'kilimo', 'shamba', 'hali ya hewa', 'soko', 'bei'
        ]
    }
