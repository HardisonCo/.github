# HMS Documentation Generator

## Overview

The HMS Documentation Generator is a standalone tool for creating comprehensive documentation for federal, state, and international agencies that integrate with the HMS system. It creates proper directory structures, handles agency-specific details correctly, and ensures consistent documentation formatting.

## Features

- **Cross-Platform**: Works on Windows, macOS, and Linux with consistent behavior
- **Zero Dependencies**: Uses only standard library modules
- **Agency Type Detection**: Automatically detects and correctly handles federal, state, and international agencies
- **Customizable**: Configurable via JSON configuration files
- **Dry Run Mode**: Preview changes without making them
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Automated Cleanup**: Optional automatic cleanup of old documentation versions

## Installation

No installation required. Just download the script and run it with Python 3.6+.

```bash
# Clone the repository
git clone https://github.com/yourusername/hms-documentation-generator.git
cd hms-documentation-generator

# Make the script executable (Linux/macOS)
chmod +x standalone_generator.py
```

## Usage

```bash
# Generate documentation for a specific agency
python standalone_generator.py --agency "Department of Education"

# Generate documentation for a state agency
python standalone_generator.py --agency "Indiana Department of Education"

# Generate documentation for an international agency
python standalone_generator.py --agency "Australian Department of Finance"

# Generate documentation for all agencies
python standalone_generator.py --agency all

# Use a custom configuration file
python standalone_generator.py --agency all --config my_config.json

# Perform a dry run (show what would be done without making changes)
python standalone_generator.py --agency all --dry-run

# Enable verbose logging
python standalone_generator.py --agency all --verbose
```

## Configuration

The generator can be configured via a JSON configuration file. Default configuration values are provided, but you can override them by creating a `config.json` file in the same directory as the script or by specifying a custom configuration file with the `--config` parameter.

Example configuration file:

```json
{
  "docs_dir": "docs",
  "prefixes": {
    "agency": "HMS-NFO-AGENCY",
    "state": "HMS-NFO-STATE",
    "international": "HMS-NFO-INTL",
    "tutorials": "HMS-NFO-TUTORIALS",
    "use_cases": "HMS-USE-CASES"
  },
  "template_dir": "templates",
  "timestamp_format": "%Y%m%d_%H%M%S",
  "log_level": "INFO",
  "max_component_files": 3,
  "cleanup": {
    "enabled": true,
    "keep_versions": 5
  }
}
```

## Directory Structure

The generator creates the following directory structure:

```
docs/
├── HMS-NFO-AGENCY-{timestamp}/       # Federal agency documentation
├── HMS-NFO-STATE-{timestamp}/        # State agency documentation
├── HMS-NFO-INTL-{timestamp}/         # International agency documentation
├── HMS-NFO-TUTORIALS-{timestamp}/    # Agency tutorials
├── HMS-USE-CASES-{timestamp}/        # Agency use cases
├── HMS-NFO-AGENCY-latest → HMS-NFO-AGENCY-{timestamp}
├── HMS-NFO-STATE-latest → HMS-NFO-STATE-{timestamp}
├── HMS-NFO-INTL-latest → HMS-NFO-INTL-{timestamp}
├── HMS-NFO-TUTORIALS-latest → HMS-NFO-TUTORIALS-{timestamp}
└── HMS-USE-CASES-latest → HMS-USE-CASES-{timestamp}
```

## Error Handling

The generator includes comprehensive error handling to ensure reliable operation:

- **File System Errors**: Proper handling of permissions, file existence, and symlink issues
- **Configuration Errors**: Validation of configuration parameters
- **Input Validation**: Sanitization of file paths and agency names
- **Graceful Fallbacks**: Default values when configuration is missing

## Customization

### Adding New Agency Types

To add support for new agency types, update the `config.json` file to include new prefixes and detection patterns.

### Customizing Templates

Templates can be customized by modifying the `MOCK_TEMPLATES` dictionary in the script or by implementing a template loading mechanism that reads templates from external files.

## Testing

The generator includes a comprehensive test suite to ensure reliable operation. Run the tests with:

```bash
python -m unittest test_standalone_generator.py
```

## Troubleshooting

### Common Issues

- **File Permission Errors**: Ensure you have write permissions for the output directory
- **Symlink Creation Failures**: On Windows, symlink creation requires administrator privileges
- **Agency Type Detection Issues**: If agencies are incorrectly categorized, review the detection patterns in the configuration

### Debugging

Enable verbose logging with the `--verbose` flag for detailed debug information:

```bash
python standalone_generator.py --agency all --verbose
```

Logs are written to `standalone_generator.log` for later review.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b my-new-feature`
3. Make your changes and add tests
4. Test your changes: `python -m unittest test_standalone_generator.py`
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin my-new-feature`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.