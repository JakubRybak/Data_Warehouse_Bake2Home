# Measures, Attributes, and Hierarchies

## 1. Measures and Aggregation Methods

### FACT_ORDER_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `PRICE` | Value/Price for a given product/offer | **SUM** (Revenue), **AVG** (Average price) |
| `QUANTITY` | Quantity of ordered items | **SUM** |
| `VAT` | VAT tax amount | **SUM** |
| `GROSS_AMOUNT` | Pre-calculated gross sales amount | **SUM** |
| `NET_AMOUNT` | Pre-calculated net sales amount | **SUM** |
| `VAT_AMOUNT` | Pre-calculated VAT amount | **SUM** |
| `WEATHER_MORNING_WAS_RAINY` | (`PRECIP_PROB` >= 50 AND `PRECIP_SUM_MM` >= 1.0) OR (`PRECIP_SUM_MM` >= 2.5) | **CUSTOM** |

### FACT_DELIVERY_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `PLANNED_QUANTITY` | Quantity planned for delivery | **SUM** |
| `PACKED_QUANTITY` | Quantity actually packed | **SUM** |
| `PRODUCT_PRICE` | Value of the product in delivery | **SUM** |

### FACT_CLAIM_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `AGREED_RETURN_AMOUNT` | Agreed return amount for the customer | **SUM** |
| `ORDERED_QUANTITY` | Initially ordered quantity (context) | **SUM**, **MAX** |
| `DELIVERED_QUANTITY` | Actually delivered quantity (context) | **SUM**, **MAX** |
| `NUMBER_OF_PRODUCTS_WITH_ACCEPTED_CLAIM` | Number of accepted products in the claim | **SUM** |
| `CLAIMED_QUANTITY` | Quantity reported in the claim | **SUM** |

### FACT_PAYMENT & FACT_REFUND_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `AMOUNT` (PAYMENT) | Booked payment amount | **SUM** |
| `AMOUNT` (REFUND) | Actual refund amount (net/gross) | **SUM** |
| `VAT_AMOUNT` | Refunded VAT amount | **SUM** |
| `MISSING_PRODUCT_QUANTITY` | Quantity of missing products forming the basis of the refund | **SUM** |

### FACT_PLANNER_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `QUANTITY` | Number of items in the subscription plan | **SUM** |
| `DURATION_DAYS` | Duration of the plan / cycle | **AVG**, **MAX** |
| `PRICE` | Value/Price for a given subscription offer | **SUM** (Planned Revenue), **AVG** |
| `VAT` | VAT rate for the offer | **AVG** |
| `GROSS_AMOUNT` | Pre-calculated gross planned amount | **SUM** |
| `NET_AMOUNT` | Pre-calculated net planned amount | **SUM** |
| `VAT_AMOUNT` | Pre-calculated VAT planned amount | **SUM** |

---

## 2. Key Attributes

### Spatial and Logistics Attributes (GIS)
**Tables:** `DIM_SITE`, `DIM_CUSTOMER_ADDRESS`, `DIM_COMPETITOR`
* **Categorizing:** `CITY`, `ZIP_CODE`, `STATE`, `COUNTRY`, `STREET`.
* **GIS (Coordinates):** `LATITUDE`, `LONGITUDE`, **`GEO_POINT`**.
* **Reach Indicators in `DIM_CUSTOMER_ADDRESS`:** 
  * `DIST_TO_NEAREST_OWN_SITE_M`, `DIST_TO_NEAREST_COMP_BAKERY_M`, `DIST_TO_NEAREST_COMP_SUPERMARKET_M`
  * `COMP_BAKERY_COUNT_500M`, `OWN_SITE_COUNT_1000M`

### Product and Marketing Attributes
**Tables:** `DIM_PRODUCT`, `DIM_OFFER`, `DIM_DISCOUNT`, `DIM_INGREDIENT`
* **Categorizing:** `PRODUCT_TYPE_NAME`, `TYPE` (in offer), `COMPETITOR_TYPE` (Competitor).
* **Technical/Nutritional:** `CALORIES`, `TOTAL_FATS`, `SUGAR`.
* **Promotional:** `DISCOUNT_CODE`, `ONLY_FOR_FIRST_PURCHASE`.

### Status Attributes
* **In orders:** `ORDER_ITEM_STATE`, `ORDER_STATE`, `MODIFIED_BY_HAND`.
* **In planner:** `PLANNER_ITEM_STATE`.
* **In customers:** `CUSTOMER_STATE`.
* **In payments:** `TYPE`, `CARD_BRAND`, `MOBILE`.
* **In claims:** `STATE`, `ISSUE_TYPE`.

---

## 3. Analytical Hierarchies

### A. Time Hierarchy (`DIM_DATE`)
1. `YEAR`
2. `QUARTER`
3. `MONTH_NAME` / `MONTH_NUMBER`
4. `WEEKDAY_NAME` / `WEEKDAY_NUMBER`
5. `SK_DATE`

### B. Geographical Hierarchy
1. `COUNTRY`
2. `STATE`
3. `CITY`
4. `ZIPCODE`
5. `STREET` / `ADDRESS`

### C. Operational-Management Hierarchy
1. `DIM_LOCATION`
2. `DIM_SITE`
*(Note: `DIM_DELIVERY_MAN` and `DIM_CUSTOMER` are independent dimensions. They are linked to a specific site dynamically per transaction via Fact tables, because a customer can order from multiple sites.)*

### D. Product-Offer Hierarchy
1. `DIM_OFFER`
2. `DIM_PRODUCT`
3. `DIM_INGREDIENT` / `DIM_ALLERGEN`
*(Note: These relationships are Many-to-Many (N:M) resolved via Bridge tables like `BRIDGE_OFFER_PRODUCT`, meaning a single product can belong to multiple offers, and an ingredient to multiple products.)*
