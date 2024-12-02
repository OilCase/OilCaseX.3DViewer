-- Этот файл был сгенерирован тНавигатор v23.3-4280-ged8ebf643115.
-- Copyright (C) Рок Флоу Динамикс 2005-2023.
-- Все права защищены.


SPECGRID
 69 50 75 /

INCLUDE
'INCLUDE/DynamicModel.grdecl' /

INCLUDE
'INCLUDE/DynamicModel_WELLTRACK.inc' /


INIT

INCLUDE
'INCLUDE/DynamicModel_ACTNUM.inc' /

INCLUDE
'INCLUDE/DynamicModel_PERMX.inc' /

INCLUDE
'INCLUDE/DynamicModel_PERMY.inc' /

INCLUDE
'INCLUDE/DynamicModel_PERMZ.inc' /

INCLUDE
'INCLUDE/DynamicModel_PORO.inc' /

FRACTURE_ARITHMETIC
    'ARITHMETIC_one' /
        PERMX (zone : ALL) = LINEAR_VERTICAL (100, 1) /
/