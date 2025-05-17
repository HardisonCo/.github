# HMS Development Guide

This document serves as a comprehensive guide for developers working within the HMS ecosystem. It covers development standards, best practices, and guidelines for creating and maintaining HMS components.

## Development Environment Setup

### Prerequisites

- Node.js (v16+)
- Python (v3.9+)
- Rust (latest stable)
- Docker and Docker Compose
- Git

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CodifyHQ/HMS-DEV.git
   cd HMS-DEV
   ```

2. Install dependencies:
   ```bash
   # For Node.js components
   npm install

   # For Python components
   pip install -e .

   # For Rust components
   cargo build
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your specific settings
   ```

4. Initialize development environment:
   ```bash
   ./scripts/flow-tools.sh init
   ```

## Development Workflow

HMS follows a structured development workflow as described in the [Workflow Guide](/docs/WORKFLOW.md). Key points:

1. **Feature Development**:
   ```bash
   # Start a new feature
   ./scripts/flow-tools.sh feature start feature-name

   # Work in Pomodoro sessions
   ./scripts/flow-tools.sh session start

   # Complete feature
   ./scripts/flow-tools.sh feature finish
   ```

2. **Verification Process**:
   ```bash
   # Verify your development environment
   ./scripts/flow-tools.sh verify
   ```

3. **Testing**:
   ```bash
   # Run all tests
   npm test

   # Run specific tests
   npm test -- --testPathPattern=path/to/test
   ```

## Coding Standards

### General Principles

- **Readability**: Write clear, self-documenting code
- **Maintainability**: Design for future changes
- **Testability**: Make all code easily testable
- **Security**: Follow security best practices
- **Performance**: Consider efficiency and scalability

### JavaScript/TypeScript Standards

- Use TypeScript for type safety
- Follow 2-space indentation
- Use camelCase for variables and functions
- Use PascalCase for classes and interfaces
- Use async/await for asynchronous code
- Always include proper error handling

Example:

```typescript
/**
 * Retrieves tool information from the registry
 * @param toolId The unique identifier of the tool
 * @returns Tool information object
 * @throws RegistryError if tool not found or registry unavailable
 */
async function getToolInfo(toolId: string): Promise<ToolInfo> {
  try {
    const response = await fetch(`${REGISTRY_URL}/tools/${toolId}`);
    
    if (!response.ok) {
      throw new RegistryError(`Failed to fetch tool: ${response.statusText}`);
    }
    
    return await response.json() as ToolInfo;
  } catch (error) {
    logger.error(`Error fetching tool ${toolId}:`, error);
    throw error instanceof RegistryError 
      ? error 
      : new RegistryError(`Registry unavailable: ${error.message}`);
  }
}
```

### Python Standards

- Use type hints for all functions
- Follow 4-space indentation
- Use snake_case for variables and functions
- Use PascalCase for classes
- Use docstrings for all public functions (Google style)
- Handle exceptions appropriately

Example:

```python
def verify_tool(tool_id: str) -> VerificationResult:
    """
    Verifies a tool meets all quality and security standards.
    
    Args:
        tool_id: The unique identifier of the tool to verify
        
    Returns:
        VerificationResult containing pass/fail status and details
        
    Raises:
        ToolNotFoundError: If the tool cannot be found
        VerificationError: If the verification process fails
    """
    try:
        tool = registry_client.get_tool(tool_id)
        
        # Run verification checks
        security_result = security_scanner.scan(tool.source_code)
        quality_result = code_quality.analyze(tool.source_code)
        
        return VerificationResult(
            passed=security_result.passed and quality_result.passed,
            security_score=security_result.score,
            quality_score=quality_result.score,
            issues=security_result.issues + quality_result.issues
        )
    except RegistryClientError as e:
        logger.error(f"Failed to retrieve tool {tool_id}: {e}")
        raise ToolNotFoundError(f"Tool {tool_id} not found in registry")
    except Exception as e:
        logger.error(f"Verification error for tool {tool_id}: {e}")
        raise VerificationError(f"Failed to verify tool: {e}")
```

### Rust Standards

- Use Rust 2021 edition
- Follow standard Rust formatting (rustfmt)
- Use snake_case for variables and functions
- Use CamelCase for types and traits
- Include documentation comments for public APIs
- Use proper error handling with Result type

Example:

```rust
/// Executes a command in a sandboxed environment
///
/// # Arguments
///
/// * `command` - The command to execute
/// * `args` - Arguments for the command
/// * `timeout_ms` - Maximum execution time in milliseconds
///
/// # Returns
///
/// Result containing command output or error
///
/// # Errors
///
/// Returns an error if the command fails to execute or times out
pub fn execute_sandboxed_command(
    command: &str,
    args: &[&str], 
    timeout_ms: u64
) -> Result<CommandOutput, ExecutionError> {
    let sandbox = Sandbox::new()?;
    
    let execution = sandbox
        .configure()
        .with_command(command)
        .with_args(args)
        .with_timeout(timeout_ms)
        .with_memory_limit(MAX_MEMORY_MB)
        .build()?;
    
    match execution.run() {
        Ok(output) => Ok(CommandOutput {
            stdout: output.stdout,
            stderr: output.stderr,
            exit_code: output.exit_code,
            execution_time_ms: output.execution_time_ms,
        }),
        Err(e) => {
            log::error!("Sandbox execution failed: {}", e);
            Err(ExecutionError::SandboxError(e.to_string()))
        }
    }
}
```

## Project Structure

HMS components should follow a consistent structure:

```
HMS-[COMPONENT]/
  ├── README.md             # Component documentation
  ├── CONTRIBUTING.md       # Contribution guidelines
  ├── LICENSE               # License information
  ├── CLAUDE.md             # Guidance for Claude AI
  ├── docs/                 # Detailed documentation
  │   ├── index.md          # Documentation home
  │   ├── architecture.md   # Architecture details
  │   ├── api.md            # API documentation
  │   └── agent.md          # Agent capabilities
  ├── src/                  # Source code
  │   ├── index.[js|ts|py|rs]  # Entry point
  │   ├── controllers/      # Business logic
  │   ├── models/           # Data models
  │   ├── utils/            # Helper utilities
  │   ├── middleware/       # Middleware components
  │   └── services/         # Service implementations
  ├── tests/                # Test code
  │   ├── unit/             # Unit tests
  │   ├── integration/      # Integration tests
  │   └── fixtures/         # Test fixtures
  ├── examples/             # Example usage
  └── [build files]         # Build configuration
```

## Documentation Standards

HMS follows comprehensive documentation standards:

### Component Documentation

Each component must have:

1. **README.md**: Overview, quickstart, basic usage
2. **Architecture Document**: System design and component interactions
3. **API Documentation**: Endpoint and function documentation
4. **Integration Guide**: How to integrate with other components
5. **Development Guide**: How to develop the component

### Code Documentation

- All public APIs must be documented
- Include purpose, parameters, return values, and exceptions
- Provide usage examples for complex functionality
- Document non-obvious behavior and edge cases

### Documentation Format

Use Markdown for all documentation:

```markdown
# Component Name

Brief description of purpose and functionality.

## Installation

```bash
npm install @hms/component-name
```

## Usage

```javascript
import { someFunction } from '@hms/component-name';

const result = await someFunction('parameter');
console.log(result);
```

## API Reference

### someFunction(param)

Description of what the function does.

Parameters:
- `param` (string): Description of parameter

Returns:
- (Promise<Result>): Description of return value

Throws:
- `SomeError`: When something goes wrong
```

## Testing Standards

HMS follows a comprehensive testing approach:

### Test Types

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test system performance
5. **Security Tests**: Validate security measures

### Testing Guidelines

- Aim for high test coverage (>80%)
- Write tests before implementation when possible
- Test both success and failure cases
- Mock external dependencies
- Use meaningful test descriptions

### Example Unit Test (JavaScript/TypeScript)

```typescript
describe('Tool Registry', () => {
  describe('verifyTool', () => {
    it('should pass verification for valid tools', async () => {
      // Arrange
      const mockTool = {
        id: 'tool-123',
        name: 'Test Tool',
        source: 'https://github.com/test/repo'
      };
      
      mockRegistryClient.getTool.mockResolvedValue(mockTool);
      mockSecurityScanner.scan.mockResolvedValue({
        passed: true,
        score: 95,
        issues: []
      });
      
      // Act
      const result = await verifyTool('tool-123');
      
      // Assert
      expect(result.passed).toBe(true);
      expect(result.security_score).toBeGreaterThanOrEqual(90);
      expect(mockRegistryClient.getTool).toHaveBeenCalledWith('tool-123');
    });
    
    it('should fail verification for insecure tools', async () => {
      // Arrange
      const mockTool = {
        id: 'tool-456',
        name: 'Insecure Tool',
        source: 'https://github.com/test/insecure'
      };
      
      mockRegistryClient.getTool.mockResolvedValue(mockTool);
      mockSecurityScanner.scan.mockResolvedValue({
        passed: false,
        score: 65,
        issues: [
          { severity: 'high', description: 'Vulnerable dependency' }
        ]
      });
      
      // Act
      const result = await verifyTool('tool-456');
      
      // Assert
      expect(result.passed).toBe(false);
      expect(result.issues).toHaveLength(1);
      expect(result.issues[0].severity).toBe('high');
    });
    
    it('should throw ToolNotFoundError when tool does not exist', async () => {
      // Arrange
      mockRegistryClient.getTool.mockRejectedValue(
        new Error('Tool not found')
      );
      
      // Act & Assert
      await expect(verifyTool('non-existent')).rejects.toThrow(ToolNotFoundError);
    });
  });
});
```

## Security Guidelines

HMS enforces strict security standards:

### Secure Coding Practices

1. **Input Validation**: Validate all input data
2. **Output Encoding**: Encode output to prevent injection attacks
3. **Authentication**: Implement proper authentication mechanisms
4. **Authorization**: Enforce access control for all resources
5. **Sensitive Data**: Protect sensitive information
6. **Error Handling**: Do not expose sensitive information in errors
7. **Logging**: Do not log sensitive data
8. **Dependency Management**: Keep dependencies updated

### Security Example

```typescript
// GOOD: Proper input validation
function processUserInput(input: unknown): ProcessedData {
  // Validate input
  if (typeof input !== 'object' || input === null) {
    throw new ValidationError('Input must be an object');
  }
  
  // Type assertion with validation
  const validatedInput = validateUserInput(input);
  
  // Process validated input
  return {
    processed: true,
    data: processData(validatedInput)
  };
}

// BAD: SQL Injection vulnerability
function getUserData(userId) {
  const query = `SELECT * FROM users WHERE id = ${userId}`; // Vulnerable!
  return database.execute(query);
}

// GOOD: Parameterized query
function getUserData(userId: string): Promise<User> {
  const query = `SELECT * FROM users WHERE id = ?`;
  return database.execute(query, [userId]);
}
```

## Deployment Guidelines

HMS components follow standardized deployment processes:

### Deployment Pipeline

1. **Build**: Compile and package the component
2. **Test**: Run all test suites
3. **Security Scan**: Perform security analysis
4. **Artifact Creation**: Create deployment artifacts
5. **Deployment**: Deploy to target environment
6. **Verification**: Verify deployment success
7. **Monitoring**: Set up monitoring and alerts

### Deployment Configuration

```yaml
# Example deployment.yaml
version: '1.0'
component: 'HMS-DEV'
environments:
  development:
    url: 'https://dev.hms.example.com'
    resources:
      cpu: '1'
      memory: '2Gi'
    replicas: 1
    
  staging:
    url: 'https://staging.hms.example.com'
    resources:
      cpu: '2'
      memory: '4Gi'
    replicas: 2
    
  production:
    url: 'https://hms.example.com'
    resources:
      cpu: '4'
      memory: '8Gi'
    replicas: 3
    scaling:
      min: 3
      max: 10
      cpu_threshold: 70
    
dependencies:
  - component: 'HMS-A2A'
    version: '^1.0.0'
  - component: 'HMS-DOC'
    version: '^1.0.0'
```

## Contribution Guidelines

Guidelines for contributing to HMS components:

### Contribution Process

1. **Issue**: Create or claim an issue
2. **Branch**: Create a feature branch
3. **Develop**: Implement the feature or fix
4. **Test**: Ensure all tests pass
5. **Document**: Update documentation
6. **Pull Request**: Submit a PR with clear description
7. **Review**: Respond to review feedback
8. **Merge**: Approved PRs are merged

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe tests that verify your changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass
- [ ] I have updated documentation
- [ ] I have checked for security implications
```

## Troubleshooting

Common issues and their solutions:

### Development Environment Issues

**Problem**: Environment initialization fails
**Solution**: Ensure all prerequisites are installed and environment variables are set correctly:
```bash
# Check dependencies
node --version
python --version
cargo --version

# Reinitialize environment
./scripts/flow-tools.sh clean
./scripts/flow-tools.sh init
```

**Problem**: Tests fail unexpectedly
**Solution**: Check for environment inconsistencies or dependency issues:
```bash
# Update dependencies
npm ci

# Clear test cache
npm test -- --clearCache
```

### Integration Issues

**Problem**: Component fails to communicate with other HMS components
**Solution**: Verify connectivity and authentication:
```bash
# Check connectivity
curl -v https://registry.hms.example.com/health

# Verify authentication
./scripts/flow-tools.sh auth check
```

## Support Resources

Additional resources for HMS developers:

- **Documentation**: [HMS-DOC](https://docs.hms.example.com)
- **Issue Tracker**: [GitHub Issues](https://github.com/CodifyHQ/HMS-DEV/issues)
- **Discussion Forum**: [HMS Discussions](https://github.com/CodifyHQ/HMS-DEV/discussions)
- **Slack Channel**: #hms-developers