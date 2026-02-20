import numpy as np
import requests
from collections import defaultdict
import re

print("=" * 130)
print("🚀 REALTIME ATC PREPARATION CLASSIFICATION — MULTI-MONTH COMPARISON (DEC 2025 / JAN 2026 / FEB 2026)")
print("=" * 130)

# =============================================================================
# LIVE DATA FETCH (End-2025 Military Aircraft)
# =============================================================================

def fetch_realtime_fleets():
    """Fetch latest military aircraft data with live requests."""
    print("📡 Fetching realtime military fleet data...")

    gfp_fleets = {
        'USA': 13209, 'RUS': 4255, 'CHN': 3304, 'IND': 2296, 'KOR': 1576,
        'JPN': 1459, 'PAK': 1434, 'EGY': 1080, 'TUR': 1069, 'FRA': 972,
        'PRK': 951, 'SAU': 914, 'ITA': 800, 'TWN': 750, 'GBR': 664,
        'DEU': 618, 'ESP': 513
    }

    try:
        resp = requests.get("https://www.globalfirepower.com/aircraft-total.php", timeout=5)
        if resp.status_code == 200:
            matches = re.findall(r'(\w+)</td>\s*<td>(\d+)', resp.text, re.IGNORECASE)
            for country, count in matches[:20]:
                gfp_fleets[country.upper()] = int(count)
            print("   ✓ Global Firepower live update")
    except Exception as e:
        print(f"   ⚠ Live fetch failed: {e} — using cached")

    combat_fleets = {
        'USA': 2803, 'RUS': 1538, 'CHN': 1334, 'IND': 686, 'PRK': 572,
        'KOR': 467, 'PAK': 450, 'EGY': 427, 'FRA': 265, 'JPN': 261,
        'GBR': 183, 'ITA': 210, 'DEU': 98
    }

    print(f"   ✓ Top: USA({gfp_fleets['USA']:,} total) RUS({combat_fleets['RUS']:,} combat)")
    return gfp_fleets, combat_fleets

gfp_fleets, combat_fleets = fetch_realtime_fleets()

# =============================================================================
# MULTI-MONTH ROUTE FUEL DATA
# Replace these values with your actual data for each month
# Format: (country, ops, fuel_liters)
# =============================================================================

MONTHLY_DATA = {
    'DEC 2025': [
        ('USA', 8112, 473.3), ('GBR', 1400, 450.2), ('FRA', 1300, 420.1),
        ('DEU', 1200, 380.5), ('IND', 850, 370.4), ('ESP', 1100, 350.3),
        ('PAK', 800, 340.2), ('ITA', 1000, 320.8)
    ],
    'JAN 2026': [
        # ✏️ REPLACE with your actual January data
        ('USA', 8300, 480.1), ('GBR', 1450, 455.0), ('FRA', 1280, 415.5),
        ('DEU', 1220, 385.0), ('IND', 870, 375.2), ('ESP', 1120, 355.8),
        ('PAK', 820, 345.0), ('ITA', 1020, 325.3)
    ],
    'FEB 2026': [
        # ✏️ REPLACE with your actual February data
        ('USA', 8500, 490.5), ('GBR', 1480, 460.3), ('FRA', 1310, 425.0),
        ('DEU', 1250, 390.2), ('IND', 900, 380.1), ('ESP', 1150, 360.0),
        ('PAK', 850, 350.5), ('ITA', 1050, 330.7)
    ],
}

# =============================================================================
# CLASSIFICATION FUNCTION
# =============================================================================

def classify_month(label, route_fuel):
    print(f"\n📊 CLASSIFICATION — {label}")
    print("-" * 130)

    nation_effort = []
    total_global_ops = sum(ops for _, ops, _ in route_fuel)

    for country, ops, fuel in route_fuel:
        total_fleet = gfp_fleets.get(country, 100)
        combat_fleet = combat_fleets.get(country, 50)

        effort_score = fuel / (ops / total_fleet) if ops > 0 and total_fleet > 0 else 0
        pct_global_ops = ops / total_global_ops * 100

        if fuel > 400:
            level = "🟥 HIGH COMMITMENT"
        elif fuel > 250:
            level = "🟨 MAJOR CONTRIBUTOR"
        elif fuel > 100:
            level = "🟢 MODERATE SUPPORT"
        else:
            level = "🔵 MINIMAL"

        nation_effort.append({
            'Nation': country, 'Ops': ops, 'Fuel_L': fuel, 'Total_Fleet': total_fleet,
            'Combat_Fleet': combat_fleet, 'Ops%': round(pct_global_ops, 1),
            'Effort_Score': round(effort_score, 2), 'Level': level
        })

    nation_effort.sort(key=lambda x: x['Effort_Score'], reverse=True)

    print(f"{'Nation':<6} {'Ops':<6} {'Fuel':<7} {'Fleet':<8} {'Combat':<7} {'Ops%':<6} {'Score':<8} {'Level'}")
    print("-" * 130)
    for row in nation_effort:
        print(f"{row['Nation']:<6} {row['Ops']:<6,} {row['Fuel_L']:<7.1f} "
              f"{row['Total_Fleet']:<8,} {row['Combat_Fleet']:<7} "
              f"{row['Ops%']:<6} {row['Effort_Score']:<8.2f} {row['Level']}")

    return nation_effort

# =============================================================================
# RUN ALL MONTHS
# =============================================================================

all_results = {}
for month_label, data in MONTHLY_DATA.items():
    all_results[month_label] = classify_month(month_label, data)

# =============================================================================
# MONTH-OVER-MONTH COMPARISON
# =============================================================================

print("\n" + "=" * 130)
print("📈 MONTH-OVER-MONTH COMPARISON — EFFORT SCORE & OPS DELTA")
print("=" * 130)

months = list(MONTHLY_DATA.keys())
all_nations = list({row['Nation'] for results in all_results.values() for row in results})

header = f"{'Nation':<6}"
for m in months:
    header += f" {m:>18}"
header += f"  {'Trend'}"
print(header)
print("-" * 130)

for nation in sorted(all_nations):
    row_str = f"{nation:<6}"
    scores = []
    for m in months:
        match = next((r for r in all_results[m] if r['Nation'] == nation), None)
        if match:
            row_str += f"  Score:{match['Effort_Score']:>7.2f} Ops:{match['Ops']:>5,}"
            scores.append(match['Effort_Score'])
        else:
            row_str += f"  {'N/A':>18}"
            scores.append(None)

    valid = [s for s in scores if s is not None]
    if len(valid) >= 2:
        delta = valid[-1] - valid[0]
        trend = f"▲ +{delta:.2f}" if delta > 0 else (f"▼ {delta:.2f}" if delta < 0 else "● No Change")
    else:
        trend = "—"
    row_str += f"  {trend}"
    print(row_str)

# =============================================================================
# STRATEGIC SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("🟥 STRATEGIC SUMMARY — ALL MONTHS")
print("=" * 80)

for month_label, results in all_results.items():
    top3 = results[:3]
    total_ops = sum(r['Ops'] for r in results)
    usa = next((r for r in results if r['Nation'] == 'USA'), None)
    usa_pct = f"{usa['Ops%']}%" if usa else "N/A"
    print(f"\n🗓  {month_label}")
    print(f"   🏆 TOP 3: " + " | ".join(
        f"{r['Nation']} (Score:{r['Effort_Score']:.2f}, Fuel:{r['Fuel_L']:.0f}L)"
        for r in top3
    ))
    print(f"   🌍 Total Ops: {total_ops:,} | USA Dominance: {usa_pct}")

print("\n" + "=" * 80)
print("STATUS: MULTI-MONTH ANALYSIS COMPLETE")
print("=" * 80)
