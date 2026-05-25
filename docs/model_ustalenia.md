# Co trzeba pamiętać
### ID_CUSTOMER w FACT_ORDER_ITEM
- trzeba wyciagnac z tabeli z ID_CUSTOMER_ADRESS

### FACT_DELIVERY_ITEM
- CUSTOMER_ID z CustomerAddressID
### DIM_LOCATION
- VERTEXES jako lista wierzchołków
### FACT_CLAIM
- ID_CUSTOMER WYCIAGNAC Z ID_ORDER
### FACT_PAYMENT
- dorzucic ID_SITE
- error YES/NO
### DIM_COMPETITORS
- usunąć z listy piekarni własne site


# Co trzeba przemyśleć

# Co trzeba sprawdzić
- sprawdzic wszedzie `STATE` co znaczy i może usunąć
- ID_AGREED_DISCOUNT w FACT_CLAIM_ITEM
- czy da sie wyłuskać date dołączenia customera/clienta
- MOBILE w DIM_PAYMENT_METHOD