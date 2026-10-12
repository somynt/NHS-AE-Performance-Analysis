-- Star schema for NHS England monthly A&E data
-- One dimension (month) and three fact tables, all keyed on month_key (YYYYMM).

DROP TABLE IF EXISTS dim_month;
DROP TABLE IF EXISTS fact_activity;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_booked;

CREATE TABLE dim_month (
    month_start                 TEXT,       -- first day of month, YYYY-MM-DD
    month_key                   INTEGER PRIMARY KEY,
    year                        INTEGER,
    month_num                   INTEGER,
    month_name                  TEXT,
    month_label                 TEXT,
    financial_year              TEXT,       -- NHS year, April to March, e.g. 2025-26
    season                      TEXT,
    flag_estimated_from_weekly  INTEGER,    -- Nov 2010 to May 2015: estimated from weekly returns
    flag_crs_field_test         INTEGER,    -- May 2019 to May 2023: 14 trusts missing from 4-hour data
    flag_includes_booked        INTEGER,    -- from Aug 2020: booked appointments counted
    flag_cyber_attack_type3     INTEGER,    -- Aug 2022 to Feb 2023: Type 3 shortfall
    flag_covid_period           INTEGER     -- Mar 2020 to Mar 2021
);

CREATE TABLE fact_activity (
    month_key        INTEGER PRIMARY KEY REFERENCES dim_month(month_key),
    att_type1        INTEGER,   -- major A&E departments
    att_type2        INTEGER,   -- single specialty (e.g. eye hospitals)
    att_type3        INTEGER,   -- urgent treatment centres, minor injury units
    att_total        INTEGER,
    adm_via_type1    INTEGER,
    adm_via_type2    INTEGER,
    adm_via_type3_4  INTEGER,
    adm_via_ae_total INTEGER,
    adm_other        INTEGER,   -- emergency admissions not via A&E
    adm_total        INTEGER,
    dta_over_4hrs    INTEGER,   -- waited >4h from decision to admit to admission
    dta_over_12hrs   INTEGER    -- waited >12h from decision to admit to admission
);

CREATE TABLE fact_performance (
    month_key      INTEGER PRIMARY KEY REFERENCES dim_month(month_key),
    within4_type1  INTEGER,
    within4_type2  INTEGER,
    within4_type3  INTEGER,
    within4_total  INTEGER,
    over4_type1    INTEGER,
    over4_type2    INTEGER,
    over4_type3    INTEGER,
    over4_total    INTEGER
);

CREATE TABLE fact_booked (
    month_key             INTEGER PRIMARY KEY REFERENCES dim_month(month_key),
    booked_type1          INTEGER,
    booked_type2          INTEGER,
    booked_type3          INTEGER,
    booked_total          INTEGER,
    booked_within4_total  INTEGER,
    booked_over4_total    INTEGER
);
