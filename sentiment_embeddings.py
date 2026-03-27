from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from typing import List, Dict
from news_social_fetcher import fetch_news_social

# Load FinBERT once
tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
model = AutoModel.from_pretrained('ProsusAI/finbert')

def get_finbert_embedding(text: str) -> np.ndarray:
    '''Get 768-dim embedding for financial text using FinBERT'''
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        # Pool [CLS] + mean pool
        cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()  # [1, 768]
        mean_pool = outputs.last_hidden_state.mean(dim=1).numpy()  # [1, 768]
        embedding = (cls_embedding + mean_pool) / 2
    return embedding.flatten()

def aggregate_embeddings(texts: List[Dict], method: str = 'mean') -> Dict:
    '''Aggregate embeddings for day/symbol'''
    if not texts:
        return {'embedding': np.zeros(768), 'count': 0, 'sentiment_score': 0.0}
    
    embeddings = []
    for text in texts:
        emb = get_finbert_embedding(text['text'])
        embeddings.append(emb)
    
    embeddings = np.array(embeddings)
    
    if method == 'mean':
        agg_emb = np.mean(embeddings, axis=0)
    elif method == 'max':
        agg_emb = np.max(embeddings, axis=0)
    
    # FinBERT sentiment logits (simplified)
    sentiment_score = np.mean([1 if 'positive' in text.get('sentiment', '').lower() else -1 for text in texts])
    
    return {
        'embedding': agg_emb,
        'raw_embeddings': embeddings.tolist(),
        'count': len(texts),
        'sentiment_score': float(sentiment_score)
    }

def get_daily_embeddings(symbol: str, date_str: str = None) -> Dict:
    '''Get embeddings for specific date/symbol'''
    data = fetch_news_social(symbol)
    all_texts = data['news'] + data['social']
    
    return aggregate_embeddings(all_texts)

if __name__ == '__main__':
    emb = get_daily_embeddings('RELIANCE.NS')
    print(f'Shape: {emb["embedding"].shape}')
    print(f'Sentiment: {emb["sentiment_score"]:.2f}')

