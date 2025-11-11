"""
Allowlist Manager

Manages program allowlists for safety and compliance.
"""

from typing import Set
from solders.pubkey import Pubkey
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AllowlistManager:
    """
    Manages allowlists of approved programs
    """
    
    def __init__(self):
        """Initialize allowlist manager"""
        self.allowed_programs: Set[str] = set()
        logger.info("AllowlistManager initialized")
    
    def add_program(self, program_id: Pubkey):
        """
        Add program to allowlist
        
        Args:
            program_id: Program ID to allow
        """
        program_str = str(program_id)
        self.allowed_programs.add(program_str)
        logger.debug(f"Added program to allowlist: {program_str}")
    
    def remove_program(self, program_id: Pubkey):
        """
        Remove program from allowlist
        
        Args:
            program_id: Program ID to remove
        """
        program_str = str(program_id)
        if program_str in self.allowed_programs:
            self.allowed_programs.remove(program_str)
            logger.debug(f"Removed program from allowlist: {program_str}")
    
    def is_allowed(self, program_id: Pubkey) -> bool:
        """
        Check if program is in allowlist
        
        Args:
            program_id: Program ID to check
            
        Returns:
            True if allowed
        """
        program_str = str(program_id)
        is_allowed = program_str in self.allowed_programs
        
        if not is_allowed:
            logger.warning(f"Program {program_str} not in allowlist")
        
        return is_allowed
    
    def get_allowed_programs(self) -> Set[str]:
        """
        Get all allowed programs
        
        Returns:
            Set of allowed program IDs (as strings)
        """
        return self.allowed_programs.copy()
    
    def clear(self):
        """Clear all allowed programs"""
        self.allowed_programs.clear()
        logger.info("Allowlist cleared")

