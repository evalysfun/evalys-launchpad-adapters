"""
Tests for allowlist manager
"""

import pytest
from solders.pubkey import Pubkey
from src.safety.allowlist import AllowlistManager


def test_allowlist_init():
    """Test allowlist initialization"""
    allowlist = AllowlistManager()
    assert len(allowlist.get_allowed_programs()) == 0


def test_add_program():
    """Test adding program to allowlist"""
    allowlist = AllowlistManager()
    program_id = Pubkey.from_string("11111111111111111111111111111111")
    
    allowlist.add_program(program_id)
    assert allowlist.is_allowed(program_id)
    assert len(allowlist.get_allowed_programs()) == 1


def test_remove_program():
    """Test removing program from allowlist"""
    allowlist = AllowlistManager()
    program_id = Pubkey.from_string("11111111111111111111111111111111")
    
    allowlist.add_program(program_id)
    assert allowlist.is_allowed(program_id)
    
    allowlist.remove_program(program_id)
    assert not allowlist.is_allowed(program_id)


def test_is_allowed():
    """Test checking if program is allowed"""
    allowlist = AllowlistManager()
    program_id = Pubkey.from_string("11111111111111111111111111111111")
    
    assert not allowlist.is_allowed(program_id)
    
    allowlist.add_program(program_id)
    assert allowlist.is_allowed(program_id)


def test_clear():
    """Test clearing allowlist"""
    allowlist = AllowlistManager()
    program_id = Pubkey.from_string("11111111111111111111111111111111")
    
    allowlist.add_program(program_id)
    assert len(allowlist.get_allowed_programs()) == 1
    
    allowlist.clear()
    assert len(allowlist.get_allowed_programs()) == 0

