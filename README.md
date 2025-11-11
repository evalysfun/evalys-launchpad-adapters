# Evalys Launchpad Adapters

Launchpad adapters for Pump.fun, Bonk.fun, and other memecoin launchpad platforms.

## 🎯 Overview

The Launchpad Adapters provide a unified interface for interacting with different memecoin launchpads:
- **Pump.fun** - Full adapter (framework ready)
- **Bonk.fun** - Adapter structure (needs implementation)
- **Generic** - Configurable adapter for other platforms

## ✨ Features

- 🔌 **Unified Interface**: Same API for all launchpads
- 🛡️ **Safety First**: Allowlists, validation, and compliance
- 🧹 **Behavior Sanitization**: Removes identifying patterns
- 🔄 **Easy Extension**: Add new launchpads easily
- 🌐 **REST API**: Full API for integration
- 📦 **Standalone**: Can be used independently

## 🚀 Installation

### From Source (Recommended: Shared Virtual Environment)

For the Evalys ecosystem, use a **shared virtual environment** at the root level:

```bash
# From evalys root directory (if not already set up)
venv\Scripts\Activate.ps1  # Windows PowerShell
$env:PYTHONPATH = "."

# Navigate to component directory
cd evalys-launchpad-adapters

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

**Note**: Using a shared venv at the root avoids duplication. All Evalys components share the same environment.

### Standalone Installation

If using this component independently:

```bash
git clone https://github.com/evalysfun/evalys-launchpad-adapters
cd evalys-launchpad-adapters
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

## 📖 Usage

### As Python Library

```python
import asyncio
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from src.adapters.pumpfun_adapter import PumpFunAdapter

async def main():
    # Initialize adapter
    adapter = PumpFunAdapter(rpc_url="https://api.devnet.solana.com")
    
    try:
        # Get token info
        token_mint = Pubkey.from_string("...")
        token_info = await adapter.get_token_info(token_mint)
        
        # Get curve data
        curve_data = await adapter.get_curve_data(token_mint)
        
        # Build buy transaction
        wallet = Keypair()  # Your wallet
        transaction = await adapter.buy_token(
            wallet,
            token_mint,
            sol_amount=0.1,
            slippage=0.05
        )
        
        # Transaction is ready to sign and send
    finally:
        await adapter.disconnect()

asyncio.run(main())
```

### As REST API

```bash
# Start the API server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8002
```

#### API Endpoints

- `POST /api/v1/launchpad/buy-token` - Build buy transaction
- `POST /api/v1/launchpad/sell-token` - Build sell transaction
- `GET /api/v1/launchpad/curve-data/{launchpad}/{token_mint}` - Get curve data
- `GET /api/v1/launchpad/token-info/{launchpad}/{token_mint}` - Get token info
- `GET /api/v1/launchpad/launchpads` - List supported launchpads
- `GET /health` - Health check

#### Example API Request

```bash
# Get curve data
curl "http://localhost:8002/api/v1/launchpad/curve-data/pumpfun/TOKEN_MINT"

# Get supported launchpads
curl "http://localhost:8002/api/v1/launchpad/launchpads"
```

## 🏗️ Architecture

```
Launchpad Adapters
├── Base Adapter        # Abstract interface
├── Pump.fun Adapter    # Pump.fun implementation
├── Bonk.fun Adapter    # Bonk.fun implementation
├── Generic Adapter     # Configurable adapter
└── Safety Layer        # Allowlists, validation, sanitization
```

## 🛡️ Safety Features

### Allowlist Management
Only interact with approved programs:
```python
from src.safety.allowlist import AllowlistManager

allowlist = AllowlistManager()
allowlist.add_program(program_id)
```

### Instruction Validation
Validate all instructions before execution:
```python
from src.safety.validator import InstructionValidator

validator = InstructionValidator()
validator.validate_instruction(instruction, expected_program)
```

### Behavior Sanitization
Remove identifying patterns:
```python
from src.safety.sanitizer import BehaviorSanitizer

sanitizer = BehaviorSanitizer()
clean_instruction = sanitizer.sanitize_instruction(instruction)
```

## 🔧 Configuration

Set environment variables:

```bash
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
export PUMP_FUN_PROGRAM_ID=6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P
export API_HOST=0.0.0.0
export API_PORT=8002
```

## 📝 Implementation Status

### Pump.fun Adapter
- ✅ Framework structure
- ✅ Safety features
- ⚠️ Instruction building (needs actual Pump.fun program interface)
- ⚠️ On-chain data fetching (needs implementation)

### Bonk.fun Adapter
- ✅ Framework structure
- ⚠️ Full implementation needed

### Generic Adapter
- ✅ Framework structure
- ⚠️ Configuration-based implementation needed

**Note**: The adapters provide the framework and structure. Actual instruction building requires:
- Pump.fun/Bonk.fun program IDLs
- Proper account derivation
- Instruction data serialization
- On-chain account parsing

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

## 📦 Project Structure

```
evalys-launchpad-adapters/
├── src/
│   ├── adapters/       # Launchpad adapters
│   │   ├── base_adapter.py
│   │   ├── pumpfun_adapter.py
│   │   ├── bonkfun_adapter.py
│   │   └── generic_adapter.py
│   ├── safety/         # Safety and compliance
│   │   ├── allowlist.py
│   │   ├── validator.py
│   │   └── sanitizer.py
│   ├── api/            # REST API
│   ├── config/         # Configuration
│   └── utils/          # Utilities
├── tests/              # Tests
├── requirements.txt
├── setup.py
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines first.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [evalys-privacy-engine](https://github.com/evalysfun/evalys-privacy-engine) - Privacy mode orchestration
- [evalys-burner-swarm](https://github.com/evalysfun/evalys-burner-swarm) - Burner wallet management
- [evalys-curve-intelligence](https://github.com/evalysfun/evalys-curve-intelligence) - Curve analysis
- [evalys-execution-engine](https://github.com/evalysfun/evalys-execution-engine) - Transaction execution

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-launchpad-adapters/issues)
- **Discord**: [Coming Soon]

---

**Evalys Launchpad Adapters** - Unified interface for memecoin launchpads 🔌

