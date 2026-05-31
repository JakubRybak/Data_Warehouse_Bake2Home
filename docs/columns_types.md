# Column Types (BigQuery)

## FACT_ORDER_ITEM
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_ORDER_ITEM` | INT64 | |
| `ID_ORDER_ITEM` | INT64 | |
| `ID_ORDER` | INT64 | |
| `ID_BOUGHT_OFFER_INSTANCE` | INT64 | |
| `ID_CUSTOMER_ADDRESS` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_OFFER` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ID_PLANNER_ITEM` | INT64 | |
| `SK_DATE_ORDER` | DATE | Partition key |
| `SK_OFFER` | INT64 | |
| `SK_CUSTOMER_ADDRESS` | INT64 | |
| `SK_LOCATION` | INT64 | |
| `SK_SITE` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `PRICE` | NUMERIC | |
| `QUANTITY` | INT64 | |
| `VAT` | NUMERIC | |
| `GROSS_AMOUNT` | NUMERIC | Pre-calculated gross sales amount |
| `NET_AMOUNT` | NUMERIC | Pre-calculated net sales amount |
| `VAT_AMOUNT` | NUMERIC | Pre-calculated VAT amount |
| `MODIFIED_BY_HAND` | BOOL | |
| `BOUGHT_OFFER_INSTANCE_TYPE_ID` | INT64 | Mapped from C# |
| `BOUGHT_OFFER_INSTANCE_TYPE` | STRING | Mapped from C# |
| `ORDER_ITEM_STATE_ID` | INT64 | Mapped from C# |
| `ORDER_ITEM_STATE` | STRING | Mapped from C# |
| `ORDER_STATE_ID` | INT64 | Mapped from C# |
| `ORDER_STATE` | STRING | Mapped from C# |
| `CREATED_AT` | TIMESTAMP | Audit created timestamp |
| `WEATHER_MORNING_PRECIP_PROB` | INT64 | max prawdopodobieństwo opadu w oknie 6-10, % |
| `WEATHER_MORNING_PRECIP_SUM_MM` | NUMERIC | suma opadów w oknie 6-10, mm |
| `WEATHER_MORNING_WAS_RAINY` | BOOL | |
## DIM_SITE
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_SITE` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_CLIENT` | INT64 | |
| `ID_COORDINATES` | INT64 | |
| `CLIENT_NAME` | STRING | |
| `CLIENT_DESCRIPTION` | STRING | |
| `CLIENT_STREET` | STRING | |
| `CLIENT_CITY` | STRING | |
| `CLIENT_COUNTRY` | STRING | |
| `CLIENT_ZIP_CODE` | STRING | |
| `CLIENT_FULL_FORMAL_NAME` | STRING | |
| `NAME` | STRING | |
| `STREET` | STRING | |
| `NR` | STRING | |
| `CITY` | STRING | |
| `STATE` | STRING | |
| `COUNTRY` | STRING | |
| `ZIP_CODE` | STRING | |
| `LATITUDE` | FLOAT64 | |
| `LONGITUDE` | FLOAT64 | |
| `GEO_POINT` | GEOGRAPHY | |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |
## DIM_LOCATION
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_LOCATION` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `NAME` | STRING | |
| `DESCRIPTION` | STRING | |
| `STATE_ID` | INT64 | Mapped from C# |
| `STATE` | STRING | Mapped from C# |
| `VERTEXES` | STRING | |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |
## DIM_CUSTOMER_ADDRESS
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_CUSTOMER_ADDRESS` | INT64 | |
| `ID_CUSTOMER_ADDRESS` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ADDRESS_NAME` | STRING | |
| `ADDRESS` | STRING | |
| `LONGITUDE` | FLOAT64 | |
| `LATITUDE` | FLOAT64 | |
| `GEO_POINT` | GEOGRAPHY | |
| `ADDITIONAL_INFORMATION` | STRING | |
| `DIST_TO_NEAREST_OWN_SITE_M` | FLOAT64 | |
| `DIST_TO_NEAREST_COMP_BAKERY_M` | FLOAT64 | |
| `DIST_TO_NEAREST_COMP_SUPERMARKET_M` | FLOAT64 | |
| `COMP_BAKERY_COUNT_300M` | INT64 | |
| `COMP_BAKERY_COUNT_500M` | INT64 | |
| `COMP_BAKERY_COUNT_1000M` | INT64 | |
| `COMP_BAKERY_COUNT_2000M` | INT64 | |
| `COMP_SUPERMARKET_COUNT_500M` | INT64 | |
| `COMP_SUPERMARKET_COUNT_1000M` | INT64 | |
| `COMP_SUPERMARKET_COUNT_2000M` | INT64 | |
| `COMP_SUPERMARKET_COUNT_3000M` | INT64 | |
| `OWN_SITE_COUNT_300M` | INT64 | |
| `OWN_SITE_COUNT_500M` | INT64 | |
| `OWN_SITE_COUNT_1000M` | INT64 | |
| `OWN_SITE_COUNT_2000M` | INT64 | |
| `OWN_SITE_COUNT_3000M` | INT64 | |
| `STATE_ID` | INT64 | Mapped from C# |
| `STATE` | STRING | Mapped from C# |

## DIM_CUSTOMER
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_CUSTOMER` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `SK_CONSENT_PROFILE` | INT64 | Klucz do profilu zgód (dim_consent_profile) |
| `NAME` | STRING | |
| `CUSTOMER_STATE_ID` | INT64 | Mapped from C# |
| `CUSTOMER_STATE` | STRING | Mapped from C# |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |

## DIM_CONSENT_PROFILE
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_CONSENT_PROFILE` | INT64 | Klucz główny (PK) |
| `RODO_STATE_ID` | INT64 | Mapped from C# |
| `RODO_STATE` | STRING | Status zgody RODO |
| `TERMS_STATE_ID` | INT64 | Mapped from C# |
| `TERMS_STATE` | STRING | Status zgody na regulamin |
| `MARKETING_STATE_ID` | INT64 | Mapped from C# |
| `MARKETING_STATE` | STRING | Status zgody marketingowej |
## FACT_DELIVERY_ITEM
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_DELIVERY_ITEM` | INT64 | |
| `ID_DELIVERY_ITEM` | INT64 | |
| `ID_CUSTOMER_ADDRESS` | INT64 | |
| `ID_DELIVERY_MAN` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `ID_DELIVERY` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `ID_ORDER` | INT64 | |
| `SK_LOCATION` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `SK_DELIVERY_MAN` | INT64 | |
| `SK_SITE` | INT64 | |
| `SK_CUSTOMER_ADDRESS` | INT64 | |
| `SK_PRODUCT` | INT64 | |
| `SK_DATE_DELIVERY` | INT64 | |
| `PLANNED_QUANTITY` | INT64 | |
| `PACKED_QUANTITY` | INT64 | |
| `PRODUCT_PRICE` | NUMERIC | |
## DIM_DELIVERY_MAN
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_DELIVERY_MAN` | INT64 | |
| `ID_DELIVERY_MAN` | INT64 | |
| `NAME` | STRING | |
| `ID_SITE` | INT64 | |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |
## FACT_CLAIM_ITEM
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_CLAIM_ITEM` | INT64 | |
| `ID_CLAIM_ITEM` | INT64 | |
| `ID_CLAIM` | INT64 | |
| `ID_ORDER` | INT64 | |
| `ID_DELIVERY` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `SK_DATE_CLAIM` | INT64 | |
| `SK_PRODUCT` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `SK_SITE` | INT64 | |
| `SK_LOCATION` | INT64 | |
| `STATE` | STRING | |
| `TYPE` | STRING | |
| `ID_AGREED_DISCOUNT` | INT64 | |
| `AGREED_RETURN_AMOUNT` | NUMERIC | |
| `DESCRIPTION` | STRING | |
| `ORDERED_QUANTITY` | INT64 | |
| `DELIVERED_QUANTITY` | INT64 | |
| `NUMBER_OF_PRODUCTS_WITH_ACCEPTED_CLAIM` | INT64 | |
| `CLAIMED_QUANTITY` | INT64 | |
| `ISSUE_TYPE` | STRING | |
## FACT_PAYMENT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_PAYMENT` | INT64 | |
| `ID_PAYMENT` | INT64 | |
| `ID_ORDER` | INT64 | |
| `ID_DELIVERY` | INT64 | |
| `ID_DISCOUNT` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ID_CLIENT` | INT64 | |
| `ID_PAYMENT_METHOD` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `SK_SITE` | INT64 | |
| `SK_DISCOUNT` | INT64 | |
| `SK_PAYMENT_METHOD` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `SK_DATE_PAYMENT` | INT64 | |
| `SK_LOCATION` | INT64 | |
| `AMOUNT` | NUMERIC | |
| `LIST_OF_ORDER_ITEMS` | STRING | |
| `ERROR` | STRING | |
## DIM_PAYMENT_METHOD
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_PAYMENT_METHOD` | INT64 | |
| `ID_PAYMENT_METHOD` | INT64 | |
| `TYPE_ID` | INT64 | Mapped from C# |
| `TYPE` | STRING | Mapped from C# |
| `CURRENCY` | STRING | |
| `CARD_BRAND` | STRING | |
| `MOBILE` | BOOL | |
| `STATE_ID` | INT64 | Mapped from C# |
| `STATE` | STRING | Mapped from C# |
## FACT_CUSTOMER_CONSENT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_CUSTOMER_CONSENT` | INT64 | |
| `ID_CUSTOMER_CONSENT` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ID_CONSENT` | INT64 | |
| `SK_START_DATE` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `SK_END_DATE` | INT64 | |
| `IS_ACTIVE` | BOOL | |
| `CONSENT_NAME` | STRING | |
## FACT_PLANNER_ITEM
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_PLANNER_ITEM` | INT64 | |
| `ID_PLANNER_ITEM` | INT64 | |
| `ID_BOUGHT_OFFER_INSTANCE` | INT64 | |
| `ID_OFFER` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_CUSTOMER_ADDRESS` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `SK_CUSTOMER_ADDRESS` | INT64 | |
| `SK_SITE` | INT64 | |
| `SK_START_DATE` | INT64 | |
| `SK_END_DATE` | INT64 | |
| `SK_OFFER` | INT64 | |
| `SK_LOCATION` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `NEXT_VERSION` | STRING | |
| `PREVIOUS_VERSION` | STRING | |
| `DAY_INDEX` | INT64 | |
| `QUANTITY` | INT64 | |
| `PLANNER_ITEM_STATE` | STRING | |
| `DURATION_DAYS` | INT64 | |
| `IS_ACTIVE` | BOOL | |
## DIM_DISCOUNT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_DISCOUNT` | INT64 | |
| `ID_DISCOUNT` | INT64 | |
| `DISCOUNT_PERCENTAGE` | NUMERIC | |
| `DISCOUNT_FLAT_RATE` | NUMERIC | |
| `DISCOUNT_CODE` | STRING | |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |
| `USE_LIMIT_GLOBALLY` | INT64 | |
| `USE_LIMIT_PER_USER` | INT64 | |
| `MINIMAL_TRANSACTION_AMOUNT` | NUMERIC | |
| `ONLY_FOR_FIRST_PURCHASE` | BOOL | |
## DIM_PRODUCT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_PRODUCT` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `NAME` | STRING | |
| `DESCRIPTION` | STRING | |
| `STATE_ID` | INT64 | Mapped from C# |
| `STATE` | STRING | Mapped from C# |
| `PRODUCT_TYPE_NAME` | STRING | |
| `WEIGHT` | FLOAT64 | |
| `CALORIES` | FLOAT64 | |
| `TOTAL_FATS` | FLOAT64 | |
| `SATURATED_FATS` | FLOAT64 | |
| `TOTAL_CARBOHYDRATES` | FLOAT64 | |
| `SUGAR` | FLOAT64 | |
| `PROTEIN` | FLOAT64 | |
| `SODIUM` | FLOAT64 | |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |
## FACT_REFUND_ITEM
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_REFUND_ITEM` | INT64 | |
| `ID_REFUND_ITEM` | INT64 | |
| `ID_REFUND` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `ID_CLAIM` | INT64 | |
| `ID_PAYMENT` | INT64 | |
| `ID_SITE` | INT64 | |
| `ID_CUSTOMER` | INT64 | |
| `ID_CLIENT` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `SK_DATE_REFUND` | INT64 | |
| `SK_SITE` | INT64 | |
| `SK_PRODUCT` | INT64 | |
| `SK_CUSTOMER` | INT64 | |
| `SK_LOCATION` | INT64 | |
| `MISSING_PRODUCT_QUANTITY` | INT64 | |
| `AMOUNT` | NUMERIC | |
| `VAT_AMOUNT` | NUMERIC | |
## DIM_OFFER
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_OFFER` | INT64 | |
| `ID_OFFER` | INT64 | |
| `NAME` | STRING | |
| `PRICE` | NUMERIC | |
| `STATE_ID` | INT64 | Mapped from C# |
| `STATE` | STRING | Mapped from C# |
| `TYPE_ID` | INT64 | Mapped from C# |
| `TYPE` | STRING | Mapped from C# |
| `VAT` | NUMERIC | |
| `VALID_FROM` | TIMESTAMP | |
| `VALID_TO` | TIMESTAMP | |
| `IS_CURRENT` | BOOL | |
## BRIDGE_OFFER_PRODUCT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_OFFER_PRODUCT` | INT64 | |
| `ID_OFFER_PRODUCT` | INT64 | |
| `ID_OFFER` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `PRODUCT_COUNT` | INT64 | |
| `PRODUCT_IN_OFFER_COUNT` | INT64 | |
## DIM_DATE
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_DATE` | INT64 | |
| `MONTH_NAME` | STRING | |
| `WEEKDAY_NAME` | STRING | |
| `IS_WORKING` | BOOL | |
| `IS_HOLIDAY` | BOOL | |
| `IS_WEEKEND` | BOOL | |
| `WEEKDAY_NUMBER` | INT64 | |
| `MONTH_NUMBER` | INT64 | |
| `YEAR` | INT64 | |
| `QUARTER` | INT64 | |
## DIM_INGREDIENT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_INGREDIENT` | INT64 | |
| `ID_INGREDIENT` | INT64 | |
| `NAME` | STRING | |
| `Unit` | STRING | |
| `IS_PUBLIC` | BOOL | |
## BRIDGE_PRODUCT_INGREDIENT
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_PRODUCT_INGREDIENT` | INT64 | |
| `ID_PRODUCT_INGREDIENT` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `ID_INGREDIENT` | INT64 | |
| `VALUE` | FLOAT64 | |
| `IS_PUBLIC` | BOOL | |
## DIM_ALLERGEN
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_ALLERGEN` | INT64 | |
| `ID_ALLERGEN` | INT64 | |
| `NAME` | STRING | |
## BRIDGE_PRODUCT_ALLERGEN
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_PRODUCT_ALLERGEN` | INT64 | |
| `ID_PRODUCT_ALLERGEN` | INT64 | |
| `ID_PRODUCT` | INT64 | |
| `ID_ALLERGEN` | INT64 | |
## DIM_COMPETITOR
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_COMPETITOR` | INT64 | |
| `ID_COMPETITOR` | STRING | Google Places API unique place ID |
| `NAME` | STRING | |
| `ADDRESS` | STRING | |
| `LATITUDE` | FLOAT64 | |
| `LONGITUDE` | FLOAT64 | |
| `GEO_POINT` | GEOGRAPHY | |
| `COMPETITOR_TYPE` | STRING | DIRECT (bakery) or INDIRECT (supermarket) |
| `GOOGLE_TYPES` | ARRAY<STRING> | Raw Google API Place types list |
| `EXTRACTED_AT` | TIMESTAMP | ETL extraction audit timestamp |
## BRIDGE_LOCATION_SITE
| Kolumna | Typ w BigQuery | Uwagi |
| :--- | :--- | :--- |
| `SK_LOCATION_SITE` | INT64 | |
| `ID_LOCATION_SITE` | INT64 | |
| `ID_LOCATION` | INT64 | |
| `ID_SITE` | INT64 | |
 