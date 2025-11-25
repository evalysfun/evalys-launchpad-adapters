# Pump.fun Adapter

## Overview

Adapter for interacting with Pump.fun bonding curve launchpad on Solana.

## Program Information

### Program ID

**Mainnet**: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

**Devnet**: Same program ID (Pump.fun uses same program on devnet)

### Program Version

- **Tested Version**: v1.0 (as of 2024-01)
- **Last Verified**: 2024-11-25
- **Status**: Active

## Instructions

### Buy Token

**Instruction Name**: `buy`

**Accounts Required**:
1. Bonding curve PDA (derived from token mint)
2. Associated token account (buyer's token account)
3. Associated SOL account (buyer's SOL account)
4. Token mint
5. System program
6. Token program
7. Buyer wallet (signer)

**Instruction Data**:
- `discriminator`: `[0x...]` (buy instruction discriminator)
- `sol_amount`: `u64` (amount in lamports)
- `min_tokens_out`: `u64` (minimum tokens expected, for slippage)

### Sell Token

**Instruction Name**: `sell`

**Accounts Required**:
1. Bonding curve PDA
2. Associated token account (seller's token account)
3. Associated SOL account (seller's SOL account)
4. Token mint
5. System program
6. Token program
7. Seller wallet (signer)

**Instruction Data**:
- `discriminator`: `[0x...]` (sell instruction discriminator)
- `token_amount`: `u64` (amount in tokens)
- `min_sol_out`: `u64` (minimum SOL expected, for slippage)

## Account Layout

### Bonding Curve Account

```
Offset | Size | Field
-------|------|------
0      | 32   | Token mint
32     | 8    | Virtual SOL reserves
40     | 8    | Virtual token reserves
48     | 8    | Real SOL reserves
56     | 8    | Real token reserves
64     | 8    | Total supply
...
```

### Token Metadata Account

```
Offset | Size | Field
-------|------|------
0      | 4    | Metadata discriminator
4      | 32   | Token mint
36     | 4    | Name length
40     | N    | Name (UTF-8)
...
```

## PDA Derivation

### Bonding Curve PDA

```python
from solders.pubkey import Pubkey
from solders.hash import Hash

def derive_bonding_curve_pda(token_mint: Pubkey, program_id: Pubkey) -> Pubkey:
    """Derive bonding curve PDA"""
    seeds = [
        b"bonding-curve",
        bytes(token_mint)
    ]
    # Use find_program_address
    pda, _ = Pubkey.find_program_address(seeds, program_id)
    return pda
```

## Known Edge Cases

1. **New Token Creation**: First buy creates the bonding curve account
2. **Complete Bonding Curve**: When curve completes, tokens migrate to Raydium
3. **Slippage Protection**: Always include min_tokens_out/min_sol_out
4. **Account Creation**: Associated token accounts may need creation

## Version Compatibility

| Pump.fun Version | Adapter Version | Status | Notes |
|------------------|-----------------|--------|-------|
| v1.0 | v0.1 | ✅ Compatible | Current version |
| Future | TBD | ⚠️ Unknown | Monitor for changes |

## Testing

### Test Fixtures

Located in `tests/fixtures/pumpfun/`:
- `buy_*.json`: Captured buy transaction fixtures
- `sell_*.json`: Captured sell transaction fixtures
- `curve_state_*.json`: Curve state snapshots

### Golden Tests

- `test_build_buy_tx_matches_fixture`: Build tx matches known-good transaction
- `test_parse_event_extracts_data`: Parse event extracts correct mint/amounts
- `test_quote_matches_observed`: Quote roughly matches observed curve output

## Resources

- **Pump.fun Website**: https://pump.fun
- **Program ID**: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
- **Documentation**: See adapter code for implementation details

