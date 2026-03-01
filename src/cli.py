import argparse
from src.rosi import RosiInputs, calculate


def format_eur(value: float) -> str:
    return f"€{value:,.2f}"


def main():
    parser = argparse.ArgumentParser(
        description="Cyber Risk Calculator (ROSI Model)"
    )

    parser.add_argument("--asset-value", type=float, required=True)
    parser.add_argument("--exposure-factor", type=float, required=True)
    parser.add_argument("--aro", type=float, required=True)
    parser.add_argument("--risk-reduction", type=float, required=True)
    parser.add_argument("--control-cost", type=float, required=True)

    args = parser.parse_args()

    inputs = RosiInputs(
        asset_value=args.asset_value,
        exposure_factor=args.exposure_factor,
        aro=args.aro,
        risk_reduction_pct=args.risk_reduction,
        control_cost=args.control_cost,
    )

    results = calculate(inputs)

    print("\n=== Cyber Risk Analysis Report ===")
    print(f"SLE: {format_eur(results.sle)}")
    print(f"ALE (Before): {format_eur(results.ale_before)}")
    print(f"ALE (After): {format_eur(results.ale_after)}")
    print(f"Risk Reduction: {format_eur(results.risk_reduction)}")
    print(f"ROSI: {results.rosi_pct:.2f}%")

    if results.rosi_pct > 0:
        print("\nDecision: ✅ APPROVE INVESTMENT")
        exit(0)
    else:
        print("\nDecision: ❌ REJECT INVESTMENT")
        exit(1)


if __name__ == "__main__":
    main()