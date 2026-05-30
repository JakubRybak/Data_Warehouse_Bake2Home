-- ================================================================================
-- Automatically generated DDL script for Bronze tables in BigQuery
-- GCP Project: bake2home-data-warehouse
-- GCS Bucket: bake2home-raw-data
-- ================================================================================


-- --------------------------------------------------------------------------------
-- DATABASE: catalog-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_Allergen`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/Allergen.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_Availability`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/Availability.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_BakeryOffer`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/BakeryOffer.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_BakeryProduct`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/BakeryProduct.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_BakeryProductSiteNew`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/BakeryProductSiteNew.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_BakeryProductsTypes`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/BakeryProductsTypes.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_Nutrition`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/Nutrition.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_OfferAvailability`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/OfferAvailability.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_OfferLocation`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/OfferLocation.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_OfferProduct`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/OfferProduct.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_OfferSite`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/OfferSite.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_PrivateIngredient`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/PrivateIngredient.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_ProductAllergen`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/ProductAllergen.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_ProductAttribute`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/ProductAttribute.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_ProductPrivateIngredient`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/ProductPrivateIngredient.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_ProductPublicIngredient`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/ProductPublicIngredient.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_catalog_PublicIngredient`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/catalog-db/PublicIngredient.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: claim-manager-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_claim_manager_ClaimEntityDeliveryItems`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/claim-manager-db/ClaimEntityDeliveryItems.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_claim_manager_ClaimItems`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/claim-manager-db/ClaimItems.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_claim_manager_ClaimsEntity`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/claim-manager-db/ClaimsEntity.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: client-manager-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_Client`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/Client.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_IndicatedBakery`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/IndicatedBakery.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_Leave`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/Leave.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_Location`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/Location.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_LocationSite`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/LocationSite.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_Person`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/Person.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_PolygonVertex`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/PolygonVertex.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_Site`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/Site.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_client_manager_SiteCoordinates`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/client-manager-db/SiteCoordinates.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: customer-manager-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_customer_manager_Consents`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/customer-manager-db/Consents.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_customer_manager_Customer`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/customer-manager-db/Customer.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_customer_manager_CustomerAddress`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/customer-manager-db/CustomerAddress.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_customer_manager_CustomerConsent`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/customer-manager-db/CustomerConsent.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: delivery-account-manager-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_account_manager_Address`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-account-manager-db/Address.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_account_manager_BankAccount`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-account-manager-db/BankAccount.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_account_manager_DeliveryMan`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-account-manager-db/DeliveryMan.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_account_manager_DeliveryManLocationAllocation`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-account-manager-db/DeliveryManLocationAllocation.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_account_manager_DeliveryManUnavailability`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-account-manager-db/DeliveryManUnavailability.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: delivery-manager-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_manager_AreaOfDeliveryForDate`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-manager-db/AreaOfDeliveryForDate.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_manager_Deliveries`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-manager-db/Deliveries.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_manager_DeliveryItems`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-manager-db/DeliveryItems.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_delivery_manager_DeliveryManArea`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/delivery-manager-db/DeliveryManArea.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: planner-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_planner_BakeryOrderItems`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/planner-db/BakeryOrderItems.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_planner_BakeryOrders`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/planner-db/BakeryOrders.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_planner_BoughtOfferInstances`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/planner-db/BoughtOfferInstances.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_planner_PlannerItems`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/planner-db/PlannerItems.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_planner_PlatformDiscount`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/planner-db/PlatformDiscount.parquet']
);

-- --------------------------------------------------------------------------------
-- DATABASE: wallet-db

-- --------------------------------------------------------------------------------

CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_DiscountUses`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/DiscountUses.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_Discounts`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/Discounts.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_PaymentMethods`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/PaymentMethods.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_Payments`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/Payments.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_RefundCreationErrors`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/RefundCreationErrors.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_RefundFinalizationError`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/RefundFinalizationError.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_RefundItems`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/RefundItems.parquet']
);
CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.raw_wallet_Refunds`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bake2home-raw-data/data/wallet-db/Refunds.parquet']
);