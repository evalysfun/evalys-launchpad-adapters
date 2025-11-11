"""
Instruction Validator

Validates instructions for safety and compliance.
"""

from solders.instruction import Instruction
from solders.pubkey import Pubkey
from ..utils.logger import get_logger

logger = get_logger(__name__)


class InstructionValidator:
    """
    Validates Solana instructions
    """
    
    def __init__(self):
        """Initialize validator"""
        logger.info("InstructionValidator initialized")
    
    def validate_instruction(self, instruction: Instruction, expected_program: Pubkey):
        """
        Validate instruction
        
        Args:
            instruction: Instruction to validate
            expected_program: Expected program ID
            
        Raises:
            ValueError: If validation fails
        """
        # Check program ID matches
        if instruction.program_id != expected_program:
            raise ValueError(
                f"Instruction program ID {instruction.program_id} "
                f"does not match expected {expected_program}"
            )
        
        # Check instruction has accounts
        if not instruction.accounts:
            raise ValueError("Instruction has no accounts")
        
        # Check instruction has data
        if not instruction.data:
            logger.warning("Instruction has no data")
        
        logger.debug(f"Instruction validated for program: {expected_program}")
    
    def validate_accounts(self, instruction: Instruction, required_accounts: int):
        """
        Validate instruction has required number of accounts
        
        Args:
            instruction: Instruction to validate
            required_accounts: Minimum number of accounts required
            
        Raises:
            ValueError: If validation fails
        """
        if len(instruction.accounts) < required_accounts:
            raise ValueError(
                f"Instruction has {len(instruction.accounts)} accounts, "
                f"but requires at least {required_accounts}"
            )

