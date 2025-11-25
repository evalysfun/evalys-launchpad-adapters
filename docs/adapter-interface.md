# Launchpad Adapter Interface

## Overview

All launchpad adapters must implement a unified interface to ensure consistency and interoperability across different platforms.

## Interface Definition

### Base Interface

```python
class LaunchpadAdapter(ABC):
    """
    Abstract base class for launchpad adapters
    
    All adapters must implement:
    - fetchCurveState: Get current curve state
    - quoteBuy: Get buy quote with expected output
    - quoteSell: Get sell quote with expected output
    - buildBuyTx: Build buy transaction
    - buildSellTx: Build sell transaction
    - parseEvent: Parse transaction events
    """
    
    @property
    @abstractmethod
    def adapter_id(self) -> str:
        """Adapter identifier: 'pumpfun', 'bonkfun', etc."""
        pass
    
    @abstractmethod
    async def fetch_curve_state(self, mint: Pubkey) -> CurveState:
        """
        Fetch current bonding curve state
        
        Args:
            mint: Token mint address
            
        Returns:
            CurveState with current price, liquidity, supply, etc.
        """
        pass
    
    @abstractmethod
    async def quote_buy(self, args: BuyArgs) -> Quote:
        """
        Get buy quote (expected output, slippage)
        
        Args:
            args: BuyArgs with mint, sol_amount, slippage
            
        Returns:
            Quote with expected tokens, price impact, slippage
        """
        pass
    
    @abstractmethod
    async def quote_sell(self, args: SellArgs) -> Quote:
        """
        Get sell quote (expected output, slippage)
        
        Args:
            args: SellArgs with mint, token_amount, slippage
            
        Returns:
            Quote with expected SOL, price impact, slippage
        """
        pass
    
    @abstractmethod
    async def build_buy_tx(
        self,
        args: BuyArgs,
        cfg: Optional[PrivacyConfig] = None
    ) -> Transaction:
        """
        Build buy transaction
        
        Args:
            args: BuyArgs with mint, sol_amount, slippage
            cfg: Optional privacy config for stealth execution
            
        Returns:
            Transaction ready to sign and send
        """
        pass
    
    @abstractmethod
    async def build_sell_tx(
        self,
        args: SellArgs,
        cfg: Optional[PrivacyConfig] = None
    ) -> Transaction:
        """
        Build sell transaction
        
        Args:
            args: SellArgs with mint, token_amount, slippage
            cfg: Optional privacy config for stealth execution
            
        Returns:
            Transaction ready to sign and send
        """
        pass
    
    @abstractmethod
    async def parse_event(self, tx: ParsedTransaction) -> List[AdapterEvent]:
        """
        Parse transaction events
        
        Args:
            tx: Parsed transaction
            
        Returns:
            List of adapter events (buy, sell, etc.)
        """
        pass
    
    @abstractmethod
    async def simulate_tx(self, tx: Transaction) -> SimulationResult:
        """
        Simulate transaction before submission
        
        Args:
            tx: Transaction to simulate
            
        Returns:
            SimulationResult with success, logs, compute units, etc.
        """
        pass
```

## Data Models

### CurveState

```python
@dataclass
class CurveState:
    """Bonding curve state"""
    token_mint: Pubkey
    current_price: float          # Current price in SOL
    virtual_sol_reserves: float   # Virtual SOL reserves
    virtual_token_reserves: float # Virtual token reserves
    real_sol_reserves: float      # Real SOL reserves (if applicable)
    real_token_reserves: float    # Real token reserves (if applicable)
    total_supply: float           # Total token supply
    market_cap: float             # Estimated market cap
    timestamp: float              # State timestamp
```

### BuyArgs

```python
@dataclass
class BuyArgs:
    """Buy transaction arguments"""
    mint: Pubkey                  # Token mint address
    sol_amount: float            # Amount of SOL to spend
    slippage: float = 0.05       # Maximum slippage (default: 5%)
    buyer: Optional[Pubkey] = None # Buyer wallet (optional, for quote)
    deadline: Optional[int] = None  # Unix timestamp deadline
```

### SellArgs

```python
@dataclass
class SellArgs:
    """Sell transaction arguments"""
    mint: Pubkey                  # Token mint address
    token_amount: float          # Amount of tokens to sell
    slippage: float = 0.05       # Maximum slippage (default: 5%)
    seller: Optional[Pubkey] = None # Seller wallet (optional, for quote)
    deadline: Optional[int] = None  # Unix timestamp deadline
```

### Quote

```python
@dataclass
class Quote:
    """Transaction quote"""
    input_amount: float          # Input amount (SOL or tokens)
    output_amount: float         # Expected output amount
    price_impact: float          # Price impact percentage
    slippage: float              # Expected slippage
    fee: float                   # Transaction fee
    min_output: float            # Minimum output (with slippage)
    max_input: float             # Maximum input (with slippage)
    valid_until: Optional[int] = None # Quote expiration timestamp
```

### PrivacyConfig

```python
@dataclass
class PrivacyConfig:
    """Privacy configuration for stealth execution"""
    use_burner_wallet: bool = False  # Use burner wallet
    burner_pubkey: Optional[Pubkey] = None
    order_slicing: bool = False      # Slice order
    num_slices: Optional[int] = None
    timing_jitter_ms: int = 0        # Timing jitter
```

### AdapterEvent

```python
@dataclass
class AdapterEvent:
    """Parsed adapter event"""
    event_type: str              # "buy", "sell", "create", etc.
    mint: Pubkey                 # Token mint
    amount_in: float             # Input amount
    amount_out: float            # Output amount
    price: float                 # Execution price
    timestamp: float             # Event timestamp
    signature: str               # Transaction signature
```

### SimulationResult

```python
@dataclass
class SimulationResult:
    """Transaction simulation result"""
    success: bool                # Simulation succeeded
    logs: List[str]              # Simulation logs
    compute_units: int           # Compute units used
    account_changes: Dict        # Account changes
    error: Optional[str] = None  # Error message if failed
```

## Implementation Requirements

### Required Methods

All adapters must implement:

1. **fetch_curve_state**: Fetch current curve state from on-chain
2. **quote_buy**: Calculate buy quote without building transaction
3. **quote_sell**: Calculate sell quote without building transaction
4. **build_buy_tx**: Build complete buy transaction
5. **build_sell_tx**: Build complete sell transaction
6. **parse_event**: Extract events from parsed transaction
7. **simulate_tx**: Simulate transaction before submission

### Optional Methods

Adapters may implement:

- `get_token_info`: Get token metadata
- `get_historical_data`: Get historical curve data
- `validate_mint`: Validate token mint is valid for this launchpad

## Error Handling

All methods should:

- Raise `AdapterError` for adapter-specific errors
- Raise `RPCError` for RPC failures
- Raise `ValidationError` for invalid inputs
- Return appropriate error messages

## Testing Requirements

Each adapter must have:

- Unit tests for all methods
- Integration tests with real fixtures
- Golden tests comparing outputs to known-good transactions
- Simulation tests verifying transaction structure

## Versioning

Adapters should:

- Support version detection for program changes
- Handle backward compatibility when possible
- Document breaking changes in adapter README

