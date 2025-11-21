bashio::log.info "Iniciando el servidor FastAPI (LLM)..."

exec uvicorn server:app --host 0.0.0.0 --port 8000