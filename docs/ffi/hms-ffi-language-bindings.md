# HMS-FFI Language-Specific Bindings Architecture

This document outlines the architecture for language-specific bindings in the HMS Foreign Function Interface (FFI) system. These bindings provide the necessary adapters between the HMS-FFI Core Library and the various programming languages used in HMS components.

## 1. Common Binding Architecture

Each language binding shares a common architectural pattern while adapting to language-specific idioms:

```
┌─────────────────────────────────────────────────────────────────┐
│                Language-Specific Application Code                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       High-Level API Layer                       │
│                                                                 │
│  • Language-idiomatic interfaces                                │
│  • Type conversion helpers                                      │
│  • Error handling wrappers                                      │
│  • Async/Sync adapters                                          │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Language Binding Core                        │
│                                                                 │
│  • Type marshaling/unmarshaling                                 │
│  • Memory management                                            │
│  • Function dispatch                                            │
│  • Error translation                                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FFI Interface Layer                        │
│                                                                 │
│  • Low-level FFI calls                                          │
│  • Direct interface to HMS-FFI Core                            │
│  • Raw data handling                                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        HMS-FFI Core Library                      │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1 Binding Components

Each language binding will include:

1. **Generated Code**:
   - Interface stubs generated from Protocol Buffer definitions
   - Type converters for standard types
   - Service client/server code

2. **Helper Libraries**:
   - Language-specific utilities
   - Async/sync adapters
   - Stream handling
   - Error management

3. **Runtime Components**:
   - Memory management
   - Thread/context management
   - Lifecycle hooks

4. **Testing Utilities**:
   - Mock generators
   - Testing helpers
   - Validation utilities

## 2. Language-Specific Binding Designs

### 2.1 Go Binding (HMS-SYS, HMS-EMR)

```go
// High-Level API Example
type HMSServiceClient struct {
    client ffi.ServiceClient
    ctx    context.Context
}

func NewHMSServiceClient(ctx context.Context) *HMSServiceClient {
    return &HMSServiceClient{
        client: ffi.NewServiceClient("hms.service"),
        ctx:    ctx,
    }
}

func (c *HMSServiceClient) ProcessHealthData(data *HealthData) (*HealthResult, error) {
    req := &ffi.Request{
        Function: "ProcessHealthData",
        Args:     ffi.MarshalArgs(data),
    }
    
    resp, err := c.client.Call(c.ctx, req)
    if err != nil {
        return nil, fmt.Errorf("FFI call failed: %w", err)
    }
    
    result := &HealthResult{}
    if err := ffi.UnmarshalResult(resp, result); err != nil {
        return nil, fmt.Errorf("failed to unmarshal result: %w", err)
    }
    
    return result, nil
}

// Async version
func (c *HMSServiceClient) ProcessHealthDataAsync(data *HealthData) <-chan *AsyncResult[*HealthResult] {
    resultCh := make(chan *AsyncResult[*HealthResult], 1)
    
    go func() {
        result, err := c.ProcessHealthData(data)
        resultCh <- &AsyncResult[*HealthResult]{
            Result: result,
            Error:  err,
        }
        close(resultCh)
    }()
    
    return resultCh
}
```

#### Key Features:

1. **Context Support**:
   - Full integration with Go's context package
   - Context-based cancellation
   - Context-based timeouts

2. **Goroutine Safety**:
   - Thread-safe client implementations
   - Protection against concurrent access issues

3. **Error Handling**:
   - Error wrapping with Go 1.13+ error chains
   - Detailed error information

4. **Type System Integration**:
   - Support for Go struct tags
   - Automatic marshaling/unmarshaling
   - Support for Go interfaces

### 2.2 Rust Binding (HMS-CDF)

```rust
// High-Level API Example
pub struct HmsServiceClient {
    client: ffi::ServiceClient,
}

impl HmsServiceClient {
    pub fn new() -> Result<Self, HmsError> {
        Ok(Self {
            client: ffi::ServiceClient::new("hms.service")?,
        })
    }
    
    pub fn process_health_data(&self, data: &HealthData) -> Result<HealthResult, HmsError> {
        let request = ffi::Request {
            function: "ProcessHealthData".to_string(),
            args: ffi::marshal_args(data)?,
        };
        
        let response = self.client.call(&request)?;
        let result = ffi::unmarshal_result(&response)?;
        
        Ok(result)
    }
    
    // Async version
    pub async fn process_health_data_async(&self, data: &HealthData) -> Result<HealthResult, HmsError> {
        let request = ffi::Request {
            function: "ProcessHealthData".to_string(),
            args: ffi::marshal_args(data)?,
        };
        
        let response = self.client.call_async(&request).await?;
        let result = ffi::unmarshal_result(&response)?;
        
        Ok(result)
    }
}

// Implement service handler
#[derive(FfiService)]
#[ffi_service(name = "hms.rust.service")]
pub struct HmsServiceImpl {
    // Service implementation
}

#[ffi_methods]
impl HmsServiceImpl {
    #[ffi_method]
    pub fn process_health_data(&self, data: HealthData) -> Result<HealthResult, HmsError> {
        // Implementation
    }
    
    #[ffi_method(stream)]
    pub fn stream_health_updates(&self) -> impl Stream<Item = Result<HealthUpdate, HmsError>> {
        // Stream implementation
    }
}
```

#### Key Features:

1. **Ownership Model**:
   - Integration with Rust's ownership system
   - Zero-copy data handling where possible
   - Strict memory safety guarantees

2. **Error Handling**:
   - Result-based error handling
   - Rich error types with context
   - Error conversion between FFI and Rust

3. **Async Support**:
   - Full support for async/await
   - Future-based async API
   - Stream-based APIs for continuous data

4. **Macro System**:
   - Procedural macros for service definitions
   - Attribute macros for FFI exports
   - Derive macros for FFI types

### 2.3 Python Binding (HMS-A2A, HMS-AGT)

```python
# High-Level API Example
class HmsServiceClient:
    def __init__(self):
        self.client = ffi.ServiceClient("hms.service")
    
    def process_health_data(self, data: HealthData) -> HealthResult:
        request = ffi.Request(
            function="ProcessHealthData",
            args=ffi.marshal_args(data)
        )
        
        try:
            response = self.client.call(request)
            return ffi.unmarshal_result(response, HealthResult)
        except ffi.FFIError as e:
            raise HmsError(f"FFI call failed: {e}") from e
    
    # Async version
    async def process_health_data_async(self, data: HealthData) -> HealthResult:
        request = ffi.Request(
            function="ProcessHealthData",
            args=ffi.marshal_args(data)
        )
        
        try:
            response = await self.client.call_async(request)
            return ffi.unmarshal_result(response, HealthResult)
        except ffi.FFIError as e:
            raise HmsError(f"FFI call failed: {e}") from e
    
    # Generator version
    def stream_health_updates(self) -> Generator[HealthUpdate, None, None]:
        request = ffi.Request(
            function="StreamHealthUpdates",
            args=ffi.marshal_args({})
        )
        
        for response in self.client.stream(request):
            yield ffi.unmarshal_result(response, HealthUpdate)

# Service implementation with decorator-based registration
@ffi.service("hms.python.service")
class HmsServiceImpl:
    @ffi.method
    def process_health_data(self, data: HealthData) -> HealthResult:
        # Implementation
        return HealthResult(...)
    
    @ffi.method(stream=True)
    def stream_health_updates(self) -> Generator[HealthUpdate, None, None]:
        # Implementation
        yield HealthUpdate(...)
```

#### Key Features:

1. **Type Hints**:
   - Full Python type hint support
   - Runtime type checking
   - IDE integration

2. **Async Support**:
   - Integration with asyncio
   - Async/await syntax support
   - Support for async generators

3. **Pythonic Interface**:
   - Decorator-based service registration
   - Context manager support
   - Generator-based streams

4. **GIL Management**:
   - Proper handling of Python's GIL
   - Thread-safe operations
   - CPU-bound operation optimizations

### 2.4 JavaScript/TypeScript Binding (HMS-ABC, HMS-AGX)

```typescript
// High-Level API Example
class HmsServiceClient {
  private client: ffi.ServiceClient;
  
  constructor() {
    this.client = new ffi.ServiceClient("hms.service");
  }
  
  async processHealthData(data: HealthData): Promise<HealthResult> {
    const request: ffi.Request = {
      function: "ProcessHealthData",
      args: ffi.marshalArgs(data)
    };
    
    try {
      const response = await this.client.call(request);
      return ffi.unmarshalResult<HealthResult>(response);
    } catch (error) {
      throw new HmsError(`FFI call failed: ${error.message}`, { cause: error });
    }
  }
  
  // Stream version using async iterators
  async *streamHealthUpdates(): AsyncIterableIterator<HealthUpdate> {
    const request: ffi.Request = {
      function: "StreamHealthUpdates",
      args: ffi.marshalArgs({})
    };
    
    try {
      const stream = this.client.createStream(request);
      for await (const response of stream) {
        yield ffi.unmarshalResult<HealthUpdate>(response);
      }
    } catch (error) {
      throw new HmsError(`FFI stream failed: ${error.message}`, { cause: error });
    }
  }
}

// Service implementation with decorator-based registration
@ffi.service("hms.typescript.service")
class HmsServiceImpl implements IHmsService {
  @ffi.method()
  async processHealthData(data: HealthData): Promise<HealthResult> {
    // Implementation
    return new HealthResult();
  }
  
  @ffi.method({ stream: true })
  async *streamHealthUpdates(): AsyncIterableIterator<HealthUpdate> {
    // Implementation
    yield new HealthUpdate();
  }
}
```

#### Key Features:

1. **TypeScript Integration**:
   - Strong TypeScript type definitions
   - Interface-based service definitions
   - Generic type parameters

2. **Promise-Based API**:
   - Full Promise integration
   - async/await support
   - Error handling with Promise chains

3. **Modern JavaScript Features**:
   - Async iterators for streams
   - Decorators for metadata
   - Class-based interface

4. **Node.js and Browser Support**:
   - Compatible with Node.js environment
   - Browser-compatible version
   - Transport selection based on environment

### 2.5 PHP Binding (HMS-API)

```php
// High-Level API Example
class HmsServiceClient
{
    private $client;
    
    public function __construct()
    {
        $this->client = new \FFI\ServiceClient("hms.service");
    }
    
    public function processHealthData(HealthData $data): HealthResult
    {
        $request = new \FFI\Request(
            "ProcessHealthData",
            \FFI\marshalArgs($data)
        );
        
        try {
            $response = $this->client->call($request);
            return \FFI\unmarshalResult($response, HealthResult::class);
        } catch (\FFI\FFIException $e) {
            throw new HmsException("FFI call failed: " . $e->getMessage(), 0, $e);
        }
    }
    
    // Async version using promises
    public function processHealthDataAsync(HealthData $data): PromiseInterface
    {
        return new Promise(function ($resolve, $reject) use ($data) {
            try {
                $result = $this->processHealthData($data);
                $resolve($result);
            } catch (\Exception $e) {
                $reject($e);
            }
        });
    }
}

// Service implementation with attribute-based registration
#[FFI\Service("hms.php.service")]
class HmsServiceImpl
{
    #[FFI\Method]
    public function processHealthData(HealthData $data): HealthResult
    {
        // Implementation
        return new HealthResult();
    }
    
    #[FFI\Method(stream: true)]
    public function streamHealthUpdates(): \Generator
    {
        // Implementation
        yield new HealthUpdate();
    }
}
```

#### Key Features:

1. **Laravel Integration**:
   - Service provider for Laravel
   - Facade for easy access
   - Middleware support

2. **Type Safety**:
   - PHP 8.0+ type hints
   - Attribute-based metadata
   - Runtime type checking

3. **Error Handling**:
   - Exception-based error handling
   - Exception hierarchy
   - Detailed error information

4. **Compatibility**:
   - PHP 7.4+ support
   - PSR standards compliance
   - Composer integration

### 2.6 Ruby Binding (HMS-ACH, HMS-ESR)

```ruby
# High-Level API Example
class HmsServiceClient
  def initialize
    @client = FFI::ServiceClient.new("hms.service")
  end
  
  def process_health_data(data)
    request = FFI::Request.new(
      function: "ProcessHealthData",
      args: FFI.marshal_args(data)
    )
    
    begin
      response = @client.call(request)
      FFI.unmarshal_result(response, HealthResult)
    rescue FFI::Error => e
      raise HmsError, "FFI call failed: #{e.message}"
    end
  end
  
  # Async version
  def process_health_data_async(data)
    Thread.new do
      begin
        result = process_health_data(data)
        yield result, nil if block_given?
      rescue => e
        yield nil, e if block_given?
      end
    end
  end
  
  # Stream version
  def stream_health_updates
    request = FFI::Request.new(
      function: "StreamHealthUpdates",
      args: FFI.marshal_args({})
    )
    
    @client.stream(request).each do |response|
      yield FFI.unmarshal_result(response, HealthUpdate)
    end
  end
end

# Service implementation with DSL-based registration
module HmsService
  extend FFI::ServiceDSL
  
  service_name "hms.ruby.service"
  
  method :process_health_data do |data|
    # Implementation
    HealthResult.new
  end
  
  stream_method :stream_health_updates do
    # Implementation
    produce HealthUpdate.new
  end
end
```

#### Key Features:

1. **Ruby Idioms**:
   - Block-based APIs
   - DSL for service definition
   - Ruby conventions

2. **Rails Integration**:
   - Rails engine
   - ActiveJob integration
   - ActionCable integration

3. **Concurrency**:
   - Thread safety
   - Fiber support
   - GVL handling

4. **Dynamic Features**:
   - Metaprogramming capabilities
   - Duck typing support
   - Ruby introspection

## 3. Code Generation Architecture

The code generation system produces consistent bindings across all languages:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Protocol Buffer Files                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      HMS-FFI Code Generator                      │
└──┬───────────┬───────────┬───────────┬──────────┬───────────┬───┘
   │           │           │           │          │           │
   ▼           ▼           ▼           ▼          ▼           ▼
┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│  Go  │   │ Rust │   │Python│   │TypeSc│   │ PHP  │   │ Ruby │
│ Code │   │ Code │   │ Code │   │ript  │   │ Code │   │ Code │
└──────┘   └──────┘   └──────┘   └──────┘   └──────┘   └──────┘
```

### 3.1 Generated Code Types

For each language, the code generator produces:

1. **Data Types**:
   - Data structures matching Protocol Buffer definitions
   - Serialization/deserialization code
   - Type converters

2. **Service Interfaces**:
   - Client stubs for calling services
   - Server interfaces for implementing services
   - Method signatures

3. **Helper Types**:
   - Common utilities
   - Error types
   - Configuration structures

### 3.2 IDE Integration

The generated code includes IDE support:

1. **TypeScript/JavaScript**:
   - TypeScript declaration files
   - JSDoc annotations

2. **Python**:
   - Type hints (PEP 484)
   - Docstrings (Google style)

3. **Go**:
   - Go doc comments
   - Examples

4. **Rust**:
   - Rust doc comments
   - Examples

5. **PHP**:
   - PHPDoc annotations
   - IDE type hints

6. **Ruby**:
   - YARD documentation
   - Type signatures (RBS)

## 4. Testing Strategy

Each language binding includes dedicated testing utilities:

### 4.1 Unit Tests

- Test individual binding components
- Mock HMS-FFI Core interactions
- Test type conversions
- Test error handling

### 4.2 Integration Tests

- Test interactions with HMS-FFI Core
- Test cross-language calls
- Test error propagation
- Test performance

### 4.3 Test Harnesses

Each language binding includes:

- Automated test runners
- Fixtures
- Mocks
- Benchmarks

## 5. Deployment and Packaging

### 5.1 Go Binding

- Go module
- Standard Go package structure
- Vendoring support

### 5.2 Rust Binding

- Cargo crate
- Feature flags for optional components
- Workspace integration

### 5.3 Python Binding

- PyPI package
- Wheel distribution
- Requirements.txt support

### 5.4 TypeScript/JavaScript Binding

- npm package
- ES modules and CommonJS formats
- Type declarations

### 5.5 PHP Binding

- Composer package
- PSR-4 autoloading
- Laravel package

### 5.6 Ruby Binding

- Ruby gem
- Bundler support
- Rails engine option

## 6. Language-Specific Considerations

### 6.1 Memory Management

Each language has specific memory management considerations:

- **Go**: Garbage collection, stack vs. heap allocation
- **Rust**: Ownership, borrowing, lifetimes
- **Python**: Reference counting, cyclic GC
- **JavaScript**: V8 GC, object lifecycles
- **PHP**: Reference counting, ZVal system
- **Ruby**: Mark and sweep GC

### 6.2 Threading Models

Each language has different threading models to consider:

- **Go**: Goroutines, channels
- **Rust**: Fearless concurrency, async/await
- **Python**: GIL limitations, asyncio
- **JavaScript**: Single-threaded event loop
- **PHP**: Request-based isolation
- **Ruby**: GVL limitations, fibers

### 6.3 Type System Differences

Each language's type system requires specific handling:

- **Go**: Structural typing, interfaces
- **Rust**: Algebraic data types, traits
- **Python**: Dynamic typing, gradual typing
- **TypeScript**: Structural typing, union types
- **PHP**: Nominal typing, duck typing
- **Ruby**: Dynamic typing, duck typing

## 7. Implementation Priorities

The language bindings will be implemented in this order:

1. **Go and Rust**: Primary systems components
2. **Python and TypeScript**: Agent components
3. **PHP**: API components
4. **Ruby**: ACH and ESR components

## 8. Conclusion

This architecture provides a comprehensive approach to designing language-specific bindings for the HMS-FFI system. By following these guidelines, we can create consistent, high-quality bindings that provide idiomatic interfaces in each language while maintaining compatibility and performance across the HMS ecosystem.