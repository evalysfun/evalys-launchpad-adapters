"""
Example usage of Evalys Launchpad Adapters
"""

import asyncio
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from src.adapters.pumpfun_adapter import PumpFunAdapter
from src.safety.allowlist import AllowlistManager


async def main():
    """Example usage"""
    print("=" * 60)
    print("Evalys Launchpad Adapters - Example")
    print("=" * 60)
    
    # Initialize adapter
    adapter = PumpFunAdapter(rpc_url="https://api.devnet.solana.com")
    
    try:
        # Example 1: Get adapter info
        print("\n📋 Example 1: Adapter Information")
        program_id = adapter.get_program_id()
        print(f"   Program ID: {program_id}")
        print(f"   RPC URL: {adapter.rpc_url}")
        print(f"   Validates program: {adapter.validate_program(program_id)}")
        
        # Example 2: Get token info
        print("\n📋 Example 2: Get Token Info")
        # Use actual token mint address for real data
        token_mint = Pubkey.from_string("11111111111111111111111111111111")
        try:
            token_info = await adapter.get_token_info(token_mint)
            print(f"   Token Mint: {token_info.mint}")
            print(f"   Symbol: {token_info.symbol}")
            print(f"   Name: {token_info.name}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Example 3: Get curve data
        print("\n📋 Example 3: Get Curve Data")
        try:
            curve_data = await adapter.get_curve_data(token_mint)
            print(f"   Token Mint: {curve_data.token_mint}")
            print(f"   Current Price: {curve_data.current_price} SOL")
            print(f"   Liquidity: {curve_data.liquidity}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Example 4: Safety features
        print("\n📋 Example 4: Safety Features")
        allowlist = AllowlistManager()
        allowlist.add_program(program_id)
        print(f"   Program in allowlist: {allowlist.is_allowed(program_id)}")
        print(f"   Allowed programs: {len(allowlist.get_allowed_programs())}")
        
        # Example 5: Build transaction (would require real token)
        print("\n📋 Example 5: Transaction Building")
        print("   Note: Transaction building requires:")
        print("   - Real token mint address")
        print("   - Funded wallet")
        print("   - Proper instruction building (TODO: implement)")
        print("   This is a framework - actual instruction building needs implementation")
        
    finally:
        await adapter.disconnect()
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("=" * 60)
    print("\n📝 Note: This adapter provides the framework.")
    print("   Actual Pump.fun/Bonk.fun instruction building needs to be")
    print("   implemented based on their program interfaces.")


if __name__ == "__main__":
    asyncio.run(main())

