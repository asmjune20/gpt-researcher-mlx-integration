# GPT-Researcher MLX Integration

This is a fork of [GPT-Researcher](https://github.com/assafelovic/gpt-researcher) with integrated support for Apple's MLX framework, enabling **100% local AI research** with no external API dependencies.

## 🎯 Features

- **Local LLM Inference**: Uses Apple's MLX framework for fast, local AI processing
- **Zero API Costs**: No OpenAI API calls = completely free operation
- **Complete Privacy**: All data processing happens locally on your machine
- **Fast Performance**: Leverages Apple Silicon for optimal performance
- **Minimal Changes**: Only 1 file modified from original GPT-Researcher

## 🏗️ Architecture

```
MLX Server (localhost:8000) ← GPT-Researcher ← Web UI (localhost:3000)
     ↓
Local Mistral-7B Model
```

## 📋 Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.11+
- MLX framework installed
- GPT-Researcher dependencies

## 🚀 Quick Start

### 1. Set up MLX Server
```bash
# Install MLX LM
pip install mlx-lm

# Start MLX server (in a separate terminal)
mlx_lm.server --model mlx-community/Mistral-7B-Instruct-v0.3-4bit --host 0.0.0.0 --port 8000
```

### 2. Configure GPT-Researcher
Create a `.env` file with:
```bash
# MLX Server Configuration
OPENAI_BASE_URL="http://localhost:8000/v1"
OPENAI_API_KEY="dummy_key_not_needed"

# LLM Configuration (MUST use provider:model format)
FAST_LLM="openai:mlx-community/Mistral-7B-Instruct-v0.3-4bit"
SMART_LLM="openai:mlx-community/Mistral-7B-Instruct-v0.3-4bit"
STRATEGIC_LLM="openai:mlx-community/Mistral-7B-Instruct-v0.3-4bit"

# Search & Embeddings
RETRIEVER="duckduckgo"
EMBEDDING="huggingface:all-MiniLM-L6-v2"

# Other Settings
TEMPERATURE="0.7"
MAX_TOKENS="1024"
LLM_PROVIDER="openai"
```

### 3. Start GPT-Researcher
```bash
# Load environment variables
source .env

# Start the server
python -m uvicorn backend.server.server:app --host=0.0.0.0 --port=3000 --reload
```

### 4. Access Web UI
Open http://localhost:3000 in your browser and start researching!

## 🔧 Technical Details

### Modified Files
- `gpt_researcher/actions/agent_creator.py`: Added MLX message format compatibility

### Why the Modification?
MLX servers work better with combined user messages rather than separate system/user roles. The modification detects local servers and adjusts the message format accordingly.

**Original Format (doesn't work well with MLX):**
```json
{
  "messages": [
    {"role": "system", "content": "You are a research assistant..."},
    {"role": "user", "content": "task: Research topic"}
  ]
}
```

**MLX-Compatible Format:**
```json
{
  "messages": [
    {"role": "user", "content": "You are a research assistant...\n\ntask: Research topic"}
  ]
}
```

## 📊 Performance

- **Speed**: ~17.5 tokens/second on Apple Silicon
- **Memory**: ~5.2GB peak usage
- **Cost**: $0.00 (completely free)
- **Privacy**: 100% local processing

## 🔍 Comparison with Original

| Feature | Original GPT-Researcher | MLX Integration |
|---------|------------------------|-----------------|
| LLM Provider | OpenAI API | Local MLX Server |
| Cost per Research | ~$0.01-0.10 | $0.00 |
| Privacy | Data sent to OpenAI | 100% local |
| Speed | API latency | 17.5 tokens/sec |
| Dependencies | OpenAI API key | MLX framework |

## 🐛 Troubleshooting

### Common Issues

1. **"ValueError: not enough values to unpack (expected 2, got 1)"**
   - Ensure LLM config uses `provider:model` format
   - Example: `FAST_LLM="openai:mlx-community/Mistral-7B-Instruct-v0.3-4bit"`

2. **Environment variables not loading**
   - Run `source .env` before starting the server
   - Verify with: `echo $FAST_LLM`

3. **MLX server not responding**
   - Check MLX server is running on port 8000
   - Test with: `curl http://localhost:8000/v1/models`

## 🤝 Contributing

This integration maintains compatibility with the original GPT-Researcher while adding MLX support. Submit issues or PRs to improve the MLX integration.

## 📄 License

Same as original GPT-Researcher project.

## 🙏 Acknowledgments

- Original [GPT-Researcher](https://github.com/assafelovic/gpt-researcher) project
- Apple's [MLX](https://github.com/ml-explore/mlx) framework
- The open-source AI community 