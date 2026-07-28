# 2-D x_HI model variants

All 29 completed runs re-evaluated on the same 384 held-out test slices. Sorted by RMSE.

RMSE is not the whole story: the L2-free runs are not optimising it, and `width`/`blur` should be compared against the TRUTH row rather than between models.

| run | architecture | train loss | params | params (log) | best val L2 | RMSE | wall | expwall | width | blur |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| whno_glob_lr3e4 | local fno / global whno | 1*L2 | 465,377 | 539,105 | 0.1060 | 0.14479 | 0.00587 | 0.02566 | 2.89 | 0.2027 |
| whno_glob_ctrglobal | local fno / global whno | 1*L2  [contrast global/sigmoid] | 465,379 | 539,107 | 0.1062 | 0.14499 | 0.00586 | 0.02585 | 2.95 | 0.2026 |
| whno_glob_ctrsched | local fno / global whno | 1*L2  [contrast xhi/sigmoid] | 465,377 | 539,105 | 0.1064 | 0.14526 | 0.00602 | 0.02599 | 2.92 | 0.2024 |
| whno_glob_h1semi | local fno / global whno | 1*H1semi | 465,377 | 539,105 | 0.1083 | 0.14540 | 0.00488 | 0.02907 | 3.14 | 0.1967 |
| whno_glob_ctrrefit | local fno / global whno | 1*L2  [contrast xhi/sigmoid] | 465,381 | 539,109 | 0.1059 | 0.14546 | 0.00569 | 0.02625 | 2.95 | 0.2033 |
| whno_glob_ctrfix040 | local fno / global whno | 1*L2  [contrast xhi/sigmoid] | 465,377 | 539,105 | 0.1061 | 0.14548 | 0.00559 | 0.02647 | 2.86 | 0.2022 |
| localfno_lr3e4_e30 | local fno / global fno | 1*L2 | 596,449 | 932,321 | 0.1069 | 0.14607 | 0.00514 | 0.02528 | 2.75 | 0.1934 |
| whno_glob_ctrrefit_swd | local fno / global whno | 1*L2 + 140*SWD  [contrast xhi/sigmoid] | 465,381 | 539,109 | 0.1063 | 0.14658 | 0.00527 | 0.02572 | 2.84 | 0.1977 |
| whno_glob_swd | local fno / global whno | 1*L2 + 140*SWD | 465,377 | 539,105 | 0.1072 | 0.14666 | 0.00498 | 0.02554 | 2.66 | 0.1939 |
| whno_glob_ctrhead | local fno / global whno | 1*L2  [contrast head/sigmoid] | 466,723 | 540,451 | 0.1055 | 0.14676 | 0.00573 | 0.02632 | 2.76 | 0.1974 |
| whno_glob_highk | local fno / global whno | 0.12*highK + 1*L2 | 465,377 | 539,105 | 0.1083 | 0.14686 | 0.00447 | 0.02559 | 2.18 | 0.1874 |
| whno_glob_ctrfix040_swd | local fno / global whno | 1*L2 + 140*SWD  [contrast xhi/sigmoid] | 465,377 | 539,105 | 0.1073 | 0.14692 | 0.00528 | 0.02625 | 2.68 | 0.1961 |
| whno_glob_edge | local fno / global whno | 0.12*highK + 1*L2 + 140*SWD | 465,377 | 539,105 | 0.1089 | 0.14905 | 0.00403 | 0.02559 | 2.15 | 0.1831 |
| localwno_lr3e4_w48r24 | local wno / global fno | 1*L2 | 1,189,585 | 1,779,409 | 0.1076 | 0.14910 | 0.00558 | 0.02506 | 2.89 | 0.1973 |
| whno_both_bce | local whno / global whno | 1*BCE | 428,513 | 428,513 | 0.1096 | 0.14922 | 0.00611 | 0.02746 | 2.93 | 0.2058 |
| whno_both_lr3e4 | local whno / global whno | 1*L2 | 428,513 | 428,513 | 0.1082 | 0.15062 | 0.00607 | 0.02707 | 2.86 | 0.2035 |
| localwno_lr2e4_e30 | local wno / global fno | 1*L2 | 529,889 | 792,033 | 0.1090 | 0.15099 | 0.00614 | 0.02714 | 3.08 | 0.2057 |
| whno_loc_w48r24 | local whno / global fno | 1*L2 | 1,256,401 | 1,846,225 | 0.1074 | 0.15239 | 0.00542 | 0.02524 | 2.79 | 0.1905 |
| whno_loc_m12_lr3e4 | local whno / global fno | 1*L2 | 670,177 | 932,321 | 0.1096 | 0.15329 | 0.00613 | 0.02698 | 2.91 | 0.2020 |
| whno_loc_natural | local whno / global fno | 1*L2 | 559,585 | 821,729 | 0.1086 | 0.15360 | 0.00608 | 0.02713 | 2.92 | 0.1971 |
| whno_loc_lr3e4 | local whno / global fno | 1*L2 | 559,585 | 821,729 | 0.1093 | 0.15366 | 0.00598 | 0.02708 | 2.85 | 0.1966 |
| localwno_lr3e4_e30 | local wno / global fno | 1*L2 | 529,889 | 792,033 | 0.1111 | 0.15452 | 0.00624 | 0.02746 | 2.90 | 0.2016 |
| localwno_lr3e4_h1e3 | local wno / global fno | 0.001*H1 + 1*L2 | 529,889 | 792,033 | 0.1099 | 0.15501 | 0.00629 | 0.02742 | 2.78 | 0.1984 |
| ufno_lr3e4_e30 | U-FNO | 1*L2 | 13,034,689 | 25,617,601 | 0.1132 | 0.15587 | 0.00657 | 0.02878 | 2.77 | 0.1926 |
| localwno_lr3e4_r32 | local wno / global fno | 1*L2 | 1,352,161 | 2,400,737 | 0.1106 | 0.15725 | 0.00635 | 0.02756 | 2.81 | 0.1953 |
| whno_glob_expwall16 | local fno / global whno | 1*expwall | 465,377 | 539,105 | 0.1273 | 0.17671 | 0.00261 | 0.02097 | 1.16 | 0.0963 |
| whno_glob_expwall8 | local fno / global whno | 1*expwall | 465,377 | 539,105 | 0.1470 | 0.19672 | 0.00268 | 0.02738 | 1.36 | 0.1060 |
| whno_glob_expwall4 | local fno / global whno | 1*expwall | 465,377 | 539,105 | 0.3040 | 0.52212 | 0.04207 | 0.15547 | 0.13 | 0.0092 |
| whno_glob_edgeonly | local fno / global whno | 0.12*highK + 140*SWD | 465,377 | 539,105 | 0.8462 | 0.91965 | 0.36791 | 0.94746 | 1.43 | 0.1468 |
| **TRUTH** | | | | | | | | | **1.46** | **0.1014** |
