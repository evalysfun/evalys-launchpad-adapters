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
├── Base Adapter        # Unified adapter interface
├── Pump.fun Adapter    # Pump.fun implementation
│   ├── Program ID: 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P
│   ├── Buy/Sell instructions
│   └── Curve state fetching
├── Bonk.fun Adapter    # Bonk.fun implementation (in development)
│   └── Framework ready, awaiting program details
├── Generic Adapter     # Configurable adapter
└── Safety Layer        # Allowlists, validation, sanitization
```

**Adapter Interface**: All adapters implement:
- `fetch_curve_state`: Get current curve state
- `quote_buy` / `quote_sell`: Get quotes with slippage
- `build_buy_tx` / `build_sell_tx`: Build transactions
- `parse_event`: Extract events from transactions
- `simulate_tx`: Simulate before submission

See [Adapter Interface](docs/adapter-interface.md) for detailed specification.

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

### Implemented (v0.1)

- ✅ **Unified Adapter Interface**: Common interface for all adapters
- ✅ **Pump.fun Adapter**: 
  - ✅ Framework structure
  - ✅ Program ID: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - ✅ Buy/sell transaction building (framework)
  - ✅ Curve state fetching (framework)
  - ✅ Quote calculation (framework)
  - ✅ Safety features (allowlists, validation, sanitization)
- ✅ **Bonk.fun Adapter**: 
  - ✅ Framework structure
  - ⏳ Program ID: Awaiting details
  - ⏳ Full implementation: Planned
- ✅ **Safety Layer**: Allowlists, validation, sanitization
- ✅ **Documentation**: Adapter interface, compatibility matrix, adapter READMEs
- ✅ **Demo Scripts**: Pump.fun ghost buy, Bonk.fun ghost sell demos
- ✅ **Test Fixtures**: Placeholder fixtures for golden tests

### Planned

- ⏳ **Full Pump.fun Implementation**: Complete instruction building with real program interface
- ⏳ **Bonk.fun Implementation**: Full implementation when program details available
- ⏳ **Real Transaction Fixtures**: Capture and add real transaction fixtures
- ⏳ **Golden Tests**: Tests comparing outputs to known-good transactions
- ⏳ **Additional Launchpads**: Bags.fm, LetsBonk, etc.
- ⏳ **Multi-LP Normalization**: Unified interface across different LP models

**Note**: The adapters provide the framework and structure. Full implementation requires:
- Complete program IDLs and instruction details
- Proper account derivation and PDA calculation
- Instruction data serialization matching program format
- On-chain account parsing for curve state

## 🧪 Testing

```bash
# Run tests
pytest

# Run golden tests
pytest tests/test_golden.py

# With coverage
pytest --cov=src --cov-report=html
```

### Golden Tests

Golden tests verify adapter outputs match known-good transaction fixtures:

- **build_buy_tx_matches_fixture**: Built transaction matches fixture structure
- **parse_event_extracts_data**: Event parsing extracts correct mint/amounts
- **quote_matches_observed**: Quote calculation matches observed outputs

See `tests/test_golden.py` for details.

### Demo Scripts

Run adapter demos:

```bash
# Pump.fun ghost buy demo
python examples/pumpfun-ghost-buy.py

# Bonk.fun ghost sell demo
python examples/bonkfun-ghost-sell.py
```

These demonstrate the full adapter flow:
- Fetch curve state
- Get quote
- Build transaction
- Simulate transaction
- Privacy configuration

## 📦 Project Structure

```
evalys-launchpad-adapters/
├── src/
│   ├── adapters/       # Launchpad adapters
│   │   ├── base_adapter.py
│   │   ├── pumpfun_adapter.py
│   │   ├── pumpfun/
│   │   │   └── README.md      # Pump.fun program details
│   │   ├── bonkfun_adapter.py
│   │   ├── bonkfun/
│   │   │   └── README.md      # Bonk.fun program details
│   │   └── generic_adapter.py
│   ├── safety/         # Safety and compliance
│   │   ├── allowlist.py
│   │   ├── validator.py
│   │   └── sanitizer.py
│   ├── api/            # REST API
│   ├── config/         # Configuration
│   └── utils/          # Utilities
├── docs/
│   ├── adapter-interface.md  # Unified adapter interface
│   └── compatibility.md      # Compatibility matrix
├── examples/
│   ├── pumpfun-ghost-buy.py  # Pump.fun demo
│   └── bonkfun-ghost-sell.py # Bonk.fun demo
├── tests/
│   ├── fixtures/       # Transaction fixtures
│   │   └── pumpfun/
│   └── test_golden.py  # Golden tests
├── CHANGELOG.md
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

## 📚 Documentation

- **[Adapter Interface](docs/adapter-interface.md)**: Unified interface specification
- **[Compatibility Matrix](docs/compatibility.md)**: Program version compatibility
- **[Pump.fun README](src/adapters/pumpfun/README.md)**: Pump.fun program details
- **[Bonk.fun README](src/adapters/bonkfun/README.md)**: Bonk.fun implementation status
- **[Changelog](CHANGELOG.md)**: Version history

## 📊 Measurable Behavior

Instead of vague claims, here's what the adapters actually do:

**Unified Interface**:
- All adapters implement: `fetch_curve_state`, `quote_buy`, `quote_sell`, `build_buy_tx`, `build_sell_tx`, `parse_event`, `simulate_tx`
- Consistent data models: `CurveState`, `BuyArgs`, `SellArgs`, `Quote`, `AdapterEvent`

**Pump.fun Adapter**:
- Program ID: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
- Instructions: `buy`, `sell` with discriminators
- Accounts: 7 accounts (bonding curve PDA, token accounts, system program, etc.)
- PDA Derivation: `find_program_address(["bonding-curve", mint], program_id)`

**Quote Calculation**:
- Input: SOL amount or token amount
- Output: Expected tokens/SOL, price impact, slippage, fees
- Slippage protection: `min_output = output * (1 - slippage)`

**Transaction Building**:
- Instructions: Buy/sell instruction + compute budget + priority fee
- Accounts: All required accounts in correct order
- Simulation: Verify transaction before submission

See [Adapter Interface](docs/adapter-interface.md) and adapter READMEs for detailed specifications.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-launchpad-adapters/issues)
- **Documentation**: See `docs/` directory and adapter READMEs
- **Related Projects**: See below

## 🔗 Related Projects

- [evalys-privacy-engine](https://github.com/evalysfun/evalys-privacy-engine) - Privacy mode orchestration
- [evalys-burner-swarm](https://github.com/evalysfun/evalys-burner-swarm) - Burner wallet management
- [evalys-curve-intelligence](https://github.com/evalysfun/evalys-curve-intelligence) - Curve analysis
- [evalys-execution-engine](https://github.com/evalysfun/evalys-execution-engine) - Transaction execution

---

**Evalys Launchpad Adapters** - Unified interface with documented program details 🔌

