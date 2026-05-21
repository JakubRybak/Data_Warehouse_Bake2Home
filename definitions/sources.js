// List of all analytical tables in the Bronze layer (excluding technical tables and push tokens)
const tables = [
  // catalog-db (Product Catalog)
  "raw_catalog_Allergen",
  "raw_catalog_Availability",
  "raw_catalog_BakeryOffer",
  "raw_catalog_BakeryProduct",
  "raw_catalog_BakeryProductSiteNew",
  "raw_catalog_BakeryProductsTypes",
  "raw_catalog_Nutrition",
  "raw_catalog_OfferAvailability",
  "raw_catalog_OfferLocation",
  "raw_catalog_OfferProduct",
  "raw_catalog_OfferSite",
  "raw_catalog_PrivateIngredient",
  "raw_catalog_ProductAllergen",
  "raw_catalog_ProductAttribute",
  "raw_catalog_ProductPrivateIngredient",
  "raw_catalog_ProductPublicIngredient",
  "raw_catalog_PublicIngredient",
  
  // claim-manager-db (Claims Management)
  "raw_claim_manager_ClaimEntityDeliveryItems",
  "raw_claim_manager_ClaimItems",
  "raw_claim_manager_ClaimsEntity",
  
  // client-manager-db (Bakeries and partner sites)
  "raw_client_manager_Client",
  "raw_client_manager_IndicatedBakery",
  "raw_client_manager_Leave",
  "raw_client_manager_Location",
  "raw_client_manager_LocationSite",
  "raw_client_manager_Person",
  "raw_client_manager_PolygonVertex",
  "raw_client_manager_Site",
  "raw_client_manager_SiteCoordinates",
  
  // customer-manager-db (Customers and consents)
  "raw_customer_manager_Consents",
  "raw_customer_manager_Customer",
  "raw_customer_manager_CustomerAddress",
  "raw_customer_manager_CustomerConsent",
  
  // delivery-account-manager-db (Delivery courier accounts)
  "raw_delivery_account_manager_Address",
  "raw_delivery_account_manager_BankAccount",
  "raw_delivery_account_manager_DeliveryMan",
  "raw_delivery_account_manager_DeliveryManLocationAllocation",
  "raw_delivery_account_manager_DeliveryManUnavailability",
  
  // delivery-manager-db (Delivery execution & fulfillment)
  "raw_delivery_manager_AreaOfDeliveryForDate",
  "raw_delivery_manager_Deliveries",
  "raw_delivery_manager_DeliveryItems",
  "raw_delivery_manager_DeliveryManArea",
  
  // planner-db (Baking planning and orders)
  "raw_planner_BakeryOrderItems",
  "raw_planner_BakeryOrders",
  "raw_planner_BoughtOfferInstances",
  "raw_planner_PlannerItems",
  "raw_planner_PlatformDiscount",
  
  // wallet-db (Payments and wallet transactions)
  "raw_wallet_DiscountUses",
  "raw_wallet_Discounts",
  "raw_wallet_PaymentMethods",
  "raw_wallet_Payments",
  "raw_wallet_RefundCreationErrors",
  "raw_wallet_RefundFinalizationError",
  "raw_wallet_RefundItems",
  "raw_wallet_Refunds"
];

// Loop to declare each source table in Dataform
tables.forEach(table => {
  declare({
    database: "bake2home-data-warehouse", // GCP Project ID
    schema: "bronze",                     // BigQuery Dataset
    name: table                           // BigQuery Table Name
  });
});