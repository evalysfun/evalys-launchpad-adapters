# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Shared Virtual Environment (Recommended)

Since Evalys uses multiple components, use a **shared virtual environment** at the root level:

```bash
# From evalys root directory (if not already set up)
venv\Scripts\Activate.ps1  # Windows PowerShell
$env:PYTHONPATH = "."

# Navigate to launchpad adapters directory
cd evalys-launchpad-adapters

# Install dependencies
pip install -r requirements.txt
```

**Note**: The shared venv approach avoids duplication. All Evalys components share the same environment.

### 2. Run Example

```bash
# Make sure you're in evalys-launchpad-adapters directory
# and venv is activated with PYTHONPATH set
python example.py
```

This will demonstrate the adapter framework.

### 3. Use as Python Library

```python
import asyncio
from src.adapters.pumpfun_adapter import PumpFunAdapter
from solders.pubkey import Pubkey

async def main():
    adapter = PumpFunAdapter(rpc_url="https://api.devnet.solana.com")
    
    try:
        # Get program ID
        program_id = adapter.get_program_id()
        print(f"Program ID: {program_id}")
    finally:
        await adapter.disconnect()

asyncio.run(main())
```

### 4. Run as API Server

```bash
# Start the API server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8002 --reload
```

Then visit:
- API Docs: http://localhost:8002/docs
- Health Check: http://localhost:8002/health

### 5. Test API

```bash
# Get supported launchpads
curl "http://localhost:8002/api/v1/launchpad/launchpads"

# Get token info (placeholder)
curl "http://localhost:8002/api/v1/launchpad/token-info/pumpfun/TOKEN_MINT"
```

### 6. Run Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

## 📚 Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check out the [example.py](example.py) for more usage examples
- Explore the API at http://localhost:8002/docs when server is running
- **Implement actual instruction building** for Pump.fun/Bonk.fun

## 🐛 Troubleshooting

### Import Errors
Make sure:
1. Virtual environment is activated
2. PYTHONPATH is set (see step 1)
3. You're in the evalys-launchpad-adapters directory

### Not Implemented Errors
The adapters provide the **framework**. Actual instruction building needs to be implemented based on:
- Pump.fun/Bonk.fun program IDLs
- Account derivation
- Instruction data serialization

### Module Not Found
Make sure:
1. Virtual environment is activated
2. PYTHONPATH is set (see step 1)
3. You're in the evalys-launchpad-adapters directory

```bash
# Verify PYTHONPATH is set
echo $env:PYTHONPATH  # Windows PowerShell
# or
echo $PYTHONPATH      # Linux/Mac

# Run from component directory
python -m src.api.server
```

## 📝 Implementation Notes

This adapter provides:
- ✅ Framework structure
- ✅ Safety features (allowlists, validation)
- ✅ Unified interface
- ⚠️ **Needs**: Actual instruction building implementation

To complete the implementation, you'll need:
1. Pump.fun program IDL
2. Bonk.fun program IDL
3. Account derivation logic
4. Instruction data serialization
5. On-chain account parsing

