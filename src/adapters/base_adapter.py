"""
Base Adapter

Abstract base class for launchpad adapters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CurveData:
    """
    Bonding curve data
    
    Attributes:
        token_mint: Token mint address
        current_price: Current price in SOL
        slope: Curve slope
        liquidity: Available liquidity
        total_supply: Total token supply
        market_cap: Market capitalization
        timestamp: Data timestamp
    """
    token_mint: Pubkey
    current_price: float
    slope: float
    liquidity: float
    total_supply: float
    market_cap: float
    timestamp: float


@dataclass
class TokenInfo:
    """
    Token information
    
    Attributes:
        mint: Token mint address
        symbol: Token symbol
        name: Token name
        uri: Token metadata URI
        created_at: Creation timestamp
    """
    mint: Pubkey
    symbol: str
    name: str
    uri: Optional[str] = None
    created_at: Optional[float] = None


class LaunchpadAdapter(ABC):
    """
    Abstract base class for launchpad adapters
    
    All launchpad adapters must implement these methods.
    """
    
    def __init__(self, program_id: Pubkey, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        """
        Initialize adapter
        
        Args:
            program_id: Launchpad program ID
            rpc_url: Solana RPC endpoint
        """
        self.program_id = program_id
        self.rpc_url = rpc_url
        logger.info(f"{self.__class__.__name__} initialized with program: {program_id}")
    
    @abstractmethod
    async def get_curve_data(self, token_mint: Pubkey) -> CurveData:
        """
        Get bonding curve data for a token
        
        Args:
            token_mint: Token mint address
            
        Returns:
            CurveData instance
        """
        pass
    
    @abstractmethod
    async def buy_token(
        self,
        buyer: Keypair,
        token_mint: Pubkey,
        sol_amount: float,
        slippage: float = 0.05
    ) -> Transaction:
        """
        Build buy token transaction
        
        Args:
            buyer: Buyer wallet keypair
            token_mint: Token mint address
            sol_amount: Amount of SOL to spend
            slippage: Maximum acceptable slippage (default: 5%)
            
        Returns:
            Transaction ready to sign and send
        """
        pass
    
    @abstractmethod
    async def sell_token(
        self,
        seller: Keypair,
        token_mint: Pubkey,
        token_amount: float,
        slippage: float = 0.05
    ) -> Transaction:
        """
        Build sell token transaction
        
        Args:
            seller: Seller wallet keypair
            token_mint: Token mint address
            token_amount: Amount of tokens to sell
            slippage: Maximum acceptable slippage (default: 5%)
            
        Returns:
            Transaction ready to sign and send
        """
        pass
    
    @abstractmethod
    async def get_token_info(self, token_mint: Pubkey) -> TokenInfo:
        """
        Get token information
        
        Args:
            token_mint: Token mint address
            
        Returns:
            TokenInfo instance
        """
        pass
    
    def validate_program(self, program_id: Pubkey) -> bool:
        """
        Validate that program ID matches adapter's program
        
        Args:
            program_id: Program ID to validate
            
        Returns:
            True if valid
        """
        return program_id == self.program_id
    
    def get_program_id(self) -> Pubkey:
        """
        Get adapter's program ID
        
        Returns:
            Program ID
        """
        return self.program_id

