.PHONY: dev

dev:
	tmux new-session -A -s rag-service 'source .venv/bin/activate && uvicorn api.main:app --reload'

down:
	tmux kill-session -t rag-service