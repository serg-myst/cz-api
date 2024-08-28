KIZ_STATUS = [
    {"kiz_id": 1,
     "db_code": 0,
     "code": "EMITTED",
     "description": "Эмитирован"
     },
    {"kiz_id": 2,
     "db_code": 1,
     "code": "APPLIED",
     "description": "Нанесён"
     },
    {"kiz_id": 3,
     "db_code": 2,
     "code": "INTRODUCED",
     "description": "В обороте"
     },
    {"kiz_id": 4,
     "db_code": 3,
     "code": "WRITTEN_OFF",
     "description": "Списан"
     },
    {"kiz_id": 5,
     "db_code": 4,
     "code": "RETIRED",
     "description": "Выбыл (для всех товарных групп, кроме Альтернативная табачная продукция,"
                    "Никотиносодержащая продукция, Табачная продукция)"
     },
    {"kiz_id": 6,
     "db_code": 4,
     "code": "WITHDRAWN",
     "description": "Выбыл (только для товарных групп Альтернативная табачная продукция,"
                    " Никотиносодержащая продукция, Табачная продукция)"
     },
    {"kiz_id": 7,
     "db_code": 7,
     "code": "DISAGGREGATION",
     "description": "Расформирован (для всех товарных групп, кроме Альтернативная табачная продукция,"
                    " Никотиносодержащая продукция, Табачная продукция)"
     },
    {"kiz_id": 8,
     "db_code": 7,
     "code": "DISAGGREGATED",
     "description": "Расформирован (только для товарных групп Альтернативная табачная продукция,"
                    " Никотиносодержащая продукция, Табачная продукция)"
     },
    {"kiz_id": 9,
     "db_code": 12,
     "code": "APPLIED_NOT_PAID",
     "description": "Не оплачен (только для товарных групп Альтернативная табачная продукция,"
                    " Никотиносодержащая продукция, Табачная продукция)"
     }
]

PRODUCT_GROUP = [
    {"group_id": 1,
     "group_name": "lp",
     "description": "Предметы одежды, бельё постельное, столовое, туалетное икухонное"
     },
    {"group_id": 2,
     "group_name": "shoes",
     "description": "Обувные товары"
     },
    {"group_id": 3,
     "group_name": "tobacco",
     "description": "Табачная продукция"
     },
    {"group_id": 4,
     "group_name": "perfumery",
     "description": "Духи и туалетная вода"
     },
    {"group_id": 5,
     "group_name": "tires",
     "description": "Шины и покрышки пневматические резиновые новые"
     },
    {"group_id": 6,
     "group_name": "electronics",
     "description": "Фотокамеры (кроме кинокамер), фотовспышки и лампывспышки"
     },
    {"group_id": 8,
     "group_name": "milk",
     "description": "Молочная продукция"
     },
    {"group_id": 9,
     "group_name": "bicycle",
     "description": "Велосипеды и велосипедные рамы"
     },
    {"group_id": 10,
     "group_name": "wheelchairs",
     "description": "Медицинские изделия"
     },
    {"group_id": 12,
     "group_name": "otp",
     "description": "Альтернативная табачная продукция"
     },
    {"group_id": 13,
     "group_name": "water",
     "description": "Упакованная вода"
     },
    {"group_id": 14,
     "group_name": "furs",
     "description": "Товары из натурального меха"
     },
    {"group_id": 15,
     "group_name": "beer",
     "description": "Пиво, напитки, изготавливаемые на основе пива,слабоалкогольные напитки"
     },
    {"group_id": 16,
     "group_name": "ncp",
     "description": "Никотиносодержащая продукция"
     },
    {"group_id": 17,
     "group_name": "bio",
     "description": "Биологически активные добавки к пище"
     },
    {"group_id": 19,
     "group_name": "antiseptic",
     "description": "Антисептики и дезинфицирующие средства"
     },
    {"group_id": 20,
     "group_name": "petfood",
     "description": "Корма для домашних животных (кромесельскохозяйственных) расфасованные в потребительскую упаковку"
     },
    {"group_id": 21,
     "group_name": "seafood",
     "description": "Морепродукты"
     },
    {"group_id": 22,
     "group_name": "nabeer",
     "description": "Безалкогольное пиво"
     },
    {"group_id": 23,
     "group_name": "softdrinks",
     "description": "Соковая продукция и безалкогольные напитки"
     },
    {"group_id": 27,
     "group_name": "toys",
     "description": "Игры и игрушки для детей"
     },
    {"group_id": 28,
     "group_name": "radio",
     "description": "Радиоэлектронная продукция"
     },
    {"group_id": 31,
     "group_name": "titan",
     "description": "Титановая металлопродукция"
     },
    {"group_id": 33,
     "group_name": "vegetableoil",
     "description": "Растительные масла"
     },
    {"group_id": 34,
     "group_name": "opticfiber",
     "description": "Оптоволокно и оптоволоконная продукция"
     },
    {"group_id": 35,
     "group_name": "chemistry",
     "description": "Парфюмерные и косметические средства и бытовая химия"
     },
]

EMISSION_TYPE = [
    {"type_id": "LOCAL",
     "description": "Производство РФ"
     },
    {"type_id": "FOREIGN",
     "description": "Ввезён в РФ"
     },
    {"type_id": "REMAINS",
     "description": "Маркировка остатков"
     },
    {"type_id": "CROSSBORDER",
     "description": "Ввезён из стран ЕАЭС"
     },
    {"type_id": "REMARK",
     "description": "Перемаркировка"
     },
    {"type_id": "COMMISSION",
     "description": "Принят на комиссию от физического лица"
     }
]

PACKAGE_TYPE = [
    {"type_id": "UNIT",
     "description": "Единица товара (КИ)",
     "comment_tobaco": "Пачка",
     "comment_other": "Потребительская упаковка"
     },
    {"type_id": "GROUP",
     "description": "Групповая упаковка (КИГУ)",
     "comment_tobaco": "",
     "comment_other": "Используется только для дезинфицирующие средства, Биологически активные добавки к пище,"
                      " Медицинские изделия, Молочная продукция, Морепродукты, Пиво, напитки,"
                      " изготавливаемые на основе пива, слабоалкогольные напитки»,"
                      " Соковая продукция и безалкогольные напитки, Упакованная вода"
     },
    {"type_id": "SET",
     "description": "Набор (КИН)",
     "comment_tobaco": "Используется только для товарной группы Никотиносодержащая продукция",
     "comment_other": "Используется только для товарных групп Антисептики и дезинфицирующие средства,"
                      " Биологически активные добавки к пище, Духи итуалетная вода, Медицинские изделия,"
                      " Молочная продукция, Предметы одежды, бельё постельное, столовое, туалетное икухонное, "
                      " Соковая продукцияи безалкогольные напитки, Фотокамеры (кромекинокамер),"
                      " фотовспышки и лампы-вспышки"
     },
    {"type_id": "BUNDLE",
     "description": "Комплект (КИК)",
     "comment_tobaco": "",
     "comment_other": "Используется только для товарной группы Предметы одежды, бельё постельное, столовое,"
                      " туалетное и кухонное"
     },
    {"type_id": "BOX",
     "description": "Транспортная упаковка (КИТУ)",
     "comment_tobaco": "",
     "comment_other": ""
     },
    {"type_id": "ATK",
     "description": "Агрегированный таможенный код (АТК)",
     "comment_tobaco": "В составе АТК может быть только КИ, КИК, КИГУ, КИТУ",
     "comment_other": "В составе АТК может быть только КИ, КИК, КИГУ, КИТУ"
     },
    {"type_id": "LEVEL1",
     "description": "Транспортная упаковка 1-го уровня (КИТУ)",
     "comment_tobaco": "Также может быть групповой упаковкой (КИГУ) - блок",
     "comment_other": ""
     },
    {"type_id": "LEVEL2",
     "description": "Транспортная упаковка 2-го уровня (КИТУ)",
     "comment_tobaco": "Короб",
     "comment_other": ""
     },
    {"type_id": "LEVEL3",
     "description": "Транспортная упаковка 3-го уровня (КИТУ)",
     "comment_tobaco": "Палета",
     "comment_other": ""
     },
    {"type_id": "LEVEL4",
     "description": "Транспортная упаковка 4-го уровня (КИТУ)",
     "comment_tobaco": "",
     "comment_other": ""
     },
    {"type_id": "LEVEL5",
     "description": "Транспортная упаковка 5-го уровня (КИТУ)",
     "comment_tobaco": "",
     "comment_other": ""
     }
]

REPORT_STATUS = [
    {"status_id": 1,
     "status_name": "PREPARATION",
     "description": "Подготовка"
     },
    {"status_id": 2,
     "status_name": "COMPLETED",
     "description": "Выполнено"
     },
    {"status_id": 3,
     "status_name": "CANCELED",
     "description": "Отменено"
     },
    {"status_id": 4,
     "status_name": "ARCHIVE",
     "description": "Архив"
     },
    {"status_id": 5,
     "status_name": "FAILED",
     "description": "Ошибка"
     },
]
