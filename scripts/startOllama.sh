curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
pid=$!

while ! pgrep -f "ollama"; do
  sleep 0.1
done

sleep 15
ollama pull llama3.2
ollama pull qwen2.5:7b
ollama list

echo Ollama is ready.
