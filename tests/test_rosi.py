import pytest
from src.rosi import RosiInputs, calculate, classify_risk_level


def test_calculate_known_example():
    i = RosiInputs(
        asset_value=500000,
        exposure_factor=0.4,
        aro=0.3,
        risk_reduction_pct=60,
        control_cost=20000,
    )
    r = calculate(i)

    assert r.sle == 200000.0
    assert r.ale_before == 60000.0
    assert r.ale_after == 24000.0
    assert r.risk_reduction == 36000.0
    assert r.rosi_pct == 80.0
    assert r.risk_level == "MEDIUM"


def test_risk_level_thresholds():
    assert classify_risk_level(0) == "LOW"
    assert classify_risk_level(29999.99) == "LOW"
    assert classify_risk_level(30000) == "MEDIUM"
    assert classify_risk_level(99999.99) == "MEDIUM"
    assert classify_risk_level(100000) == "HIGH"


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        calculate(RosiInputs(-1, 0.4, 0.3, 60, 20000))

    with pytest.raises(ValueError):
        calculate(RosiInputs(500000, 1.5, 0.3, 60, 20000))

    with pytest.raises(ValueError):
        calculate(RosiInputs(500000, 0.4, -0.1, 60, 20000))

    with pytest.raises(ValueError):
        calculate(RosiInputs(500000, 0.4, 0.3, 120, 20000))

    with pytest.raises(ValueError):
        calculate(RosiInputs(500000, 0.4, 0.3, 60, 0))