-- Этот файл был сгенерирован тНавигатор v23.3-4280-ged8ebf643115.
-- Copyright (C) Рок Флоу Динамикс 2005-2023.
-- Все права защищены.

RPTSCHED
'WELLS=2' 'SUMMARY=2' 'fip=3' 'RESTART=1' 'WELSPECS' 'CPU=2' /

INCLUDE
'INCLUDE/DynamicModel_VFP.inc' /

INCLUDE
'INCLUDE/DynamicModel_WELLTRACK.inc' /


WELSPECS
-- wname   gname iw jw ref.depth phase radius inflow_flag shut-in_flag crossflow_ability_flag PVT_n density_type filt.tbl reserved reserved well_model_type polymer_mixing_tbl.n
   'E01'   1*    2*    /
   'E02'   1*    2*    /
   'E03'   1*    2*    /
   'E04'   1*    2*    /
   'E05'   1*    2*    /
   'E06'   1*    2*    /
   'E07'   1*    2*    /
   'E08'   1*    2*    /
   'E09'   1*    2*    /
   'E10'   1*    2*    /
   'Etest' 1*    2*    /
/

COMPDATMD
-- wname|stage_name branch|stage_num mdl|delta1 mdu|delta2 md_type status filt.tbl pi diameter Kh skin D-factor cf_mult DP completion
   'E01'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E02'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E03'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E04'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E05'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E06'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E07'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E08'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E09'            1*               500        2600       MD      OPEN   2*          0.114    /
   'E10'            1*               500        2600       MD      OPEN   2*          0.114    /
   'Etest'          1*               500        2600       MD      OPEN   2*          0.114    /
/

COMPORD
-- wname   sort
   'E01'   INPUT /
   'E02'   INPUT /
   'E03'   INPUT /
   'E04'   INPUT /
   'E05'   INPUT /
   'E06'   INPUT /
   'E07'   INPUT /
   'E08'   INPUT /
   'E09'   INPUT /
   'E10'   INPUT /
   'Etest' INPUT /
/

DATES
 01 JAN 2024 /
 /



WCONPROD
-- wname status control orate wrate grate lrate lrate(rc) BHP THP VFP_n ALQ wgrate mlrate steam sat.pressure sat.temperature calorific_rate linearly_combined_rate NGL_rate
   'E01' OPEN   BHP     5*                                200 /
   'E02' OPEN   BHP     5*                                200 /
   'E03' OPEN   BHP     5*                                200 /
   'E04' OPEN   BHP     5*                                200 /
   'E05' OPEN   BHP     5*                                200 /
   'E06' OPEN   BHP     5*                                200 /
   'E07' OPEN   BHP     5*                                200 /
   'E08' OPEN   BHP     5*                                200 /
   'E09' OPEN   BHP     5*                                200 /
   'E10' OPEN   BHP     5*                                200 /
/

DATES
 12 FEB 2024 /
 /



DATES
 12 MAR 2024 /
 /



DATES
 12 APR 2024 /
 /



DATES
 12 MAY 2024 /
 /



DATES
 12 JUN 2024 /
 /



DATES
 12 JUL 2024 /
 /



DATES
 12 AUG 2024 /
 /



DATES
 12 SEP 2024 /
 /



DATES
 12 OCT 2024 /
 /



DATES
 12 NOV 2024 /
 /



DATES
 12 DEC 2024 /
 /



DATES
 12 JAN 2025 /
 /



DATES
 12 FEB 2025 /
 /



DATES
 12 MAR 2025 /
 /



DATES
 12 APR 2025 /
 /



DATES
 12 MAY 2025 /
 /



DATES
 12 JUN 2025 /
 /



DATES
 12 JUL 2025 /
 /



DATES
 12 AUG 2025 /
 /



DATES
 12 SEP 2025 /
 /



DATES
 12 OCT 2025 /
 /



DATES
 12 NOV 2025 /
 /



DATES
 12 DEC 2025 /
 /



DATES
 12 JAN 2026 /
 /



DATES
 12 FEB 2026 /
 /



DATES
 12 MAR 2026 /
 /



DATES
 12 APR 2026 /
 /



DATES
 12 MAY 2026 /
 /



DATES
 12 JUN 2026 /
 /



DATES
 12 JUL 2026 /
 /



DATES
 12 AUG 2026 /
 /



DATES
 12 SEP 2026 /
 /



DATES
 12 OCT 2026 /
 /



DATES
 12 NOV 2026 /
 /



DATES
 12 DEC 2026 /
 /



DATES
 12 JAN 2027 /
 /



DATES
 12 FEB 2027 /
 /



DATES
 12 MAR 2027 /
 /



DATES
 12 APR 2027 /
 /



DATES
 12 MAY 2027 /
 /



DATES
 12 JUN 2027 /
 /



DATES
 12 JUL 2027 /
 /



DATES
 12 AUG 2027 /
 /



DATES
 12 SEP 2027 /
 /



DATES
 12 OCT 2027 /
 /



DATES
 12 NOV 2027 /
 /



DATES
 12 DEC 2027 /
 /



DATES
 12 JAN 2028 /
 /



DATES
 12 FEB 2028 /
 /



DATES
 12 MAR 2028 /
 /



DATES
 12 APR 2028 /
 /



DATES
 12 MAY 2028 /
 /



DATES
 12 JUN 2028 /
 /



DATES
 12 JUL 2028 /
 /



DATES
 12 AUG 2028 /
 /



DATES
 12 SEP 2028 /
 /



DATES
 12 OCT 2028 /
 /



DATES
 12 NOV 2028 /
 /



DATES
 12 DEC 2028 /
 /



DATES
 12 JAN 2029 /
 /



DATES
 12 FEB 2029 /
 /



DATES
 12 MAR 2029 /
 /



DATES
 12 APR 2029 /
 /



DATES
 12 MAY 2029 /
 /



DATES
 12 JUN 2029 /
 /



DATES
 12 JUL 2029 /
 /



DATES
 12 AUG 2029 /
 /



DATES
 12 SEP 2029 /
 /



DATES
 12 OCT 2029 /
 /



DATES
 12 NOV 2029 /
 /



DATES
 12 DEC 2029 /
 /



DATES
 12 JAN 2030 /
 /



DATES
 12 FEB 2030 /
 /



DATES
 12 MAR 2030 /
 /



DATES
 12 APR 2030 /
 /



DATES
 12 MAY 2030 /
 /



DATES
 12 JUN 2030 /
 /



DATES
 12 JUL 2030 /
 /



DATES
 12 AUG 2030 /
 /



DATES
 12 SEP 2030 /
 /



DATES
 12 OCT 2030 /
 /



DATES
 12 NOV 2030 /
 /



DATES
 12 DEC 2030 /
 /



DATES
 12 JAN 2031 /
 /



DATES
 12 FEB 2031 /
 /



DATES
 12 MAR 2031 /
 /



DATES
 12 APR 2031 /
 /



DATES
 12 MAY 2031 /
 /



DATES
 12 JUN 2031 /
 /



DATES
 12 JUL 2031 /
 /



DATES
 12 AUG 2031 /
 /



DATES
 12 SEP 2031 /
 /



DATES
 12 OCT 2031 /
 /



DATES
 12 NOV 2031 /
 /



DATES
 12 DEC 2031 /
 /



DATES
 12 JAN 2032 /
 /



DATES
 12 FEB 2032 /
 /



DATES
 12 MAR 2032 /
 /



DATES
 12 APR 2032 /
 /



DATES
 12 MAY 2032 /
 /



DATES
 12 JUN 2032 /
 /



DATES
 12 JUL 2032 /
 /



DATES
 12 AUG 2032 /
 /



DATES
 12 SEP 2032 /
 /



DATES
 12 OCT 2032 /
 /



DATES
 12 NOV 2032 /
 /



DATES
 12 DEC 2032 /
 /



DATES
 12 JAN 2033 /
 /



DATES
 12 FEB 2033 /
 /



DATES
 12 MAR 2033 /
 /



DATES
 12 APR 2033 /
 /



DATES
 12 MAY 2033 /
 /



DATES
 12 JUN 2033 /
 /



DATES
 12 JUL 2033 /
 /



DATES
 12 AUG 2033 /
 /



DATES
 12 SEP 2033 /
 /



DATES
 12 OCT 2033 /
 /



DATES
 12 NOV 2033 /
 /



DATES
 12 DEC 2033 /
 /



DATES
 01 JAN 2034 /
 /


END
