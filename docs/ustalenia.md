## DISCOUNT w FACT_ORDER_ITEM
- danie ID_PLATFORM_DISCOUNT tylko dla tych co mają zniżkę, trzeba zrobic podczas ETL i DISCOUNT_PERCENT
- i ogolnie nwm czy spoko ze duzo informacji pominalem z platform_discount
## ID_CUSTOMER w FACT_ORDER_ITEM
- trzeba wyciagnac z tabeli z ID_CUSTOMER_ADRESS
## CONSENST w CUSTOMER_MANAGER
- moze osobna tabela faktow?
## FACT_DELIVERY_ITEM
- CUSTOMER_ID z CustomerAddressID
## DIM_LOCATION
- VERTEXES jako lista wierzchołków
## FACT_CLAIM
- ID_CUSTOMER WYCIAGNAC Z ID_ORDER
## FACT_PAYMENT
- dorzucic ID_SITE
- error YES/NO
## DIM_SITE/DIM_CLIENT
- może to rozbić, albo jakis outrigger
## DIM_PRODUCT
- dorzucic nutrition i allergens?