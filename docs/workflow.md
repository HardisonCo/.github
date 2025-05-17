# HMS-DEV Workflow Guide

This document describes the official workflow process for HMS component development. It covers the structured development approach, verification process, and workflow tools available in the HMS-DEV system.

## Workflow Model

The HMS workflow follows a structured 10-phase development cycle that ensures consistent quality and integration across components:

### 1. **Discovery Phase**
- Understand requirements
- Analyze existing components
- Define integration points
- Create user stories

### 2. **Specification Phase**
- Draft technical specifications
- Define API contracts
- Create component diagrams
- Establish verification criteria

### 3. **Design Phase**
- Architecture design
- Component structure
- Data flow mapping
- Security considerations

### 4. **Development Phase**
- Implementation
- Unit testing
- Documentation
- Code reviews

### 5. **Verification Phase**
- Component testing
- Integration testing
- Security validation
- Performance testing

### 6. **Integration Phase**
- System integration
- Cross-component testing
- API conformance testing
- Error handling validation

### 7. **Deployment Phase**
- Environment preparation
- Deployment execution
- Health checks
- Rollback procedures

### 8. **Monitoring Phase**
- Metric collection
- Performance analysis
- Error tracking
- Usage monitoring

### 9. **Improvement Phase**
- Analyze feedback
- Identify optimizations
- Plan improvements
- Update documentation

### 10. **Release Phase**
- Version finalization
- Release notes
- User documentation
- Component announcement

## Pomodoro-Based Workflow

The HMS development process follows a modified Pomodoro technique:

### 60-Minute Session Structure

Each 60-minute development session is structured as:

1. **Discovery (15 minutes)**
   - Review requirements
   - Understand existing code
   - Plan implementation approach

2. **Specs (10 minutes)**
   - Define acceptance criteria
   - Create implementation plan
   - Identify potential challenges

3. **Coding (25 minutes)**
   - Focused implementation time
   - No interruptions
   - Commit small, focused changes

4. **Verification (5 minutes)**
   - Run tests
   - Check code quality
   - Ensure documentation

5. **Reflection (5 minutes)**
   - Review progress
   - Update journal
   - Plan next steps

### Between Sessions

- Background supervisor reviews completed work
- Improvement tickets may be generated
- Next session prioritization occurs

## GitFlow Integration

HMS-DEV uses a modified GitFlow workflow:

### Branch Types

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: New features or enhancements
- **release/**: Preparing for a new release
- **hotfix/**: Emergency fixes for production

### Feature Development Workflow

1. Create a feature branch from develop
   ```bash
   ./scripts/flow-tools.sh feature start feature-name
   ```

2. Work in Pomodoro sessions
   ```bash
   ./scripts/flow-tools.sh session start
   ```

3. Complete the feature and merge to develop
   ```bash
   ./scripts/flow-tools.sh feature finish
   ```

## Developer Verification System

HMS-DEV requires all developers to complete verification:

### Verification Process

1. **Trivia Quiz**: Answer questions about HMS architecture and principles
2. **Component Understanding**: Demonstrate knowledge of specific components
3. **Security Advisory**: Review and acknowledge security guidelines

### Verification Command

```bash
./scripts/flow-tools.sh verify
```

### Verification Token

- Generated upon successful verification
- Valid for 30 days
- Required for committing code

## CoRT Supervisor Integration

The workflow integrates with the Chain of Recursive Thoughts (CoRT) supervisor:

### Agent Journal

During each Pomodoro session, developers (or agents) maintain a journal:

```markdown
## Decisions
- Decision 1: Selected X approach because Y
- Decision 2: Used library Z for feature F

## Blockers
- Blocker 1: API documentation is incomplete
- Blocker 2: Integration with component X is unclear
```

### Improvement Tickets

The CoRT supervisor analyzes journals and generates improvement tickets:

```markdown
Ticket ID: IMP-123
Title: Improve error handling in API client
Acceptance Criteria:
- Add comprehensive error types
- Implement retry logic
- Document error handling patterns
Assigned To: Agent-X
Priority: Medium
```

## Workflow Tools Usage

The `flow-tools.sh` script provides commands for managing the workflow:

### Session Management

```bash
# Start a Pomodoro session
./scripts/flow-tools.sh session start

# End a session and log progress
./scripts/flow-tools.sh session end

# Pause a session
./scripts/flow-tools.sh session pause

# Resume a session
./scripts/flow-tools.sh session resume
```

### Feature Management

```bash
# Start a new feature
./scripts/flow-tools.sh feature start feature-name

# Finish a feature
./scripts/flow-tools.sh feature finish

# List all features
./scripts/flow-tools.sh feature list
```

### Release Management

```bash
# Start a release
./scripts/flow-tools.sh release start v1.0.0

# Finish a release
./scripts/flow-tools.sh release finish
```

### Verification

```bash
# Start verification process
./scripts/flow-tools.sh verify

# Check verification status
./scripts/flow-tools.sh verify status
```

### Agent Management

```bash
# Register a new agent
./scripts/flow-tools.sh agent register agent-name

# Assign a task to an agent
./scripts/flow-tools.sh agent assign agent-name task-id

# Check agent status
./scripts/flow-tools.sh agent status agent-name
```

## Integration with Other HMS Components

The workflow tools integrate with other HMS components:

- **HMS-A2A**: Task delegation and agent communication
- **HMS-DOC**: Automatic documentation generation
- **HMS-MCP**: Verification task execution
-- **Registry Service**: Tool discovery and integration

## Developer Profiles

The HMS-DEV system uses root-level configuration files to synchronize human and agent developers:

- **ARION.md** – Defines the Arion persona, responsibilities, and sync guidelines.
- **EUGENE.md** – Defines the Eugene persona, responsibilities, and sync guidelines.

Ensure these files are kept up-to-date as part of the development workflow.