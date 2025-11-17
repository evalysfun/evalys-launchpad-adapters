"""
Pump.fun Adapter

Adapter for Pump.fun launchpad platform.
"""

from typing import Optional
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.instruction import Instruction, AccountMeta
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from .base_adapter import LaunchpadAdapter, CurveData, TokenInfo
from ..safety.allowlist import AllowlistManager
from ..safety.validator import InstructionValidator
from ..safety.sanitizer import BehaviorSanitizer
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Pump.fun Program ID (mainnet)
PUMP_FUN_PROGRAM_ID = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")


class PumpFunAdapter(LaunchpadAdapter):
    """
    Adapter for Pump.fun launchpad
    """
    
    def __init__(
        self,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        allowlist_manager: Optional[AllowlistManager] = None
    ):
        """
        Initialize Pump.fun adapter
        
        Args:
            rpc_url: Solana RPC endpoint
            allowlist_manager: Optional allowlist manager for safety
        """
        super().__init__(PUMP_FUN_PROGRAM_ID, rpc_url)
        
        self.client: Optional[AsyncClient] = None
        self.allowlist = allowlist_manager or AllowlistManager()
        self.validator = InstructionValidator()
        self.sanitizer = BehaviorSanitizer()
        
        # Add Pump.fun program to allowlist
        self.allowlist.add_program(PUMP_FUN_PROGRAM_ID)
        
        logger.info("PumpFunAdapter initialized")
    
    async def connect(self):
        """Connect to Solana RPC"""
        if self.client is None:
            self.client = AsyncClient(self.rpc_url)
            logger.debug("Connected to Solana RPC")
    
    async def disconnect(self):
        """Disconnect from Solana RPC"""
        if self.client:
            await self.client.close()
            self.client = None
            logger.debug("Disconnected from Solana RPC")
    
    async def get_curve_data(self, token_mint: Pubkey) -> CurveData:
        """
        Get bonding curve data for a token
        
        Args:
            token_mint: Token mint address
            
        Returns:
            CurveData instance
        """
        await self.connect()
        
        try:
            # Fetch curve data from on-chain accounts
            # TODO: Implement on-chain account parsing for Pump.fun bonding curve
            logger.debug(f"Fetching curve data for {token_mint}")
            # TODO: Parse on-chain account data to populate curve metrics
            curve_data = CurveData(
                token_mint=token_mint,
                current_price=0.0,
                slope=0.0,
                liquidity=0.0,
                total_supply=0.0,
                market_cap=0.0,
                timestamp=0.0
            )
            
            return curve_data
            
        except Exception as e:
            logger.error(f"Error fetching curve data: {e}")
            raise
    
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
            slippage: Maximum acceptable slippage
            
        Returns:
            Transaction ready to sign and send
        """
        await self.connect()
        
        # Validate program is in allowlist
        if not self.allowlist.is_allowed(self.program_id):
            raise ValueError(f"Program {self.program_id} not in allowlist")
        
        try:
            # Get recent blockhash
            blockhash_resp = await self.client.get_latest_blockhash(commitment=Confirmed)
            recent_blockhash = blockhash_resp.value.blockhash
            
            # Build buy instruction
            instruction = self._build_buy_instruction(
                buyer.pubkey(),
                token_mint,
                sol_amount,
                slippage
            )
            
            # Validate instruction
            self.validator.validate_instruction(instruction, self.program_id)
            
            # Sanitize behavior (remove identifying patterns)
            instruction = self.sanitizer.sanitize_instruction(instruction)
            
            # Build transaction
            transaction = Transaction()
            transaction.add(instruction)
            transaction.sign([buyer], recent_blockhash)
            
            logger.info(
                f"Built buy transaction: {token_mint}, amount: {sol_amount} SOL, "
                f"slippage: {slippage * 100}%"
            )
            
            return transaction
            
        except Exception as e:
            logger.error(f"Error building buy transaction: {e}")
            raise
    
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
            slippage: Maximum acceptable slippage
            
        Returns:
            Transaction ready to sign and send
        """
        await self.connect()
        
        # Validate program is in allowlist
        if not self.allowlist.is_allowed(self.program_id):
            raise ValueError(f"Program {self.program_id} not in allowlist")
        
        try:
            # Get recent blockhash
            blockhash_resp = await self.client.get_latest_blockhash(commitment=Confirmed)
            recent_blockhash = blockhash_resp.value.blockhash
            
            # Build sell instruction
            instruction = self._build_sell_instruction(
                seller.pubkey(),
                token_mint,
                token_amount,
                slippage
            )
            
            # Validate instruction
            self.validator.validate_instruction(instruction, self.program_id)
            
            # Sanitize behavior
            instruction = self.sanitizer.sanitize_instruction(instruction)
            
            # Build transaction
            transaction = Transaction()
            transaction.add(instruction)
            transaction.sign([seller], recent_blockhash)
            
            logger.info(
                f"Built sell transaction: {token_mint}, amount: {token_amount}, "
                f"slippage: {slippage * 100}%"
            )
            
            return transaction
            
        except Exception as e:
            logger.error(f"Error building sell transaction: {e}")
            raise
    
    async def get_token_info(self, token_mint: Pubkey) -> TokenInfo:
        """
        Get token information
        
        Args:
            token_mint: Token mint address
            
        Returns:
            TokenInfo instance
        """
        await self.connect()
        
        try:
            # TODO: Fetch token metadata from on-chain accounts
            logger.debug(f"Fetching token info for {token_mint}")
            
            token_info = TokenInfo(
                mint=token_mint,
                symbol="",
                name="",
                uri=None
            )
            
            return token_info
            
        except Exception as e:
            logger.error(f"Error fetching token info: {e}")
            raise
    
    def _build_buy_instruction(
        self,
        buyer: Pubkey,
        token_mint: Pubkey,
        sol_amount: float,
        slippage: float
    ) -> Instruction:
        """
        Build buy instruction for Pump.fun
        
        TODO: Implement full instruction building:
        - Derive required PDAs (bonding curve, associated token accounts)
        - Serialize instruction data with proper discriminators
        - Include all required accounts per Pump.fun program spec
        """
        lamports = int(sol_amount * 1_000_000_000)
        
        accounts = [
            AccountMeta(pubkey=buyer, is_signer=True, is_writable=True),
            AccountMeta(pubkey=token_mint, is_signer=False, is_writable=True),
        ]
        
        # TODO: Serialize proper Pump.fun buy instruction data
        data = bytes([0])
        
        return Instruction(
            program_id=self.program_id,
            accounts=accounts,
            data=data
        )
    
    def _build_sell_instruction(
        self,
        seller: Pubkey,
        token_mint: Pubkey,
        token_amount: float,
        slippage: float
    ) -> Instruction:
        """
        Build sell instruction for Pump.fun
        
        TODO: Implement full sell instruction building
        """
        accounts = [
            AccountMeta(pubkey=seller, is_signer=True, is_writable=True),
            AccountMeta(pubkey=token_mint, is_signer=False, is_writable=True),
        ]
        
        data = bytes([1])  # Sell instruction discriminator
        
        return Instruction(
            program_id=self.program_id,
            accounts=accounts,
            data=data
        )

