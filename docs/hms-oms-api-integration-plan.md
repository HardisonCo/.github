# HMS-OMS and HMS-API Order Module Integration Plan

## Overview

This document outlines the plan for integrating the HMS-OMS (Order Management System) with the HMS-API Order module. The integration will allow orders placed through the HMS-API to be processed, tracked, and fulfilled by the HMS-OMS.

## System Analysis

### HMS-OMS
- **Technology Stack**: Ruby on Rails, PostgreSQL
- **Key Models**: Order, OrderType, User
- **API Endpoints**: RESTful API under `/api/v1/orders`
- **Authentication**: HTTP Authentication, API tokens

### HMS-API Order Module
- **Technology Stack**: PHP/Laravel, MySQL
- **Key Models**: Order, OrderItem, AttachedOrder, AttachedOrderItem
- **API Endpoints**: RESTful API under `/api/order`
- **Authentication**: JWT, role-based access

## Integration Strategy

We will implement a bidirectional integration that syncs orders between both systems while respecting their different data models and workflows.

### Integration Points

1. **Order Creation**: Orders created in HMS-API should be replicated in HMS-OMS
2. **Order Updates**: Status updates in either system should be synced
3. **Order Fulfillment**: Order fulfillment processes in HMS-OMS should update HMS-API
4. **User Association**: Ensure user associations are maintained across systems

### Data Mapping

| HMS-API Order Field | HMS-OMS Order Field | Notes |
|---------------------|---------------------|-------|
| id                  | ext_code            | HMS-API order ID stored as external code in HMS-OMS |
| title               | data['title']       | Stored in the JSON data field in HMS-OMS |
| user_id             | user_id             | User mapping required |
| items               | data['items']       | Order items serialized as JSON in HMS-OMS |
| created_at          | created_at          | Direct mapping |
| updated_at          | updated_at          | Direct mapping |

### Implementation Phases

#### Phase 1: Create Integration Service Layer
1. Create an adapter class in HMS-API to communicate with HMS-OMS
2. Create an adapter class in HMS-OMS to communicate with HMS-API
3. Implement authentication between systems

#### Phase 2: Implement Order Synchronization
1. Implement webhook handlers in HMS-OMS for HMS-API events
2. Implement order creation sync from HMS-API to HMS-OMS
3. Implement order status sync from HMS-OMS to HMS-API

#### Phase 3: Implement Order Fulfillment Flow
1. Extend HMS-OMS to handle HMS-API order types
2. Implement order fulfillment process sync from HMS-OMS to HMS-API
3. Create order completion notification from HMS-OMS to HMS-API

#### Phase 4: Testing and Documentation
1. Create integration tests for all sync processes
2. Update system documentation
3. Create operational guides for the integrated system

## Technical Implementation Details

### 1. HMS-API Integration Adapter

Create a new service in HMS-API to handle communication with HMS-OMS:

```php
// HMS-API/Modules/Order/Services/OMSIntegrationService.php
namespace Modules\Order\Services;

class OMSIntegrationService
{
    public function sendOrderToOMS(Order $order): bool
    {
        // Convert order to OMS format
        // Send API request to OMS
        // Return success/failure
    }
    
    public function syncOrderStatus(Order $order, string $status): bool
    {
        // Send status update to OMS
        // Return success/failure
    }
    
    public function fetchOrderFromOMS(string $omsOrderCode): array
    {
        // Fetch order details from OMS
        // Return formatted data
    }
}
```

### 2. HMS-OMS Integration Adapter

Create a new service in HMS-OMS to handle communication with HMS-API:

```ruby
# app/services/hms_api_integration_service.rb
class HmsApiIntegrationService
  def send_order_to_api(order)
    # Convert order to API format
    # Send API request to HMS-API
    # Return success/failure
  end
  
  def sync_order_status(order, status)
    # Send status update to HMS-API
    # Return success/failure
  end
  
  def fetch_order_from_api(api_order_id)
    # Fetch order details from HMS-API
    # Return formatted data
  end
end
```

### 3. Webhook Implementation

Implement webhooks to handle real-time updates between systems:

```ruby
# HMS-OMS/app/controllers/api/v1/webhooks_controller.rb
module API
  module V1
    class WebhooksController < API::BaseController
      def order_created
        # Process order creation webhook from HMS-API
        # Create new order in HMS-OMS
      end
      
      def order_updated
        # Process order update webhook from HMS-API
        # Update order in HMS-OMS
      end
    end
  end
end
```

```php
// HMS-API/Modules/Order/Http/Controllers/WebhooksController.php
namespace Modules\Order\Http\Controllers;

class WebhooksController extends Controller
{
    public function orderStatusUpdated(Request $request)
    {
        // Process order status update from HMS-OMS
        // Update order in HMS-API
    }
    
    public function orderFulfilled(Request $request)
    {
        // Process order fulfillment from HMS-OMS
        // Update order in HMS-API
    }
}
```

## Security Considerations

1. Implement secure API key exchange between systems
2. Ensure all API communications use HTTPS
3. Implement request signing for webhook verification
4. Create audit logs for all cross-system operations

## Deployment Strategy

1. Deploy integration adapters to staging environments
2. Test integration with sample orders
3. Monitor system performance and error rates
4. Gradually roll out to production with increasing order volume

## Rollback Plan

1. Implement feature flags to disable integration
2. Create data recovery scripts to handle sync failures
3. Document manual order handling procedures for fallback

## Timeline

- Phase 1: 1 week
- Phase 2: 2 weeks
- Phase 3: 1 week
- Phase 4: 1 week
- Testing and refinement: 1 week

## Success Criteria

1. Orders created in HMS-API are successfully processed in HMS-OMS
2. Order status updates are reflected in both systems within 5 minutes
3. No data loss or duplicate orders across systems
4. System performance remains within acceptable parameters
5. Seamless user experience across both systems