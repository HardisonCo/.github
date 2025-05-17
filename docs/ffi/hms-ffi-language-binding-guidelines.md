# HMS FFI Language Bindings Guidelines

This document provides guidelines for implementing language-specific bindings for the HMS Foreign Function Interface (FFI) system.

## 1. Overview

The HMS FFI system enables cross-language communication between different components of the HMS ecosystem. Each supported language requires well-designed bindings that follow idiomatic patterns for that language while maintaining compatibility with the underlying protocol buffer definitions.

## 2. Supported Languages

The HMS FFI system supports the following languages:

- Go
- Rust
- Python
- PHP
- TypeScript/JavaScript
- Ruby

## 3. Common Requirements

Regardless of language, all bindings must:

1. **Correctness**: Faithfully represent proto definitions
2. **Compatibility**: Work seamlessly with other language bindings
3. **Performance**: Minimize overhead in serialization/deserialization
4. **Error Handling**: Provide clear and idiomatic error handling
5. **Documentation**: Include comprehensive API documentation
6. **Testing**: Include thorough unit and integration tests

## 4. Go Bindings

### 4.1 Code Generation

Use the standard `protoc-gen-go` plugin with the following options:

```bash
protoc \
  --go_out=paths=source_relative:. \
  --go-grpc_out=paths=source_relative:. \
  proto/hms/component/v1/*.proto
```

### 4.2 Package Structure

```
hms/component/v1/
  ├── component.pb.go       # Generated message code
  ├── component_grpc.pb.go  # Generated service code
  ├── component_ext.go      # Extensions and helpers
  └── component_test.go     # Tests
```

### 4.3 Idiomatic Patterns

- Use Go interfaces for services
- Follow Go naming conventions (e.g., `PascalCase` for exported names)
- Use context for cancellation and timeout
- Return errors instead of exceptions
- Use pointer receivers consistently

### 4.4 Example

```go
// Client code
client := componentpb.NewComponentServiceClient(conn)
resp, err := client.MethodName(ctx, &componentpb.MethodNameRequest{
    Field: "value",
})
if err != nil {
    return fmt.Errorf("failed to call MethodName: %w", err)
}

// Server code
type server struct {
    componentpb.UnimplementedComponentServiceServer
}

func (s *server) MethodName(ctx context.Context, req *componentpb.MethodNameRequest) (*componentpb.MethodNameResponse, error) {
    if req.Field == "" {
        return nil, status.Error(codes.InvalidArgument, "field is required")
    }
    return &componentpb.MethodNameResponse{
        Result: "processed: " + req.Field,
    }, nil
}
```

## 5. Rust Bindings

### 5.1 Code Generation

Use `prost` and `tonic` for Rust bindings:

```bash
cargo run --bin protoc-gen-tonic -- \
  --proto-path=proto \
  --output=src/gen \
  proto/hms/component/v1/*.proto
```

### 5.2 Package Structure

```
src/
  ├── gen/
  │   └── hms.component.v1.rs  # Generated code
  ├── component/
  │   ├── mod.rs               # Module definition
  │   ├── client.rs            # Client implementation
  │   ├── server.rs            # Server implementation
  │   └── error.rs             # Error types
  └── lib.rs                   # Library entry point
```

### 5.3 Idiomatic Patterns

- Use Rust traits for service interfaces
- Implement proper error types with `std::error::Error`
- Use async/await for asynchronous operations
- Follow Rust naming conventions (e.g., `snake_case` for functions)
- Use Option/Result for handling nullability and errors

### 5.4 Example

```rust
// Client code
let mut client = ComponentServiceClient::connect(endpoint).await?;
let request = MethodNameRequest {
    field: "value".to_string(),
    ..Default::default()
};
let response = client.method_name(request).await?;

// Server code
#[derive(Debug, Default)]
pub struct ComponentServer;

#[tonic::async_trait]
impl ComponentService for ComponentServer {
    async fn method_name(
        &self,
        request: Request<MethodNameRequest>,
    ) -> Result<Response<MethodNameResponse>, Status> {
        let req = request.into_inner();
        if req.field.is_empty() {
            return Err(Status::invalid_argument("field is required"));
        }
        Ok(Response::new(MethodNameResponse {
            result: format!("processed: {}", req.field),
        }))
    }
}
```

## 6. Python Bindings

### 6.1 Code Generation

Use `grpcio-tools` or `grpc-tools` for Python bindings:

```bash
python -m grpc_tools.protoc \
  --python_out=. \
  --grpc_python_out=. \
  --proto_path=proto \
  proto/hms/component/v1/*.proto
```

### 6.2 Package Structure

```
hms/
  └── component/
      └── v1/
          ├── __init__.py           # Package initialization
          ├── component_pb2.py      # Generated message code
          ├── component_pb2_grpc.py # Generated service code
          ├── client.py             # Client wrapper
          ├── server.py             # Server implementation
          └── test_component.py     # Tests
```

### 6.3 Idiomatic Patterns

- Use Python classes for service implementations
- Support both synchronous and asynchronous APIs
- Follow PEP 8 naming conventions
- Use proper type hints (PEP 484)
- Raise exceptions for errors
- Support context managers for cleanup

### 6.4 Example

```python
# Client code
with ComponentServiceClient() as client:
    response = client.method_name(MethodNameRequest(field="value"))
    print(f"Result: {response.result}")

# Async client code
async with ComponentServiceAsyncClient() as client:
    response = await client.method_name(MethodNameRequest(field="value"))
    print(f"Result: {response.result}")

# Server code
class ComponentServicer(component_pb2_grpc.ComponentServiceServicer):
    def MethodName(self, request, context):
        if not request.field:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("field is required")
            return component_pb2.MethodNameResponse()
        
        return component_pb2.MethodNameResponse(
            result=f"processed: {request.field}"
        )
```

## 7. PHP Bindings

### 7.1 Code Generation

Use `protoc-gen-php` for PHP bindings:

```bash
protoc \
  --php_out=. \
  --grpc_php_out=. \
  --proto_path=proto \
  proto/hms/component/v1/*.proto
```

### 7.2 Package Structure

```
HMS/
  └── FFI/
      └── Protos/
          └── Component/
              └── V1/
                  ├── ComponentClient.php     # Client implementation
                  ├── ComponentService.php    # Service interface
                  ├── MethodNameRequest.php   # Request message
                  ├── MethodNameResponse.php  # Response message
                  └── GPBMetadata/            # Metadata
```

### 7.3 Idiomatic Patterns

- Use PHP namespaces according to proto package
- Follow PSR-1 and PSR-2 coding standards
- Use type declarations (PHP 7.4+)
- Use exceptions for error handling
- Support Laravel integration for HMS-API components

### 7.4 Example

```php
// Client code
$client = new \HMS\FFI\Protos\Component\V1\ComponentClient($channel);
$request = new \HMS\FFI\Protos\Component\V1\MethodNameRequest();
$request->setField("value");

try {
    [$response, $status] = $client->MethodName($request)->wait();
    echo "Result: " . $response->getResult() . "\n";
} catch (\Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

// Server code
class ComponentServiceImpl extends \HMS\FFI\Protos\Component\V1\ComponentServiceBase {
    public function MethodName(
        \HMS\FFI\Protos\Component\V1\MethodNameRequest $request,
        \Grpc\ServerContext $context
    ): \HMS\FFI\Protos\Component\V1\MethodNameResponse {
        if ($request->getField() === '') {
            $context->setStatus(\Grpc\Status::INVALID_ARGUMENT, 'field is required');
            return new \HMS\FFI\Protos\Component\V1\MethodNameResponse();
        }
        
        $response = new \HMS\FFI\Protos\Component\V1\MethodNameResponse();
        $response->setResult("processed: " . $request->getField());
        return $response;
    }
}
```

## 8. TypeScript/JavaScript Bindings

### 8.1 Code Generation

Use `protoc-gen-ts` for TypeScript bindings:

```bash
protoc \
  --ts_out=service=grpc-web:. \
  --js_out=import_style=commonjs,binary:. \
  --proto_path=proto \
  proto/hms/component/v1/*.proto
```

### 8.2 Package Structure

```
src/
  └── hms/
      └── component/
          └── v1/
              ├── component_pb.js     # Generated JavaScript
              ├── component_pb.d.ts   # TypeScript definitions
              ├── component_grpc.js   # Service JavaScript
              ├── component_grpc.d.ts # Service TypeScript
              ├── index.ts            # Package exports
              └── component.test.ts   # Tests
```

### 8.3 Idiomatic Patterns

- Use ES modules for imports/exports
- Follow TypeScript naming conventions
- Use Promises for asynchronous operations
- Use proper TypeScript interfaces and types
- Support both Node.js and browser environments
- Use async/await for asynchronous code

### 8.4 Example

```typescript
// Client code
const client = new ComponentServiceClient(endpoint);

const request = new MethodNameRequest();
request.setField("value");

client.methodName(request)
  .then(response => {
    console.log(`Result: ${response.getResult()}`);
  })
  .catch(error => {
    console.error(`Error: ${error.message}`);
  });

// Async client code
async function callService() {
  const client = new ComponentServiceClient(endpoint);
  
  const request = new MethodNameRequest();
  request.setField("value");
  
  try {
    const response = await client.methodName(request);
    console.log(`Result: ${response.getResult()}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
  }
}

// Server code (Node.js)
class ComponentServer implements IComponentServer {
  methodName(
    call: grpc.ServerUnaryCall<MethodNameRequest, MethodNameResponse>,
    callback: grpc.sendUnaryData<MethodNameResponse>
  ): void {
    const request = call.request;
    
    if (!request.getField()) {
      const error = new Error('field is required');
      return callback({
        code: grpc.status.INVALID_ARGUMENT,
        details: error.message
      }, null);
    }
    
    const response = new MethodNameResponse();
    response.setResult(`processed: ${request.getField()}`);
    callback(null, response);
  }
}
```

## 9. Ruby Bindings

### 9.1 Code Generation

Use `grpc-tools` for Ruby bindings:

```bash
grpc_tools_ruby_protoc \
  --ruby_out=. \
  --grpc_out=. \
  --proto_path=proto \
  proto/hms/component/v1/*.proto
```

### 9.2 Package Structure

```
lib/
  └── hms/
      └── component/
          └── v1/
              ├── component_pb.rb      # Generated message code
              ├── component_services_pb.rb  # Generated service code
              ├── component_client.rb  # Client wrapper
              ├── component_server.rb  # Server implementation
              └── component_test.rb    # Tests
```

### 9.3 Idiomatic Patterns

- Follow Ruby naming conventions (e.g., `snake_case` for methods)
- Use Ruby modules for namespacing
- Use Ruby exceptions for error handling
- Support both blocking and non-blocking APIs
- Use Ruby blocks for callbacks

### 9.4 Example

```ruby
# Client code
client = HMS::Component::V1::ComponentService::Stub.new(
  address, GRPC::Core::ChannelCredentials.insecure
)

request = HMS::Component::V1::MethodNameRequest.new(field: "value")
begin
  response = client.method_name(request)
  puts "Result: #{response.result}"
rescue GRPC::BadStatus => e
  puts "Error: #{e.message}"
end

# Server code
class ComponentServiceImpl < HMS::Component::V1::ComponentService::Service
  def method_name(request, _call)
    if request.field.empty?
      raise GRPC::InvalidArgument.new("field is required")
    end
    
    HMS::Component::V1::MethodNameResponse.new(
      result: "processed: #{request.field}"
    )
  end
end
```

## 10. Integration Guidelines

### 10.1 Cross-Language Compatibility

- Use consistent naming across languages
- Ensure serialization formats are compatible
- Test cross-language calls for all services
- Maintain consistent error codes and messages

### 10.2 Error Handling

- Use standard gRPC error codes
- Include detailed error messages
- Propagate errors across language boundaries
- Map gRPC errors to language-specific errors

### 10.3 Authentication

- Support JWT authentication
- Pass authentication tokens consistently
- Handle authentication failures uniformly
- Support role-based access control

### 10.4 Versioning

- Use semantic versioning for all APIs
- Support backward compatibility
- Use proto versioning (v1, v2, etc.)
- Document breaking changes

## 11. Implementation Process

1. **Generate Base Code**: Use protoc to generate language-specific code
2. **Create Wrappers**: Implement idiomatic wrappers around generated code
3. **Add Error Handling**: Implement proper error handling and mapping
4. **Add Tests**: Create comprehensive unit and integration tests
5. **Document API**: Add language-specific API documentation
6. **Create Examples**: Provide usage examples for common scenarios

## 12. Build and Distribution

### 12.1 Go

- Use Go modules for dependency management
- Distribute as a Go module via GitHub
- Version using git tags

### 12.2 Rust

- Use Cargo for building and dependency management
- Distribute via crates.io
- Version using Cargo.toml

### 12.3 Python

- Use setuptools for packaging
- Distribute via PyPI
- Version using setuptools configuration

### 12.4 PHP

- Use Composer for dependency management
- Distribute via Packagist
- Version using composer.json

### 12.5 TypeScript/JavaScript

- Use npm/yarn for package management
- Distribute via npm
- Version using package.json

### 12.6 Ruby

- Use Bundler for dependency management
- Distribute via RubyGems
- Version using gemspec

## 13. Documentation Requirements

Each language binding must include:

1. **API Reference**: Comprehensive API documentation
2. **Getting Started Guide**: How to use the bindings
3. **Example Code**: Real-world usage examples
4. **Integration Guide**: How to integrate with HMS components
5. **Error Reference**: List of error codes and handling strategies

## 14. Quality Assurance

### 14.1 Linting and Style

- Go: gofmt, golint
- Rust: clippy, rustfmt
- Python: flake8, black
- PHP: PHP_CodeSniffer, PHPStan
- TypeScript: eslint, prettier
- Ruby: rubocop

### 14.2 Testing

- Unit tests for all generated code
- Integration tests for services
- Cross-language compatibility tests
- Performance benchmarks

### 14.3 CI/CD

- Automated testing on pull requests
- Compatibility testing matrix
- Version verification
- Documentation generation

## 15. Conclusion

These guidelines provide a standardized approach to implementing language-specific bindings for the HMS FFI system. By following these guidelines, developers can ensure that all FFI implementations are consistent, compatible, and maintainable across the entire HMS ecosystem.