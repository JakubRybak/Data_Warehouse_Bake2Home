# Diagramy relacji – Bake2Home

Diagramy dla wszystkich 8 baz danych z Dockera. Strzałki pokazują klucze obce (FK).

---

## 1. catalog-db (katalog produktów)

Serce oferty – produkty, oferty, składniki, alergeny, wartości odżywcze.

```mermaid
erDiagram
    BakeryProductsTypes {
        int Id PK
        varchar Name
        text PictureFileName
        int ProductTypeDisplayOrder
        timestamp Created
        timestamp Updated
    }

    BakeryProduct {
        int Id PK
        varchar Name
        varchar Description
        int State
        text PictureFileName
        int BakeryProductsTypeId FK
        int PlatformClientId
        int Weight
        timestamp Created
        timestamp Updated
    }

    Nutrition {
        int Id PK
        bigint Calories
        float TotalFats
        float SaturatedFats
        float TotalCarbohydrates
        float Sugar
        float Protein
        float Sodium
        int ProductId FK
        timestamp Created
        timestamp Updated
    }

    Allergen {
        int Id PK
        varchar Name
        bool IsUsed
        timestamp Created
        timestamp Updated
    }

    ProductAllergen {
        int Id PK
        int AllergenId FK
        int BakeryProductId FK
        timestamp Created
        timestamp Updated
    }

    ProductAttribute {
        int Id PK
        varchar Description
        varchar Value
        int BakeryProductId FK
        timestamp Created
        timestamp Updated
    }

    PublicIngredient {
        int Id PK
        varchar Name
        varchar Unit
        timestamp Created
        timestamp Updated
    }

    PrivateIngredient {
        int Id PK
        int PlatformClientId
        varchar Name
        varchar Unit
        timestamp Created
        timestamp Updated
    }

    ProductPublicIngredient {
        int Id PK
        int BakeryProductId FK
        int IngredientId FK
        float Value
        timestamp Created
        timestamp Updated
    }

    ProductPrivateIngredient {
        int Id PK
        int BakeryProductId FK
        int IngredientId FK
        float Value
        timestamp Created
        timestamp Updated
    }

    BakeryOffer {
        int Id PK
        varchar Name
        numeric Price
        int State
        int Type
        int AvailableStock
        bool IsAvailable
        int PlatformClientId
        int VatRateId
        numeric VAT
        timestamp Created
        timestamp Updated
    }

    OfferProduct {
        int Id PK
        int ProductId FK
        int BakeryOfferId FK
        numeric ProductPrice
        text ProductName
        int ProductCount
        bool IsAvailableInOffer
        numeric ProductInOfferPrice
        numeric VATForProductInOffer
        timestamp Created
        timestamp Updated
    }

    Availability {
        int Id PK
        bool Monday
        bool Tuesday
        bool Wednesday
        bool Thursday
        bool Friday
        bool Saturday
        bool Sunday
        timestamp AvailableDateFrom
        timestamp AvailableDateTo
        timestamp Created
        timestamp Updated
    }

    OfferAvailability {
        int Id PK
        int BakeryOfferId FK
    }

    OfferLocation {
        int Id PK
        int LocationId
        int BakeryOfferId FK
        timestamp Created
        timestamp Updated
    }

    OfferSite {
        int Id PK
        int SiteId
        int BakeryOfferId FK
        timestamp Created
        timestamp Updated
    }

    BakeryProductSiteNew {
        int Id PK
        int BakeryProductId FK
        int SiteId
        timestamp Created
        timestamp Updated
    }

    BakeryProductsTypes ||--o{ BakeryProduct : "typ produktu"
    BakeryProduct ||--|| Nutrition : "wartosci odzywcze"
    BakeryProduct ||--o{ ProductAllergen : "alergeny"
    Allergen ||--o{ ProductAllergen : "alergeny"
    BakeryProduct ||--o{ ProductAttribute : "atrybuty"
    BakeryProduct ||--o{ ProductPublicIngredient : "skladniki publiczne"
    PublicIngredient ||--o{ ProductPublicIngredient : "skladniki publiczne"
    BakeryProduct ||--o{ ProductPrivateIngredient : "skladniki prywatne"
    PrivateIngredient ||--o{ ProductPrivateIngredient : "skladniki prywatne"
    BakeryProduct ||--o{ OfferProduct : "produkty w ofercie"
    BakeryOffer ||--o{ OfferProduct : "produkty w ofercie"
    BakeryOffer ||--o{ OfferAvailability : "dostepnosc"
    Availability ||--|| OfferAvailability : "dostepnosc"
    BakeryOffer ||--o{ OfferLocation : "lokalizacje oferty"
    BakeryOffer ||--o{ OfferSite : "piekarnie oferty"
    BakeryProduct ||--o{ BakeryProductSiteNew : "produkty w piekarniach"
```

---

## 2. client-manager-db (piekarnie, oddziały, obszary)

Struktura organizacyjna – firmy piekarnicze, ich budynki, strefy dostawcze.

```mermaid
erDiagram
    Client {
        int Id PK
        text Name
        text Description
        bigint NIP
        char BankAccount
        text Street
        text City
        text Country
        varchar ZipCode
        text Email
        text FullFormalName
        text Phone
        timestamp Created
        timestamp Updated
    }

    Site {
        int Id PK
        varchar Name
        varchar Street
        varchar Nr
        varchar City
        text State
        varchar Country
        varchar ZipCode
        int ClientId FK
        int SiteCoordinatesId FK
        timestamp Created
        timestamp Updated
    }

    SiteCoordinates {
        int Id PK
        float Latitude
        float Longitude
        timestamp Created
        timestamp Updated
    }

    Person {
        int Id PK
        int ClientId FK
        text Name
        text Interview
        text PictureLink
        timestamp Created
        timestamp Updated
    }

    Location {
        int Id PK
        varchar Name
        varchar Description
        int Status
        timestamp Created
        timestamp Updated
    }

    LocationSite {
        int Id PK
        int SiteId FK
        int LocationId FK
        timestamp Created
        timestamp Updated
    }

    PolygonVertex {
        int Id PK
        int LocationId FK
        float Latitude
        float Longitude
        timestamp Created
        timestamp Updated
    }

    Leave {
        int Id PK
        int SiteId FK
        timestamp DateFrom
        timestamp DateTo
        int Type
        text Description
        int State
        timestamp Created
        timestamp Updated
    }

    IndicatedBakery {
        int Id PK
        varchar BakeryName
        text BakeryAddress
        text MapInfo
    }

    Client ||--o{ Site : "oddzialy"
    Client ||--o{ Person : "pracownicy"
    SiteCoordinates ||--o| Site : "wspolrzedne"
    Site ||--o{ Leave : "urlopy"
    Site ||--o{ LocationSite : "obsluguje obszary"
    Location ||--o{ LocationSite : "obslugiwana przez"
    Location ||--o{ PolygonVertex : "wierzcholki granicy"
```

---

## 3. customer-manager-db (klienci końcowi)

Ludzie, którzy zamawiają pieczywo.

```mermaid
erDiagram
    Customer {
        int Id PK
        varchar Name
        varchar PhoneNumber
        varchar Avatar
        text Email
        text UserId
        int OtherRoleStatus
        int CustomerState
        text CustomerIp
        timestamp Created
        timestamp Updated
    }

    CustomerAddress {
        int Id PK
        varchar AddressName
        varchar Address
        float Longitude
        float Latitude
        varchar EntryInformationAndCodes
        text AdditionalInformation
        int CustomerId FK
        int State
        timestamp Created
        timestamp Updated
    }

    CustomerAndroidToken {
        int Id PK
        int CustomerId FK
        text Token
        int TokenState
        text InstallationId
        text Platform
        timestamp ExpirationTime
        timestamp Created
        timestamp Updated
    }

    Consents {
        int Id PK
        int Type
        varchar LinkToDocument
        int Status
        text Version
        timestamp ExpiryDate
        timestamp GoLiveDate
        int ObligationType
        timestamp Created
        timestamp Updated
    }

    CustomerConsent {
        int Id PK
        int CustomerId FK
        int ConsentId FK
        int Status
        timestamp Date
        timestamp Created
        timestamp Updated
    }

    Customer ||--o{ CustomerAddress : "adresy dostawy"
    Customer ||--o{ CustomerAndroidToken : "tokeny push"
    Customer ||--o{ CustomerConsent : "zgody"
    Consents ||--o{ CustomerConsent : "typy zgod"
```

---

## 4. planner-db (zamówienia)

Serce transakcji – zamówienia klientów, pozycje zamówień, subskrypcje.

```mermaid
erDiagram
    BakeryOrders {
        int Id PK
        int CustomerAddressId
        int DailySettlementItemId
        int PlatformDiscountId FK
        timestamp Date
        int OrderState
        int ServicingBySiteId
        int LocationId
        timestamp Created
        timestamp Updated
    }

    BakeryOrderItems {
        int Id PK
        int Quantity
        int OrderId FK
        int BoughtOfferInstanceId FK
        int OrderItemState
        bool ModifiedByHand
        int PlannerItemId FK
        timestamp Created
        timestamp Updated
    }

    BoughtOfferInstances {
        int Id PK
        numeric Price
        int OfferId
        text AdditionalInfo
        text OfferName
        text PictureFileName
        numeric VAT
        int VatRateId
        int Type
        timestamp Created
        timestamp Updated
    }

    PlannerItems {
        int Id PK
        int PlannerItemState
        int Quantity
        int CustomerAddressId
        int DayIndex
        int NextVersion
        int PreviousVersion
        timestamp StartDate
        timestamp EndDate
        int BoughtOfferInstanceId FK
        int ServicingBySiteId
        int LocationId
        timestamp Created
        timestamp Updated
    }

    PlatformDiscount {
        int Id PK
        int BoughtOfferInstanceId FK
        timestamp DateFrom
        timestamp DateTo
        int NumbersOfOrders
        int Discount
        text AdditionalInformation
        timestamp Created
        timestamp Updated
    }

    BakeryOrders ||--o{ BakeryOrderItems : "pozycje zamowienia"
    BoughtOfferInstances ||--o{ BakeryOrderItems : "kupiona oferta"
    PlannerItems ||--o{ BakeryOrderItems : "plan subskrypcji"
    BoughtOfferInstances ||--o{ PlannerItems : "oferta w planie"
    BakeryOrders }o--o| PlatformDiscount : "znizka"
    BoughtOfferInstances ||--o{ PlatformDiscount : "znizka na oferte"
```

---

## 5. delivery-manager-db (dostawy)

Realizacja zamówień – kto, co, komu i kiedy dostarczył.

```mermaid
erDiagram
    AreaOfDeliveryForDate {
        int Id PK
        timestamp Date
        text Name
        int EstimatedNoOfDelivery
        int LocationId
        int SiteId
        timestamp Created
        timestamp Updated
    }

    Deliveries {
        int Id PK
        int CustomerAddressId
        int AreaOfDeliveryForDateId FK
        varchar AddressName
        varchar Address
        float Longitude
        float Latitude
        int State
        int DeliveryManId
        int SiteId
        text CustomerUserId
        text DeliveryManUserId
        int OrderId
        timestamp Created
        timestamp Updated
    }

    DeliveryItems {
        int Id PK
        int State
        int PlannedQuantity
        int PackedQuantity
        varchar ProductName
        numeric ProductPrice
        int ProductId
        int DeliveryId FK
        timestamp Created
        timestamp Updated
    }

    DeliveryManArea {
        int Id PK
        int DeliveryManId
        int AreaOfDeliveryForDateId FK
        int State
        timestamp Created
        timestamp Updated
    }

    AreaOfDeliveryForDate ||--o{ Deliveries : "dostawy w obszarze"
    Deliveries ||--o{ DeliveryItems : "pozycje dostawy"
    AreaOfDeliveryForDate ||--o{ DeliveryManArea : "dostawcy w obszarze"
```

---

## 6. delivery-account-manager-db (konta dostawców)

Dane osobowe i organizacyjne dostawców.

```mermaid
erDiagram
    DeliveryMan {
        int Id PK
        varchar Name
        text PhoneNumber
        text Email
        timestamp DateOfBirth
        text NumberOfIDCard
        text Pesel
        text NIP
        int SiteId
        int ContractOwner
        timestamp Created
        timestamp Updated
    }

    Address {
        int Id PK
        text AddressName
        text Voivodeship
        text City
        text District
        text StreetName
        text HouseNumber
        text ZipCode
        int DeliveryManId FK
        timestamp Created
        timestamp Updated
    }

    BankAccount {
        int Id PK
        text BankName
        text BankAccountNumber
        int DeliveryManId FK
        timestamp Created
        timestamp Updated
    }

    DeliveryManAndroidToken {
        int Id PK
        int DeliveryManId FK
        text Token
        int TokenState
        text InstallationId
        text Platform
        timestamp Created
        timestamp Updated
    }

    DeliveryManLocationAllocation {
        int Id PK
        int LocationId
        timestamp Date
        int DeliveryManId FK
        int SiteId
        timestamp Created
        timestamp Updated
    }

    DeliveryManUnavailability {
        int Id PK
        int DeliveryManId FK
        timestamp DateFrom
        timestamp DateTo
        int State
        timestamp Created
        timestamp Updated
    }

    DeliveryMan ||--o{ Address : "adresy"
    DeliveryMan ||--o{ BankAccount : "konta bankowe"
    DeliveryMan ||--o{ DeliveryManAndroidToken : "tokeny push"
    DeliveryMan ||--o{ DeliveryManLocationAllocation : "przypisania do obszarow"
    DeliveryMan ||--o{ DeliveryManUnavailability : "niedostepnosci"
```

---

## 7. claim-manager-db (reklamacje)

Obsługa problemów z dostawami.

```mermaid
erDiagram
    ClaimsEntity {
        int Id PK
        int OrderId
        int DeliveryId
        text Description
        timestamp Date
        int State
        int Type
        int AgreedDiscountId
        int AgreedReturnAmount
        int ServicingBySiteId
        timestamp Created
        timestamp Updated
    }

    ClaimEntityDeliveryItems {
        int Id PK
        int IssueType
        int DeliveryItemId
        int ClaimId FK
        text ProductName
        int OrderedQuantity
        int DeliveredQuantity
        int NumberOfProductsWithAcceptedClaim
        int ProductId
        int ClaimedQuantity
        timestamp Created
        timestamp Updated
    }

    ClaimItems {
        int Id PK
        int ClaimEntityId FK
        text Description
        text Notifier
        text PictureName
        int Type
        timestamp Created
        timestamp Updated
    }

    ClaimsEntity ||--o{ ClaimEntityDeliveryItems : "reklamowane produkty"
    ClaimsEntity ||--o{ ClaimItems : "szczegoly reklamacji"
```

---

## 8. wallet-db (płatności, zniżki, zwroty)

Cały przepływ pieniędzy.

```mermaid
erDiagram
    PaymentMethods {
        int Id PK
        int Type
        text Currency
        int Status
        text EncryptedToken
        text CardMask
        text CardBrand
        bool Mobile
        int CustomerId
        timestamp Created
        timestamp Updated
    }

    Discounts {
        int Id PK
        money DiscountPercentage
        money DiscountFlatRate
        varchar DiscountCode
        timestamp ActiveFrom
        timestamp ActiveTo
        int UseLimitGlobally
        int UseLimitPerCustomer
        money MinimalTransactionAmount
        int ClientId
        bool OnlyForFirstPurchase
        int CustomerId
        timestamp Created
        timestamp Updated
    }

    Payments {
        int Id PK
        int Status
        money Amount
        int OrderId
        int DeliveryId
        int PaymentMethodId FK
        text ListOfOrderItems
        bool ForManualHandling
        int PaymentType
        text PaidByTransactionId
        text Error
        int DiscountId FK
        money DiscountedAmount
        int ClientId
        timestamp Created
        timestamp Updated
    }

    DiscountUses {
        int Id PK
        timestamp UseDate
        int CustomerId
        int DiscountId FK
        text ListOfPaymentIds
        timestamp Created
        timestamp Updated
    }

    Refunds {
        int Id PK
        int Status
        int Type
        money Amount
        text Description
        int ClaimId
        int PaymentId FK
        money BaseAmount
        timestamp Created
        timestamp Updated
    }

    RefundItems {
        int Id PK
        int RefundId FK
        int MissingProductQuantity
        money Amount
        money VatAmount
        int ProductId
        timestamp Created
        timestamp Updated
    }

    RefundCreationErrors {
        int Id PK
        text StatusCode
        text CodeLiteral
        int Code
        text Description
        int RefundId FK
        timestamp Created
        timestamp Updated
    }

    RefundFinalizationError {
        int Id PK
        text PayURefundId
        text ExtRefundId
        int RefundId FK
        numeric Amount
        timestamp RefundRegistrationDate
        text Status
        text ErrorCode
        timestamp Created
        timestamp Updated
    }

    PaymentMethods ||--o{ Payments : "platnosci metoda"
    Discounts ||--o{ Payments : "znizka na platnosc"
    Discounts ||--o{ DiscountUses : "uzycia znizki"
    Payments ||--o{ Refunds : "zwroty z platnosci"
    Refunds ||--o{ RefundItems : "pozycje zwrotu"
    Refunds ||--o{ RefundCreationErrors : "bledy tworzenia"
    Refunds ||--o{ RefundFinalizationError : "bledy finalizacji"
```
