"""
Configuration settings
"""

import os


class Settings:
    """Application settings"""
    
    # Solana RPC
    SOLANA_RPC_URL: str = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Pump.fun Program ID
    PUMP_FUN_PROGRAM_ID: str = os.getenv(
        "PUMP_FUN_PROGRAM_ID",
        "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
    )
    
    # Bonk.fun Program ID
    # Set via BONK_FUN_PROGRAM_ID environment variable when available
    BONK_FUN_PROGRAM_ID: str = os.getenv(
        "BONK_FUN_PROGRAM_ID",
        "11111111111111111111111111111111"
    )
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8002"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "false").lower() == "true"

