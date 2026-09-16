# batch_cost_calculator.py — Craft Brewery Batch Cost Calculator
# Inspired by: tfrayner/beerfestdb/CBF_beer_price_calculator.py

def calculate_batch_cost(
    grain_cost_per_lb: float,
    hops_cost_per_oz: float,
    yeast_cost_per_unit: float,
    packaging_cost_per_unit: float,
    batch_size_barrels: float,
    margin_pct: float,
    # Recipe quantities (per batch)
    grain_lbs: float = 2000.0,
    hops_oz: float = 80.0,
    yeast_units: float = 2.0,
    packaging_units: float = 200.0,
) -> dict:
    """
    Calculate the total cost and recommended selling price per barrel
    for a craft brewery batch.

    Parameters
    ----------
    grain_cost_per_lb : float – price per pound of grain ($)
    hops_cost_per_oz : float – price per ounce of hops ($)
    yeast_cost_per_unit : float – price per unit of yeast ($)
    packaging_cost_per_unit : float – price per unit of packaging (e.g. can/bottle) ($)
    batch_size_barrels : float – batch size in US beer barrels (1 US bbl = 31 US gal)
    margin_pct : float – desired profit margin as a percentage (e.g. 30 for 30%)
    grain_lbs : float – total grain pounds for the batch (default 2000)
    hops_oz : float – total hops ounces for the batch (default 80)
    yeast_units : float – total yeast units for the batch (default 2)
    packaging_units : float – total packaging units for the batch (default 200)

    Returns
    -------
    dict with ingredient costs, totals, cost per barrel, and recommended price.
    """
    # --- Ingredient-level costs ---
    grain_total    = grain_lbs    * grain_cost_per_lb
    hops_total     = hops_oz      * hops_cost_per_oz
    yeast_total    = yeast_units  * yeast_cost_per_unit
    packaging_total = packaging_units * packaging_cost_per_unit

    # --- Totals ---
    total_cost = grain_total + hops_total + yeast_total + packaging_total
    cost_per_barrel = total_cost / batch_size_barrels

    # --- Recommended selling price with margin ---
    # selling_price = cost / (1 - margin)
    recommended_price_per_barrel = cost_per_barrel / (1 - margin_pct / 100)

    return {
        "grain_cost":       grain_total,
        "hops_cost":        hops_total,
        "yeast_cost":       yeast_total,
        "packaging_cost":   packaging_total,
        "total_cost":       total_cost,
        "cost_per_barrel":  cost_per_barrel,
        "margin_pct":       margin_pct,
        "recommended_price_per_barrel": recommended_price_per_barrel,
    }


def main():
    # --- Sample batch ---
    # 2,000 lb grain @ $0.45/lb, 80 oz hops @ $0.60/oz,
    # 2 yeast units @ $12 each, 200 cans @ $0.15 each
    # Batch size: 10 barrels, margin: 30%

    results = calculate_batch_cost(
        grain_cost_per_lb=0.45,
        hops_cost_per_oz=0.60,
        yeast_cost_per_unit=12.0,
        packaging_cost_per_unit=0.15,
        batch_size_barrels=10,
        margin_pct=30,
        grain_lbs=2000,
        hops_oz=80,
        yeast_units=2,
        packaging_units=200,
    )

    # --- Display results ---
    print("=" * 60)
    print("  CRAFT BREWERY BATCH COST CALCULATOR")
    print("=" * 60)
    print()
    print("  Ingredient Costs:")
    print(f"    Grain       : ${results['grain_cost']:>10,.2f}  (2,000 lb × $0.45/lb)")
    print(f"    Hops        : ${results['hops_cost']:>10,.2f}  (80 oz × $0.60/oz)")
    print(f"    Yeast       : ${results['yeast_cost']:>10,.2f}  (2 × $12.00)")
    print(f"    Packaging   : ${results['packaging_cost']:>10,.2f}  (200 × $0.15)")
    print()
    print("  Cost Summary:")
    print(f"    Total Cost          : ${results['total_cost']:>10,.2f}")
    print(f"    Batch Size          : 10 barrels")
    print(f"    Cost per Barrel     : ${results['cost_per_barrel']:>10,.2f}")
    print()
    print("  Pricing:")
    print(f"    Margin              : 30%")
    print(f"    Recommended Price   : ${results['recommended_price_per_barrel']:>10,.2f} per barrel")
    print()
    print("=" * 60)

    # --- Validation checks ---
    assert results['total_cost'] > 0, "Total cost must be positive"
    assert results['cost_per_barrel'] > 0, "Cost per barrel must be positive"
    assert results['recommended_price_per_barrel'] > results['cost_per_barrel'], \
        "Recommended price must exceed cost"
    assert abs(results['recommended_price_per_barrel'] - results['cost_per_barrel'] / 0.70) < 0.01, \
        "Price calculation is incorrect"
    print("All validation checks passed.")


if __name__ == "__main__":
    main()