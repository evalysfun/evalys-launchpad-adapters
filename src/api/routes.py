"""
API Routes for Launchpad Adapters

REST API endpoints for launchpad adapter operations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import base64
from ..adapters.pumpfun_adapter import PumpFunAdapter
from ..adapters.bonkfun_adapter import BonkFunAdapter
from ..config.settings import Settings

router = APIRouter(prefix="/api/v1/launchpad", tags=["launchpad"])

# Global adapters (in production, use dependency injection)
pumpfun_adapter = PumpFunAdapter(rpc_url=Settings.SOLANA_RPC_URL)
bonkfun_adapter = BonkFunAdapter(rpc_url=Settings.SOLANA_RPC_URL)


class BuyTokenRequest(BaseModel):
    """Request model for buying tokens"""
    launchpad: str = Field(..., description="Launchpad name: 'pumpfun' or 'bonkfun'")
    token_mint: str = Field(..., description="Token mint address")
    sol_amount: float = Field(..., ge=0.0, description="Amount of SOL to spend")
    slippage: float = Field(0.05, ge=0.0, le=1.0, description="Maximum slippage (0-1)")
    wallet_keypair: str = Field(..., description="Base64 encoded wallet keypair")


class SellTokenRequest(BaseModel):
    """Request model for selling tokens"""
    launchpad: str = Field(..., description="Launchpad name: 'pumpfun' or 'bonkfun'")
    token_mint: str = Field(..., description="Token mint address")
    token_amount: float = Field(..., ge=0.0, description="Amount of tokens to sell")
    slippage: float = Field(0.05, ge=0.0, le=1.0, description="Maximum slippage (0-1)")
    wallet_keypair: str = Field(..., description="Base64 encoded wallet keypair")


class CurveDataResponse(BaseModel):
    """Response model for curve data"""
    token_mint: str
    current_price: float
    slope: float
    liquidity: float
    total_supply: float
    market_cap: float
    timestamp: float


class TokenInfoResponse(BaseModel):
    """Response model for token info"""
    mint: str
    symbol: str
    name: str
    uri: Optional[str] = None
    created_at: Optional[float] = None


def decode_keypair(keypair_str: str) -> Keypair:
    """Decode base64 keypair string"""
    try:
        keypair_bytes = base64.b64decode(keypair_str)
        return Keypair.from_bytes(keypair_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid keypair: {e}")


def get_adapter(launchpad: str):
    """Get adapter for launchpad"""
    launchpad_lower = launchpad.lower()
    
    if launchpad_lower == "pumpfun" or launchpad_lower == "pump.fun":
        return pumpfun_adapter
    elif launchpad_lower == "bonkfun" or launchpad_lower == "bonk.fun":
        return bonkfun_adapter
    else:
        raise HTTPException(status_code=400, detail=f"Unknown launchpad: {launchpad}")


@router.post("/buy-token")
async def buy_token(request: BuyTokenRequest):
    """
    Build buy token transaction
    
    Returns a transaction ready to sign and send.
    """
    try:
        adapter = get_adapter(request.launchpad)
        wallet = decode_keypair(request.wallet_keypair)
        token_mint = Pubkey.from_string(request.token_mint)
        
        transaction = await adapter.buy_token(
            wallet,
            token_mint,
            request.sol_amount,
            request.slippage
        )
        
        # Serialize transaction
        transaction_bytes = bytes(transaction)
        transaction_b64 = base64.b64encode(transaction_bytes).decode()
        
        return {
            "success": True,
            "transaction": transaction_b64,
            "launchpad": request.launchpad,
            "token_mint": request.token_mint,
            "sol_amount": request.sol_amount
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sell-token")
async def sell_token(request: SellTokenRequest):
    """
    Build sell token transaction
    
    Returns a transaction ready to sign and send.
    """
    try:
        adapter = get_adapter(request.launchpad)
        wallet = decode_keypair(request.wallet_keypair)
        token_mint = Pubkey.from_string(request.token_mint)
        
        transaction = await adapter.sell_token(
            wallet,
            token_mint,
            request.token_amount,
            request.slippage
        )
        
        # Serialize transaction
        transaction_bytes = bytes(transaction)
        transaction_b64 = base64.b64encode(transaction_bytes).decode()
        
        return {
            "success": True,
            "transaction": transaction_b64,
            "launchpad": request.launchpad,
            "token_mint": request.token_mint,
            "token_amount": request.token_amount
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/curve-data/{launchpad}/{token_mint}")
async def get_curve_data(launchpad: str, token_mint: str):
    """Get bonding curve data for a token"""
    try:
        adapter = get_adapter(launchpad)
        mint = Pubkey.from_string(token_mint)
        
        curve_data = await adapter.get_curve_data(mint)
        
        return CurveDataResponse(
            token_mint=token_mint,
            current_price=curve_data.current_price,
            slope=curve_data.slope,
            liquidity=curve_data.liquidity,
            total_supply=curve_data.total_supply,
            market_cap=curve_data.market_cap,
            timestamp=curve_data.timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/token-info/{launchpad}/{token_mint}")
async def get_token_info(launchpad: str, token_mint: str):
    """Get token information"""
    try:
        adapter = get_adapter(launchpad)
        mint = Pubkey.from_string(token_mint)
        
        token_info = await adapter.get_token_info(mint)
        
        return TokenInfoResponse(
            mint=token_mint,
            symbol=token_info.symbol,
            name=token_info.name,
            uri=token_info.uri,
            created_at=token_info.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/launchpads")
async def get_launchpads():
    """Get list of supported launchpads"""
    return {
        "launchpads": [
            {
                "name": "pumpfun",
                "display_name": "Pump.fun",
                "program_id": str(pumpfun_adapter.get_program_id()),
                "supported": True
            },
            {
                "name": "bonkfun",
                "display_name": "Bonk.fun",
                "program_id": str(bonkfun_adapter.get_program_id()),
                "supported": False  # Not fully implemented
            }
        ]
    }

