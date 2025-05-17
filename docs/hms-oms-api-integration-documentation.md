# HMS-OMS and HMS-API Order Module Integration Documentation

## Overview

This document provides detailed information about the integration between the HMS-OMS (Order Management System) and HMS-API Order Module. The integration enables bidirectional synchronization of orders between both systems, allowing orders placed through the HMS-API to be processed and fulfilled by HMS-OMS.

## Integration Components

### HMS-API Components

1. **OMSIntegrationService**
   - Located at: `/SYSTEM-COMPONENTS/HMS-API/Modules/Order/Services/OMSIntegrationService.php`
   - Handles communication with HMS-OMS for order operations
   - Methods:
     - `sendOrderToOMS()`: Sends a new order to HMS-OMS
     - `syncOrderStatus()`: Updates order status in HMS-OMS
     - `fetchOrderFromOMS()`: Retrieves order details from HMS-OMS

2. **OMSWebhookController**
   - Located at: `/SYSTEM-COMPONENTS/HMS-API/Modules/Order/Http/Controllers/OMSWebhookController.php`
   - Processes webhooks from HMS-OMS
   - Endpoints:
     - `statusUpdate()`: Handles order status updates from HMS-OMS

### HMS-OMS Components

1. **HmsApiIntegrationService**
   - Located at: `/SYSTEM-COMPONENTS/HMS-OMS/app/services/integration/hms_api_integration_service.rb`
   - Handles communication with HMS-API
   - Methods:
     - `sync_order_status()`: Updates order status in HMS-API
     - `notify_order_fulfilled()`: Notifies HMS-API when an order is fulfilled
     - `fetch_order_from_api()`: Retrieves order details from HMS-API
     - `send_webhook()`: Sends webhook events to HMS-API

2. **WebhooksController**
   - Located at: `/SYSTEM-COMPONENTS/HMS-OMS/app/controllers/api/v1/webhooks_controller.rb`
   - Processes webhooks from HMS-API
   - Endpoints:
     - `order_created()`: Handles new orders from HMS-API
     - `order_updated()`: Handles order updates from HMS-API

3. **OrderSyncService**
   - Located at: `/SYSTEM-COMPONENTS/HMS-OMS/app/services/integration/order_sync_service.rb`
   - Manages order synchronization between systems
   - Methods:
     - `sync_order()`: Syncs a specific order with HMS-API
     - `sync_all_orders()`: Syncs all orders with HMS-API
     - `import_order_from_api()`: Imports an order from HMS-API

## Data Mapping

### HMS-API Order to HMS-OMS Order

| HMS-API Field | HMS-OMS Field | Notes |
|---------------|---------------|-------|
| id | ext_code | HMS-API ID stored as external code in HMS-OMS |
| title | data['title'] | Stored in the JSON data field |
| items | data['items'] | Array of order items stored in JSON data |
| status | state | Mapped using status mapping functions |
| user_id | user_id | User mapping required between systems |

### Status Mapping

| HMS-API Status | HMS-OMS State |
|----------------|---------------|
| pending | to_execute |
| processing | in_progress |
| completed | done |

## Configuration

### HMS-API Configuration

The HMS-API Order Module requires the following configuration in `/SYSTEM-COMPONENTS/HMS-API/Modules/Order/Config/config.php`:

```php
// HMS-OMS Integration Settings
'oms_api_url' => env('OMS_API_URL', 'http://oms-service:3000'),
'oms_api_key' => env('OMS_API_KEY', ''),
'oms_order_type_code' => env('OMS_ORDER_TYPE_CODE', 'api_order'),
'oms_webhook_secret' => env('OMS_WEBHOOK_SECRET', ''),
```

Environment variables:
- `OMS_API_URL`: Base URL of the HMS-OMS API
- `OMS_API_KEY`: Authentication token for HMS-OMS
- `OMS_ORDER_TYPE_CODE`: Default order type code for API orders
- `OMS_WEBHOOK_SECRET`: Secret key for webhook signature validation

### HMS-OMS Configuration

HMS-OMS requires the following configuration in `/SYSTEM-COMPONENTS/HMS-OMS/config/initializers/hms_api_integration.rb`:

```ruby
Rails.application.config.hms_api_integration = {
  api_base_url: ENV['HMS_API_URL'] || 'http://api-service:8000',
  api_token: ENV['HMS_API_TOKEN'],
  webhook_secret: ENV['HMS_API_WEBHOOK_SECRET']
}
```

Environment variables:
- `HMS_API_URL`: Base URL of the HMS-API
- `HMS_API_TOKEN`: Authentication token for HMS-API
- `HMS_API_WEBHOOK_SECRET`: Secret key for webhook signature validation

## Integration Workflows

### Order Creation Flow

1. Customer places an order through HMS-API
2. HMS-API `OrderController.store()` creates the order
3. HMS-API `OMSIntegrationService.sendOrderToOMS()` sends the order to HMS-OMS
4. HMS-OMS creates a corresponding order with the HMS-API order ID as `ext_code`
5. HMS-OMS returns the new order code to HMS-API
6. HMS-API updates the order with the HMS-OMS order code

### Order Status Update Flow (HMS-OMS to HMS-API)

1. Order status changes in HMS-OMS
2. HMS-OMS `after_update` callback triggers `notify_hms_api_of_status_change`
3. HMS-OMS `HmsApiIntegrationService.send_webhook()` sends a webhook to HMS-API
4. HMS-API `OMSWebhookController.statusUpdate()` processes the webhook
5. HMS-API updates the order status

### Order Status Update Flow (HMS-API to HMS-OMS)

1. Order status changes in HMS-API
2. HMS-API `OrderController.update()` calls `OMSIntegrationService.syncOrderStatus()`
3. HMS-OMS receives the status update and updates the order

### Order Fulfillment Flow

1. Order is marked as 'done' in HMS-OMS
2. HMS-OMS `after_update` callback triggers `notify_hms_api_of_status_change`
3. HMS-OMS `HmsApiIntegrationService.send_webhook()` sends an 'order.fulfilled' webhook
4. HMS-API `OMSWebhookController.handleOrderFulfilled()` processes the webhook
5. HMS-API marks the order as 'completed'

## Security

The integration uses the following security measures:

1. **API Authentication**
   - HMS-API uses Bearer token authentication
   - HMS-OMS uses Token authentication
   - Tokens are stored as environment variables

2. **Webhook Signature Validation**
   - All webhooks include an HMAC-SHA256 signature of the payload
   - The signature is calculated using a shared secret
   - Both systems validate the signature before processing webhooks

## Testing

Use the provided test script to verify the integration:

```bash
$ ./test-hms-oms-api-integration.sh
```

The script tests the following flows:
1. Creating an order in HMS-API
2. Verifying the order was synced to HMS-OMS
3. Updating the order status in HMS-OMS
4. Verifying the status update in HMS-API
5. Marking the order as complete in HMS-OMS
6. Verifying order completion in HMS-API

## Maintenance Tasks

### HMS-OMS Rake Tasks

The following rake tasks are available for maintaining the integration:

```bash
# Sync all orders with HMS-API
$ rake hms_api:sync_orders

# Import a specific order from HMS-API
$ rake hms_api:import_order[12345]
```

## Troubleshooting

### Common Issues

1. **Webhook Signature Failures**
   - Ensure the webhook secret is correctly configured in both systems
   - Check that the payload is not being modified during transmission

2. **Order Not Syncing**
   - Verify network connectivity between systems
   - Check API credentials are correct
   - Review application logs for error messages

3. **Status Updates Not Propagating**
   - Ensure the order has the correct external ID/code
   - Check webhook signature validation
   - Review the status mapping implementations

### Logging

Both systems log integration events:

- HMS-API: Uses Laravel's logging system with dedicated messages for integration events
- HMS-OMS: Uses Rails logger with prefixed messages for integration events

Review these logs for detailed information on integration issues.