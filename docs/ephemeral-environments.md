# HMS Ephemeral Development Environments

## Overview

HMS employs ephemeral development environments using Nix to ensure consistent, reproducible development experiences across all components. These environments are:

- **Component-specific**: Tailored to HMS-SME, HMS-ESR, HMS-DEV, or HMS-SYS needs
- **Isolated**: Each PR or branch gets its own clean environment
- **Ephemeral**: Automatically provisioned and cleaned up
- **Reproducible**: Same environment on every machine via Nix
- **Self-destructing**: Auto-cleanup after configurable timeframe

## Prerequisites

- Nix package manager installed (`curl -L https://nixos.org/nix/install | sh`)
- Git
- For GitHub Actions integration: self-hosted runner with Nix

## Usage

### Manual Provisioning

Create an ephemeral environment for a specific component and branch:

```bash
./SYSTEM-COMPONENTS/HMS-SYS/provision-env.sh --component hms-sme --branch feature/new-feature
```

Create an environment from a specific PR:

```bash
./SYSTEM-COMPONENTS/HMS-SYS/provision-env.sh --component hms-dev --pr 123
```

Set auto-cleanup timeout:

```bash
./SYSTEM-COMPONENTS/HMS-SYS/provision-env.sh --component all --pr 123 --timeout 8h
```

### Using Provisioned Environments

After provisioning, you'll receive instructions with the environment location. To use it:

1. Navigate to the environment directory:
   ```bash
   cd /path/to/temp_envs/YYYYMMDD_HHMMSS_hms-sme_feature_branch
   ```

2. Launch the environment:
   ```bash
   ./launch.sh
   ```

3. When done, clean up:
   ```bash
   ./cleanup.sh
   ```

### Automatic PR Environments

When a PR is submitted, the system automatically:

1. Determines which component(s) are affected based on changed files
2. Provisions appropriate environments for each affected component
3. Comments on the PR with environment locations and usage instructions
4. Sets a 24-hour auto-cleanup timer

## Configuration

### Nix Environment Configuration

The `hms-env.nix` file defines environment configurations for each component, including:

- Common development tools
- Component-specific dependencies
- Environment variables
- Shell hooks for component setup

You can override the default environment variables by editing the `componentEnvVars` section in `hms-env.nix`.

### Component-Specific Features

- **HMS-SME**: Ruby, Rails, PostgreSQL
- **HMS-ESR**: Ruby, custom ESR config
- **HMS-DEV**: Node.js, TypeScript, Rust
- **HMS-SYS**: Rust, Clang, Protobuf, LLVM

### Environment Variables

Each component gets specific environment variables:

```bash
# Example for HMS-DEV
export HMS_COMPONENT="HMS-DEV"
export NODE_ENV="development"
export HMS_DEV_ROOT="$PWD"

# All components get access to root cause DB
export HMS_ROOT_CAUSE_DB="$PWD/data/root_cause.json"
```

## Integration with Bug Resolution Process

The ephemeral environments are integrated with the bug resolution workflow:

1. When a bug is reported, the triage bot assigns it to the appropriate team
2. HMS-SYS automatically provisions an environment for the affected component
3. The environment includes the root cause database for quick reference
4. Developers can test fixes in isolation without affecting their primary workspaces
5. After PR merge, the environment is automatically cleaned up

This integration significantly reduces the "time to first keystroke" for bug fixes and ensures consistent environments when testing fixes.

## Troubleshooting

### Common Issues

1. **Environment fails to launch**:
   - Check Nix installation: `nix --version`
   - Ensure you have read permissions for the environment directory

2. **Missing dependencies**:
   - Edit `hms-env.nix` to add required packages
   - Re-launch the environment

3. **Auto-cleanup occurred too early**:
   - Provision a new environment with a longer timeout: `--timeout 48h`

## Future Enhancements

1. Integration with container-based workflows (Docker, Kubernetes)
2. Cached dependency downloads for faster environment setup
3. Remote development environment provisioning for distributed teams 