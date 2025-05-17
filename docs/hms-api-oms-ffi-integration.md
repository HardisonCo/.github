# HMS-API Order Module and HMS-OMS Integration using FFI

This document provides comprehensive documentation for the integration between the HMS-API Order Module and HMS-OMS using the HMS Foreign Function Interface (FFI) system.

## Overview

The integration enables seamless communication between the HMS-API Order Module (PHP) and HMS-OMS (Ruby) systems, allowing orders placed through the API to be processed by the OMS while maintaining performance, type safety, and cross-language compatibility.

## Architecture

The integration uses the HMS-FFI system to handle cross-language communication using Protocol Buffers as the serialization format. This approach provides type safety, efficient serialization, and language-agnostic interfaces.

### Key Components

1. **Protocol Buffer Definitions**: Define the data structures and service interfaces
2. **FFI Service Implementation**: Implement the service using the FFI bindings
3. **Serialization Layer**: Convert between language-specific types and FFI types
4. **Controller Integration**: Update controllers to use FFI services

## Integration Flow

```
┌─────────────────┐         ┌───────────────────┐         ┌────────────────┐
│                 │         │                   │         │                │
│   HMS-API       │ ◀────▶  │   HMS-FFI Layer   │ ◀────▶  │   HMS-OMS      │
│   (PHP)         │         │   (Protocol Buf)  │         │   (Ruby)       │
│                 │         │                   │         │                │
└─────────────────┘         └───────────────────┘         └────────────────┘
```

### Order Creation Flow

1. User creates an order through HMS-API
2. HMS-API converts the order to Protocol Buffer format
3. HMS-API calls the OMS service through FFI
4. HMS-OMS processes the order and returns success/failure
5. HMS-API updates the order with OMS reference code

### Order Status Update Flow

1. HMS-OMS updates order status
2. HMS-OMS sends a webhook to HMS-API
3. HMS-API validates the webhook signature
4. HMS-API processes the status update
5. HMS-API updates the order status in the database

## Protocol Buffer Definitions

The integration uses two main Protocol Buffer definition files:

### order.proto

Defines the Order service and related messages:

```protobuf
syntax = "proto3";

package hms.order.v1;

import "google/protobuf/timestamp.proto";

// Order service definition for FFI interface
service OrderService {
  // Create a new order
  rpc CreateOrder(CreateOrderRequest) returns (OrderResponse);
  
  // Get order details
  rpc GetOrder(GetOrderRequest) returns (OrderResponse);
  
  // Update an existing order
  rpc UpdateOrder(UpdateOrderRequest) returns (OrderResponse);
  
  // ...other methods...
}

// ...message definitions...
```

### oms_integration.proto

Defines the OMS Integration service and related messages:

```protobuf
syntax = "proto3";

package hms.order.v1;

import "google/protobuf/timestamp.proto";

// OMS Integration service definition for FFI interface
service OMSIntegrationService {
  // Send order to OMS
  rpc SendOrderToOMS(SendOrderToOMSRequest) returns (SendOrderToOMSResponse);
  
  // Sync order status with OMS
  rpc SyncOrderStatus(SyncOrderStatusRequest) returns (SyncOrderStatusResponse);
  
  // ...other methods...
}

// ...message definitions...
```

## Implementation Components

### 1. OrderSerializer

Handles serialization and deserialization between HMS-API Order entities and FFI protobuf messages.

Key methods:
- `orderToProto()`: Converts an Order entity to a Protocol Buffer message
- `protoToOrder()`: Converts a Protocol Buffer message to an Order entity
- `orderItemToProto()`: Converts an OrderItem entity to a Protocol Buffer message
- `protoToOrderItem()`: Converts a Protocol Buffer message to an OrderItem entity
- `mapStatusToProto()`: Maps API status strings to Protocol Buffer enums
- `mapStatusFromProto()`: Maps Protocol Buffer enums to API status strings

### 2. OMSIntegrationService

Implements the OMS integration service using FFI.

Key methods:
- `sendOrderToOMS()`: Sends a new order to HMS-OMS
- `syncOrderStatus()`: Syncs order status with HMS-OMS
- `fetchOrderFromOMS()`: Fetches order details from HMS-OMS
- `handleStatusUpdate()`: Handles order status update webhooks
- `handleOrderFulfilled()`: Handles order fulfilled webhooks
- `verifyWebhookSignature()`: Verifies webhook signatures

### 3. FFIServiceProvider

Registers FFI services with the Laravel dependency injection container.

## FFI Type Mapping

The integration maps between language-specific types and FFI types as follows:

| PHP Type               | Protocol Buffer Type          | Ruby Type              |
|------------------------|-------------------------------|------------------------|
| int                    | int32/int64                   | Integer                |
| float                  | float/double                  | Float                  |
| string                 | string                        | String                 |
| array                  | repeated                      | Array                  |
| DateTime               | google.protobuf.Timestamp     | Time                   |
| associative array      | map<string, string>           | Hash                   |
| Order                  | OrderData                     | Order                  |
| OrderItem              | OrderItemData                 | OrderItem              |

## Security Considerations

1. **Webhook Authentication**: All webhooks are authenticated using HMAC signatures
2. **Sensitive Data**: No sensitive data is transmitted in plain text
3. **Input Validation**: All inputs are validated using Protocol Buffer schemas
4. **Error Handling**: Comprehensive error handling for all FFI calls
5. **Logging**: Detailed logging for debugging and audit purposes

## Performance Considerations

1. **Serialization Efficiency**: Protocol Buffers provides compact binary serialization
2. **Caching**: Frequently used schema information is cached
3. **Connection Management**: Connections are pooled and reused
4. **Error Recovery**: Retry mechanisms for transient failures
5. **Monitoring**: Performance metrics are collected for optimization

## Testing

The integration includes comprehensive test coverage:

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test components working together
3. **End-to-End Tests**: Test the complete flow from API to OMS
4. **Performance Tests**: Test performance under load
5. **Failure Tests**: Test behavior under failure conditions

## Deployment

Deployment of the integration requires:

1. **Protocol Buffer Compiler**: Install protoc on the build server
2. **FFI Extension**: Ensure PHP FFI extension is enabled
3. **Shared Libraries**: Deploy shared libraries for FFI bindings
4. **Configuration**: Configure FFI paths and security settings
5. **Monitoring**: Set up monitoring and alerting

## Troubleshooting

Common issues and solutions:

1. **Serialization Errors**: Check Protocol Buffer version compatibility
2. **FFI Errors**: Ensure shared libraries are accessible and permissions are correct
3. **Type Errors**: Check for type compatibility issues between languages
4. **Performance Issues**: Monitor serialization overhead and optimize
5. **Webhook Failures**: Check signature verification and payload format

## Future Enhancements

Planned enhancements for the integration:

1. **Streaming Support**: Add support for streaming large datasets
2. **Schema Evolution**: Better handle schema changes
3. **Zero-Copy Optimization**: Implement zero-copy techniques for large payloads
4. **Distributed Tracing**: Add OpenTelemetry integration
5. **Enhanced Security**: Add mutual TLS authentication