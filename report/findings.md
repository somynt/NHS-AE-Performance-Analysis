# A&E in England, 2010 to 2026: findings

*Audience: an NHS operational or planning manager. All figures are from NHS England's Monthly A&E Time Series (published 8 October 2026) and can be reproduced with the SQL in [`../sql`](../sql).*

## Summary

Demand for A&E has grown steadily for 15 years, and the system has not kept pace. Fewer than two in three patients in major A&E departments are now seen within four hours, against a 95% standard last met nationally in July 2015. The sharpest change is in long waits for a hospital bed. More than half a million patients a year now wait over 12 hours after the decision to admit them, up from about 3,000 a year before the pandemic. Performance has recovered a little since its low point in winter 2022, even though demand has kept rising.

## Key findings

**1. Demand is up by almost a third.**
A&E attendances rose from 21.6 million in 2011-12 to 28.0 million in 2025-26 (+29%), about 77,000 patients a day. Attendances at major (Type 1) departments rose by 21%. Apart from the 2020-21 pandemic dip, every year has been busier than the last.

**2. The 4-hour standard has not been met for over a decade.**
Across all A&E types, 95% of patients were seen within 4 hours in 2011-12 (96.6%). By 2025-26 it was 74.9%. In major A&E the fall is steeper, from 94.9% to 60.9%. The worst month on record was December 2022, when only 49.6% of major A&E patients were seen within 4 hours.

**3. The problem is concentrated in major A&E.**
Minor injury units and urgent treatment centres (Type 3) still see about 97% of patients within 4 hours. The gap between Type 3 and Type 1 has widened from about 5 percentage points in 2011 to about 37 points in 2022–2025. Headline "all types" figures hide how stretched major departments are.

**4. Long waits for a bed have exploded.**
Patients waiting more than 12 hours from the decision to admit to actually getting a bed:

| Year | 12-hour waits |
|---|---|
| 2018-19 | 3,262 |
| 2021-22 | 98,564 |
| 2022-23 | 410,092 |
| 2025-26 | 570,957 |

That is 175 times the 2018-19 level, and equal to 12% of emergency admissions via major A&E. Meanwhile the share of major A&E patients who need admitting has stayed at roughly 27–30% (apart from the 2020-21 pandemic year). **This suggests the bottleneck is moving admitted patients into a ward bed (patient flow), not a rise in the share of patients who need admitting.**

**5. Winter is the pressure point.**
Over the last four complete years, major A&E performance averages about 60–61% from March to August and falls to 54.8% in December. Waits of 12+ hours for a bed peak in January, with 71,517 in January 2026 alone.

**6. Partial recovery since 2022.**
Major A&E performance has improved from 56.7% (2022-23) to 60.9% (2025-26) while attendances grew by 10% over the same period. The latest month, September 2026, was slightly worse than a year earlier: 60.6% vs 61.1% in major A&E, with 13% more 12-hour waits.

## Recommendations for further analysis

1. **Trust-level breakdown.** NHS England publishes the same data by provider. Ranking trusts would show whether the decline is national or concentrated in a few.
2. **Link to bed occupancy and delayed discharges.** If finding 4 is right, 12-hour waits should track general and acute bed occupancy closely.
3. **Forecast winter demand.** The strong seasonal pattern makes a simple time-series model (e.g. SARIMA) practical for planning winter capacity.

## Data caveats

- **Nov 2010 to May 2015:** NHS England estimated monthly figures from weekly returns.
- **May 2019 to May 2023:** 14 trusts taking part in the clinical review of access standards (CRS) were left out of the 4-hour figures. My reconciliation check (query 08) confirms it: in exactly these 49 months, the 4-hour counts don't add up to total attendances. Performance in this period is not fully comparable.
- **From Aug 2020:** attendances include booked appointments.
- **Aug 2022 to Feb 2023:** a cyber-attack caused a shortfall in Type 3 attendances.
- Percentages are calculated from patient totals, never by averaging monthly percentages.
