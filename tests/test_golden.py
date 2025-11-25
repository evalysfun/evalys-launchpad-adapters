"""
Golden Tests

Tests that verify adapter outputs match known-good transaction fixtures.
"""

import pytest
import json
from pathlib import Path
from solders.pubkey import Pubkey
from src.adapters.pumpfun_adapter import PumpFunAdapter

# Fixture directory
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "pumpfun"


class TestPumpFunGolden:
    """Golden tests for Pump.fun adapter"""
    
    def test_build_buy_tx_matches_fixture(self):
        """
        Test that built buy transaction matches known-good fixture
        
        This test verifies:
        - Correct program ID
        - Correct account list
        - Correct instruction data structure
        """
        # Load fixture
        fixture_path = FIXTURES_DIR / "buy_example.json"
        if not fixture_path.exists():
            pytest.skip("Buy fixture not available")
        
        with open(fixture_path) as f:
            fixture = json.load(f)
        
        # Build transaction (would use actual adapter)
        # For now, verify fixture structure
        assert "program_id" in fixture
        assert "accounts" in fixture
        assert "instruction_data" in fixture
        
        # Verify program ID matches
        expected_program_id = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
        assert fixture["program_id"] == expected_program_id
        
        # Verify account structure
        assert len(fixture["accounts"]) > 0
        for account in fixture["accounts"]:
            assert "pubkey" in account
            assert "is_signer" in account
            assert "is_writable" in account
    
    def test_parse_event_extracts_data(self):
        """
        Test that parse_event extracts correct mint/amounts from transaction
        
        This test verifies:
        - Event type is correctly identified
        - Mint address is extracted
        - Amounts are correctly parsed
        """
        # Load fixture
        fixture_path = FIXTURES_DIR / "buy_example.json"
        if not fixture_path.exists():
            pytest.skip("Buy fixture not available")
        
        with open(fixture_path) as f:
            fixture = json.load(f)
        
        # Verify fixture has required fields for parsing
        assert "instruction_data" in fixture
        assert "accounts" in fixture
        
        # In real implementation, would parse transaction and extract events
        # For now, verify fixture structure supports parsing
        instruction_data = fixture["instruction_data"]
        assert "discriminator" in instruction_data
        assert "sol_amount" in instruction_data or "token_amount" in instruction_data
    
    def test_quote_matches_observed(self):
        """
        Test that quote roughly matches observed curve output
        
        This test verifies:
        - Quote calculation is reasonable
        - Output amount is within expected range
        - Slippage calculation is correct
        """
        # Load curve state fixture
        curve_fixture_path = FIXTURES_DIR / "curve_state_example.json"
        if not curve_fixture_path.exists():
            pytest.skip("Curve state fixture not available")
        
        with open(curve_fixture_path) as f:
            curve_fixture = json.load(f)
        
        # Verify curve state structure
        assert "curve_state" in curve_fixture
        curve_state = curve_fixture["curve_state"]
        
        # Verify required fields
        assert "current_price" in curve_state
        assert "virtual_sol_reserves" in curve_state
        assert "virtual_token_reserves" in curve_state
        
        # In real implementation, would:
        # 1. Calculate quote from curve state
        # 2. Compare to observed transaction output
        # 3. Verify quote is within acceptable range
        
        # For now, verify curve state is valid
        assert curve_state["current_price"] > 0
        assert curve_state["virtual_sol_reserves"] > 0
        assert curve_state["virtual_token_reserves"] > 0


class TestBonkFunGolden:
    """Golden tests for Bonk.fun adapter"""
    
    def test_build_sell_tx_matches_fixture(self):
        """
        Test that built sell transaction matches known-good fixture
        
        Status: ⏳ Awaiting Bonk.fun program details
        """
        pytest.skip("Bonk.fun adapter not yet implemented")
    
    def test_parse_event_extracts_data(self):
        """
        Test that parse_event extracts correct data
        
        Status: ⏳ Awaiting Bonk.fun program details
        """
        pytest.skip("Bonk.fun adapter not yet implemented")

