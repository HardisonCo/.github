# Paraguay Health System Documentation

This directory contains comprehensive documentation for the integration of Paraguay's healthcare system with the HMS (Health Management System) platform, with a particular focus on the HMS-NFO (Network Foundation Operations) component.

## Documentation Structure

- **Main Documentation**: Located at `docs/International/py-health/`
- **Component-Specific Documentation**: Each HMS component has its own dedicated folder (e.g., `HMS-NFO`, `HMS-EHR`, etc.)
- **Use Case Documentation**: Detailed use case for Paraguay health system integration is in `docs/International/py-health/HMS-NFO/use_case.md`
- **Configuration Files**: System configuration is defined in `docs/International/py-health/config.json`

## Quick Access

For convenience, a symbolic link to the latest Paraguay health documentation is provided at:
`output/paraguay_health_latest`

## Key Components

The documentation covers all HMS components with Paraguay-specific adaptations:

- **HMS-NFO**: Core health information management with Paraguay-specific adaptations
- **HMS-EHR**: Electronic health records tailored to Paraguay's healthcare context
- **HMS-MCP**: Multi-channel platform for diverse healthcare access methods
- **HMS-CUR**: Clinical utilities and resources adapted for Paraguayan healthcare practices
- And all other standard HMS components

## Documentation Generation

Documentation was generated using the following scripts:

1. `generate_py_health_docs.py`: Creates the base documentation structure
2. `run_py_health_docs.sh`: Orchestrates the full documentation generation process

## Special Considerations for Paraguay

The documentation addresses several unique aspects of Paraguay's healthcare system:

1. **Multilingual Support**: Interfaces in Spanish and Guaraní
2. **Geographic Adaptations**: Solutions for both urban and remote rural areas
3. **System Integration**: Connections with MSPBS, IPS, and private providers
4. **Regional Collaboration**: Cross-border health initiatives with neighboring countries

## Use Cases

The detailed use case document covers:

- Integration objectives with Paraguay's healthcare system
- Implementation approach (4 phases)
- Expected outcomes and metrics
- Specific adaptations for Paraguay's healthcare context

## Future Updates

This documentation will be periodically updated as the Paraguay health system implementation progresses. New versions will maintain the same structure but will include additional details on:

- Implementation progress and lessons learned
- Real-world success metrics and case studies
- Adaptations based on field experience
- Enhanced integration with other health systems

## Contact

For questions or additional information about Paraguay health system documentation, please contact the HMS documentation team.

---

*Generated on: May 4, 2025*