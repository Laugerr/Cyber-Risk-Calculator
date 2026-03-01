import argparse
import json
from src.rosi import RosiInputs, calculate
from dataclasses import asdict


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
    parser.add_argument("--json", action="store_true", help="Output a JSON report")
    parser.add_argument("--out", type=str, help="Write JSON output to a file (e.g., report.json)")

    args = parser.parse_args()

    inputs = RosiInputs(
        asset_value=args.asset_value,
        exposure_factor=args.exposure_factor,
        aro=args.aro,
        risk_reduction_pct=args.risk_reduction,
        control_cost=args.control_cost,
    )

    results = calculate(inputs)

    # --- JSON MODE ---
    if args.json:
        payload = {
            "inputs": asdict(inputs),
            "results": asdict(results),
            "decision": "APPROVE" if results.rosi_pct > 0 else "REJECT",
        }

        output = json.dumps(payload, indent=2)

        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output + "\n")
            print(f"✅ JSON report written to: {args.out}")
        else:
            print(output)

        raise SystemExit(0 if results.rosi_pct > 0 else 1)

    # --- NORMAL REPORT MODE ---
    print("\n=== Cyber Risk Analysis Report ===")
    print(f"SLE: {format_eur(results.sle)}")
    print(f"ALE (Before): {format_eur(results.ale_before)}")
    print(f"Risk Level (based on ALE before): {results.risk_level}")
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