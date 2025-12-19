from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI()

# --- Funções Auxiliares ---
def _normalize_ticker(ticker: str) -> str:
    """Normaliza o ticker para o padrão da B3 (ex: PETR4 -> PETR4.SA)."""
    clean = ticker.upper().strip()
    if not clean.endswith(".SA"):
        clean += ".SA"
    return clean

# --- Rotas ---

@app.get("/health")
def health_check():
    """Endpoint de monitoramento de saúde."""
    return {"status": "ok", "service": "market-data-api"}

@app.get("/price/{ticker}")
def get_price(ticker: str):
    """Busca o preço de fechamento mais recente do ativo."""
    clean_ticker = _normalize_ticker(ticker)
    
    try:
        stock = yf.Ticker(clean_ticker)
        history = stock.history(period="1d")
        
        if history.empty:
            raise HTTPException(status_code=404, detail=f"Ticker '{clean_ticker}' não encontrado na B3.")
        
        current_price = float(history['Close'].iloc[-1])
        
        return {
            "ticker": clean_ticker,
            "price": round(current_price, 2),
            "source": "Yahoo Finance"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"Erro interno ao buscar preço: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados de mercado.")

@app.get("/info/{ticker}")
def get_info(ticker: str):
    """Retorna metadados do ativo (Setor, Moeda, Nome Longo)."""
    clean_ticker = _normalize_ticker(ticker)
        
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        
        return {
            "ticker": clean_ticker,
            "long_name": info.get("longName", "Desconhecido"),
            "sector": info.get("sector", "N/A"),
            "currency": info.get("currency", "BRL")
        }
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{ticker}")
def get_history(ticker: str):
    """Retorna o histórico de fechamento dos últimos 5 dias."""
    clean_ticker = _normalize_ticker(ticker)
    
    try:
        stock = yf.Ticker(clean_ticker)
        hist = stock.history(period="5d")
        
        if hist.empty:
             raise HTTPException(status_code=404, detail="Histórico indisponível.")

        # Serialização: Data (String) -> Preço (Float)
        history_dict = {str(date.date()): round(close, 2) for date, close in zip(hist.index, hist['Close'])}
        
        return {
            "ticker": clean_ticker,
            "period": "5d",
            "history": history_dict
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))