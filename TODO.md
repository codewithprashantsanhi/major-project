# Transformer-Based Market Movement Prediction with News & Social Media Sentiment Embeddings

## Progress Tracker

### ✅ 1. Setup Free Data Sources
   - Created news_social_fetcher.py (yfinance + mock)
   - Created mock_news_social.json
   - Created sentiment_embeddings.py (FinBERT)

### ✅ 2. Integrate Embeddings into Data Loader
   - Edited data_loader.py (+ sentiment features)
   - input_dim now auto 37+

### ✅ 3. Model & Retrain Ready
   - Model/train auto-handle
   - pip install -r requirements.txt (ollama added)
   - Run: python train.py RELIANCE.NS (retrain with embeddings)

### [ ] 4. Ollama Setup & Test
   - ollama serve
   - python test_llm.py

### [ ] 2. Sentiment Embeddings
   - Create sentiment_embeddings.py (FinBERT for embeddings)
   - Test: Extract 768-dim vectors from text

### [ ] 3. Update Data Pipeline
   - Edit data_loader.py: Add embeddings as features
   - input_dim: 26 tech → 26 + sentiment_dims (e.g., 768 mean-pooled → 30 selected)

### [ ] 4. Model Updates
   - Edit model.py: Handle new input_dim
   - Optional: Multi-modal attention for embeddings

### [ ] 5. Retrain
   - Update train.py config
   - python train.py

### [ ] 6. Ollama/LLM Setup
   - Check ollama serve running
   - Test llm_market_analyst.py
   - Update guides

### [ ] 7. Integration & Test
   - Update serve.py pipeline
   - Test API + frontend
   - Visualizations with embeddings attention

### [ ] 8. Documentation
   - Update README.md, AI_Market_Predictor_Presentation.md
   - Add EMBEDDINGS_GUIDE.md

**Current: Starting Step 1**
