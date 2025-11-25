# Launchpad Adapter Compatibility Matrix

## Overview

This document tracks compatibility between adapter versions and launchpad program versions.

## Compatibility Matrix

| Launchpad | Program ID | Program Version | Adapter Version | Last Verified | Status | Notes |
|-----------|------------|-----------------|-----------------|---------------|--------|-------|
| Pump.fun | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` | v1.0 | v0.1.0 | 2024-11-25 | ✅ Compatible | Mainnet tested |
| Bonk.fun | TBD | TBD | v0.1.0 | TBD | ⏳ Planned | Awaiting program details |

## Version History

### Pump.fun

| Program Version | Release Date | Adapter Compatibility | Breaking Changes |
|----------------|--------------|----------------------|------------------|
| v1.0 | 2024-01 | ✅ v0.1.0+ | None |

### Bonk.fun

| Program Version | Release Date | Adapter Compatibility | Breaking Changes |
|----------------|--------------|----------------------|------------------|
| TBD | TBD | ⏳ Planned | TBD |

## Testing Status

### Pump.fun

- ✅ **Buy Transactions**: Tested with real fixtures
- ✅ **Sell Transactions**: Tested with real fixtures
- ✅ **Curve State Fetching**: Tested on mainnet
- ✅ **Quote Calculation**: Verified against observed outputs
- ✅ **Transaction Building**: Golden tests passing

### Bonk.fun

- ⏳ **Buy Transactions**: Awaiting program details
- ⏳ **Sell Transactions**: Awaiting program details
- ⏳ **Curve State Fetching**: Awaiting program details
- ⏳ **Quote Calculation**: Awaiting program details
- ⏳ **Transaction Building**: Awaiting program details

## Known Issues

### Pump.fun

- None currently known

### Bonk.fun

- Program ID not yet available
- Instruction details not yet documented

## Update Schedule

- **Weekly**: Check for program updates
- **Monthly**: Verify compatibility with latest program versions
- **On Breaking Changes**: Update adapter and compatibility matrix immediately

## Verification Process

1. **Fetch Latest Program**: Get program ID and version from on-chain
2. **Test Transactions**: Run test suite with latest program
3. **Compare Outputs**: Verify transaction building matches expected format
4. **Update Matrix**: Update compatibility matrix with results
5. **Document Changes**: Note any breaking changes or new features

## Breaking Changes

### Pump.fun

None to date.

### Bonk.fun

N/A (not yet implemented)

## Migration Guide

### Pump.fun v1.0 → Future Version

When Pump.fun updates:

1. Check compatibility matrix for breaking changes
2. Update adapter code if needed
3. Run test suite
4. Update fixtures if transaction format changed
5. Update compatibility matrix

## Support

For compatibility questions or issues:

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-launchpad-adapters/issues)
- **Documentation**: See adapter READMEs in `src/adapters/`

