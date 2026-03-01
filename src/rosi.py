from dataclasses import dataclass


@dataclass(frozen=True)
class RosiInputs:
    asset_value: float          # €
    exposure_factor: float      # 0..1
    aro: float                  # occurrences per year
    risk_reduction_pct: float   # 0..100
    control_cost: float         # €


@dataclass(frozen=True)
class RosiResults:
    sle: float
    ale_before: float
    ale_after: float
    risk_reduction: float
    rosi_pct: float


def _validate(i: RosiInputs) -> None:
    if i.asset_value < 0:
        raise ValueError("asset_value must be >= 0")
    if not (0 <= i.exposure_factor <= 1):
        raise ValueError("exposure_factor must be between 0 and 1")
    if i.aro < 0:
        raise ValueError("aro must be >= 0")
    if not (0 <= i.risk_reduction_pct <= 100):
        raise ValueError("risk_reduction_pct must be between 0 and 100")
    if i.control_cost <= 0:
        raise ValueError("control_cost must be > 0 (needed for ROSI)")


def calculate(i: RosiInputs) -> RosiResults:
    """
    SLE = Asset Value * Exposure Factor
    ALE(before) = SLE * ARO
    ALE(after) = ALE(before) * (1 - risk_reduction_pct)
    Risk Reduction = ALE(before) - ALE(after)
    ROSI% = ((Risk Reduction - Cost) / Cost) * 100
    """
    _validate(i)

    sle = i.asset_value * i.exposure_factor
    ale_before = sle * i.aro

    reduction_factor = i.risk_reduction_pct / 100.0
    ale_after = ale_before * (1.0 - reduction_factor)

    risk_reduction = ale_before - ale_after
    rosi_pct = ((risk_reduction - i.control_cost) / i.control_cost) * 100.0

    return RosiResults(
        sle=sle,
        ale_before=ale_before,
        ale_after=ale_after,
        risk_reduction=risk_reduction,
        rosi_pct=rosi_pct,
    )