# HMS A2A Communication Protocol Specification

## Overview

This document defines the standardized communication protocol for Agent-to-Agent (A2A) interactions in the HMS ecosystem. The protocol builds on the Model Context Protocol (MCP) and extends it with HMS-specific requirements for security, compliance, and comprehensive agent collaboration. This protocol enables all HMS components to communicate through their respective agents in a consistent, secure, and verifiable manner.

## Core Principles

The HMS A2A Communication Protocol follows these core principles:

1. **Standardization**: Common message format and interaction patterns for all agents
2. **Security**: Robust security measures for all communications
3. **Verifiability**: Complete audit trail and verification for all messages
4. **Extensibility**: Flexible format for diverse agent capabilities
5. **Compliance**: Built-in mechanisms for regulatory compliance

## Message Format

The standard message format for all A2A communications is:

```json
{
  "message_id": "msg-uuid",
  "timestamp": "ISO-8601-timestamp",
  "sender": {
    "id": "component-agent-id",
    "type": "government|civilian|component|specialized|sub",
    "capabilities": ["capability1", "capability2"],
    "component": "component-name",
    "domain": "domain-name",
    "specialty": "specialty-name"
  },
  "receiver": {
    "id": "component-agent-id",
    "type": "government|civilian|component|specialized|sub",
    "component": "component-name",
    "domain": "domain-name",
    "specialty": "specialty-name"
  },
  "message_type": "request|response|event|notification",
  "content": {
    "action": "action_name",
    "parameters": {},
    "context": {}
  },
  "security": {
    "signature": "auth-signature",
    "verification_token": "token-value",
    "encryption": "encryption-type",
    "encryption_key_id": "key-id"
  },
  "compliance": {
    "standards": ["standard1", "standard2"],
    "verification_status": "verified|pending|failed",
    "verification_id": "verification-uuid",
    "approved_by": "approver-id"
  },
  "cort": {
    "reasoning_depth": 3,
    "alternatives_considered": 5,
    "confidence": 0.95,
    "verification_steps": ["step1", "step2"],
    "reasoning_trace": "reasoning-trace-id"
  },
  "conversation_id": "conversation-uuid",
  "correlation_id": "correlation-uuid",
  "sequence_number": 1,
  "expires_at": "ISO-8601-timestamp",
  "priority": "high|medium|low",
  "requires_human_review": false
}
```

### Field Definitions

#### Core Message Fields

- **message_id**: Unique identifier for the message (UUID format)
- **timestamp**: ISO-8601 formatted timestamp when the message was created
- **sender**: Information about the message sender
  - **id**: Unique identifier for the sender agent
  - **type**: Type of the sender agent (government, civilian, component, specialized, sub)
  - **capabilities**: List of sender capabilities relevant to the message
  - **component**: Optional component name for component agents
  - **domain**: Optional domain name for specialized agents
  - **specialty**: Optional specialty name for specialized agents
- **receiver**: Information about the message recipient
  - **id**: Unique identifier for the receiver agent
  - **type**: Type of the receiver agent
  - **component**: Optional component name for component agents
  - **domain**: Optional domain name for specialized agents
  - **specialty**: Optional specialty name for specialized agents
- **message_type**: Type of message being sent
  - **request**: Message requesting an action
  - **response**: Message responding to a request
  - **event**: Message broadcasting an event
  - **notification**: Message providing information without requiring response
- **content**: Primary message content
  - **action**: The action to be performed
  - **parameters**: Parameters for the action
  - **context**: Additional context for the action

#### Security Fields

- **security**: Security-related information
  - **signature**: Digital signature of the message content
  - **verification_token**: Token for message verification
  - **encryption**: Encryption type used (if message is encrypted)
  - **encryption_key_id**: Identifier for the encryption key

#### Compliance Fields

- **compliance**: Compliance-related information
  - **standards**: List of standards applicable to this message
  - **verification_status**: Status of compliance verification
  - **verification_id**: Identifier for the verification record
  - **approved_by**: Identifier of the approval entity (if applicable)

#### CoRT Fields

- **cort**: Chain of Recursive Thoughts information
  - **reasoning_depth**: Number of reasoning rounds used
  - **alternatives_considered**: Number of alternatives evaluated
  - **confidence**: Confidence level in the result (0.0-1.0)
  - **verification_steps**: Steps used to verify the reasoning
  - **reasoning_trace**: Identifier for the detailed reasoning trace

#### Coordination Fields

- **conversation_id**: Identifier for the conversation this message belongs to
- **correlation_id**: Identifier for correlated messages
- **sequence_number**: Position of this message in a sequence
- **expires_at**: When this message should be considered expired
- **priority**: Message priority level
- **requires_human_review**: Whether this message requires human review

## Message Types

### Request Message

A message requesting an agent to perform an action:

```json
{
  "message_id": "req-uuid",
  "timestamp": "2025-05-04T10:15:30Z",
  "sender": {
    "id": "hms-api-agent",
    "type": "component",
    "component": "api"
  },
  "receiver": {
    "id": "hms-cdf-agent",
    "type": "component",
    "component": "cdf"
  },
  "message_type": "request",
  "content": {
    "action": "verify_policy",
    "parameters": {
      "policy_text": "...",
      "verification_criteria": ["consistency", "completeness"]
    },
    "context": {
      "policy_domain": "healthcare",
      "urgency": "medium"
    }
  },
  "security": {
    "signature": "...",
    "verification_token": "..."
  },
  "conversation_id": "conv-uuid",
  "sequence_number": 1,
  "priority": "medium"
}
```

### Response Message

A message responding to a request:

```json
{
  "message_id": "resp-uuid",
  "timestamp": "2025-05-04T10:15:35Z",
  "sender": {
    "id": "hms-cdf-agent",
    "type": "component",
    "component": "cdf"
  },
  "receiver": {
    "id": "hms-api-agent",
    "type": "component",
    "component": "api"
  },
  "message_type": "response",
  "content": {
    "action": "verify_policy",
    "parameters": {
      "policy_text": "..."
    },
    "result": {
      "verification_status": "passed",
      "issues": [],
      "recommendations": []
    }
  },
  "security": {
    "signature": "...",
    "verification_token": "..."
  },
  "compliance": {
    "standards": ["fisma", "nist"],
    "verification_status": "verified",
    "verification_id": "ver-uuid"
  },
  "cort": {
    "reasoning_depth": 3,
    "alternatives_considered": 2,
    "confidence": 0.95,
    "reasoning_trace": "trace-uuid"
  },
  "conversation_id": "conv-uuid",
  "correlation_id": "req-uuid",
  "sequence_number": 2
}
```

### Event Message

A message broadcasting an event:

```json
{
  "message_id": "evt-uuid",
  "timestamp": "2025-05-04T10:20:00Z",
  "sender": {
    "id": "hms-gov-agent",
    "type": "component",
    "component": "gov"
  },
  "receiver": {
    "id": "broadcast",
    "type": "broadcast"
  },
  "message_type": "event",
  "content": {
    "action": "policy_updated",
    "parameters": {
      "policy_id": "pol-123",
      "policy_name": "Data Privacy Policy",
      "update_type": "minor"
    },
    "context": {
      "effective_date": "2025-06-01T00:00:00Z"
    }
  },
  "security": {
    "signature": "...",
    "verification_token": "..."
  }
}
```

### Notification Message

A message providing information without requiring a response:

```json
{
  "message_id": "notif-uuid",
  "timestamp": "2025-05-04T10:25:00Z",
  "sender": {
    "id": "hms-mbl-agent",
    "type": "component",
    "component": "mbl"
  },
  "receiver": {
    "id": "hms-api-agent",
    "type": "component",
    "component": "api"
  },
  "message_type": "notification",
  "content": {
    "action": "system_status",
    "parameters": {
      "status": "operational",
      "metrics": {
        "cpu_usage": 0.45,
        "memory_usage": 0.32,
        "request_rate": 120
      }
    }
  },
  "security": {
    "signature": "...",
    "verification_token": "..."
  }
}
```

## Communication Patterns

The protocol supports several communication patterns:

### Request-Response Pattern

The most common pattern for point-to-point communication:

1. **Requester** sends a request message to a **Responder**
2. **Responder** processes the request and sends a response message
3. **Requester** receives and processes the response

```
Requester                    Responder
    |                            |
    |------- Request ----------->|
    |                            |
    |<------ Response -----------|
    |                            |
```

### Broadcast Pattern

For distributing information to multiple agents:

1. **Publisher** sends an event message to the "broadcast" receiver
2. **A2A Protocol Layer** distributes the message to all registered **Subscribers**
3. **Subscribers** process the event message

```
Publisher                    A2A Protocol Layer                 Subscribers
    |                               |                                |
    |------- Event --------------->|------ Event ------------------>|
    |                               |                                |
    |                               |------ Event ------------------>|
    |                               |                                |
    |                               |------ Event ------------------>|
    |                               |                                |
```

### Notification Pattern

For sending information to a specific agent without requiring a response:

1. **Notifier** sends a notification message to a **Recipient**
2. **Recipient** processes the notification without responding

```
Notifier                     Recipient
    |                            |
    |------- Notification ------>|
    |                            |
```

### Conversation Pattern

For multi-message interactions using a shared conversation ID:

1. **Agent A** initiates a conversation with a request message
2. **Agent B** responds with a response message
3. **Agent A** sends a follow-up request
4. **Agent B** responds with a follow-up response
5. The conversation continues until completion

```
Agent A                      Agent B
    |                            |
    |------- Request 1 --------->|
    |                            |
    |<------ Response 1 ----------|
    |                            |
    |------- Request 2 --------->|
    |                            |
    |<------ Response 2 ----------|
    |                            |
```

### Multi-Agent Conversation Pattern

For complex interactions involving multiple agents:

1. **Coordinator** initiates a conversation
2. **Participants** respond and interact
3. The conversation continues until completion

```
Coordinator             Participant A             Participant B
    |                        |                         |
    |------ Request -------->|                         |
    |                        |                         |
    |<----- Response --------|                         |
    |                        |                         |
    |------ Request ----------------------------------->|
    |                        |                         |
    |<----- Response -----------------------------------|
    |                        |                         |
    |------ Event ---------->|------------ Event ----->|
    |                        |                         |
```

## Message Serialization

Messages are serialized as JSON for transmission. For binary data, Base64 encoding is used within the JSON structure.

## Message Validation

All messages must undergo validation before processing:

1. **Format Validation**: Ensuring the message structure is correct
2. **Schema Validation**: Ensuring all required fields are present
3. **Signature Validation**: Verifying the message signature
4. **Content Validation**: Validating the message content is appropriate

## Security Implementation

### Message Signing

All messages must be signed by the sender:

1. Compute a hash of the message content (excluding the signature field)
2. Sign the hash with the sender's private key
3. Include the signature in the message

### Verification Tokens

Each message includes a verification token:

1. Generate a unique token for the message
2. Include the token in the message
3. Verify the token upon receipt

### Message Encryption

Sensitive messages can be encrypted:

1. Generate a symmetric encryption key
2. Encrypt the message content with the key
3. Encrypt the symmetric key with the receiver's public key
4. Include the encrypted key and encrypted content in the message

## A2A Server Implementation

The A2A server manages message routing and delivery:

```
┌─────────────────────────────────────────────────────────────┐
│                        A2A Server                            │
│                                                             │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│   │Message Router │  │ Agent Registry│  │Message Queue  │   │
│   └───────┬───────┘  └──────┬────────┘  └───────┬───────┘   │
│           │                 │                   │           │
│           └─────────────────┼───────────────────┘           │
│                             │                               │
└─────────────────────────────┼───────────────────────────────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
┌───▼───────────┐      ┌──────▼─────────┐      ┌───────▼───────┐
│ Component A   │      │ Component B    │      │ Component C   │
│    Agent      │      │    Agent       │      │    Agent      │
└───────────────┘      └────────────────┘      └───────────────┘
```

### Message Router

The Message Router is responsible for:

1. Receiving incoming messages
2. Validating message format and signature
3. Determining the appropriate recipient(s)
4. Delivering the message to the recipient(s)
5. Handling message routing errors

### Agent Registry

The Agent Registry maintains:

1. List of all registered agents
2. Agent capabilities
3. Agent public keys
4. Agent status (active/inactive)

### Message Queue

The Message Queue manages:

1. Message persistence for reliability
2. Message delivery retries
3. Message prioritization
4. Message expiration

## A2A Client Implementation

Each agent implements an A2A client:

```python
class A2AClient:
    """Client for A2A communication."""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        private_key_path: str,
        server_url: str,
        component: str = None,
        domain: str = None,
        specialty: str = None
    ):
        """Initialize the A2A client.
        
        Args:
            agent_id: Agent identifier
            agent_type: Type of agent
            private_key_path: Path to private key file
            server_url: URL of the A2A server
            component: Optional component name
            domain: Optional domain name
            specialty: Optional specialty name
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.component = component
        self.domain = domain
        self.specialty = specialty
        self.server_url = server_url
        
        # Load private key
        with open(private_key_path, 'rb') as key_file:
            self.private_key = load_pem_private_key(
                key_file.read(),
                password=None
            )
        
        # Initialize capabilities
        self.capabilities = []
        
        # Initialize message handlers
        self.message_handlers = {}
        
        # Initialize conversation tracking
        self.conversations = {}
        
    def register_capability(self, capability: str) -> None:
        """Register a capability.
        
        Args:
            capability: Capability to register
        """
        if capability not in self.capabilities:
            self.capabilities.append(capability)
        
    def register_message_handler(self, action: str, handler: Callable) -> None:
        """Register a message handler.
        
        Args:
            action: Action to handle
            handler: Handler function
        """
        self.message_handlers[action] = handler
        
    def send_request(
        self,
        receiver_id: str,
        action: str,
        parameters: Dict[str, Any],
        context: Dict[str, Any] = None,
        conversation_id: str = None,
        priority: str = "medium",
        requires_human_review: bool = False,
        standards: List[str] = None
    ) -> Dict[str, Any]:
        """Send a request message.
        
        Args:
            receiver_id: Receiver agent ID
            action: Action to request
            parameters: Action parameters
            context: Optional context
            conversation_id: Optional conversation ID
            priority: Message priority
            requires_human_review: Whether human review is required
            standards: Applicable standards
            
        Returns:
            Response message
        """
        # Create request message
        message = self._create_message(
            message_type="request",
            receiver_id=receiver_id,
            content={
                "action": action,
                "parameters": parameters,
                "context": context or {}
            },
            conversation_id=conversation_id,
            priority=priority,
            requires_human_review=requires_human_review,
            standards=standards
        )
        
        # Sign message
        message = self._sign_message(message)
        
        # Send message
        response = self._send_message(message)
        
        # Store in conversation tracking
        if conversation_id:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            self.conversations[conversation_id].append({
                "type": "request",
                "message_id": message["message_id"],
                "timestamp": message["timestamp"],
                "action": action
            })
        
        return response
        
    def send_response(
        self,
        receiver_id: str,
        request_message_id: str,
        action: str,
        result: Dict[str, Any],
        conversation_id: str = None,
        cort_data: Dict[str, Any] = None,
        standards: List[str] = None
    ) -> None:
        """Send a response message.
        
        Args:
            receiver_id: Receiver agent ID
            request_message_id: ID of the request message
            action: Action to respond to
            result: Result of the action
            conversation_id: Optional conversation ID
            cort_data: Optional CoRT data
            standards: Applicable standards
        """
        # Create response message
        message = self._create_message(
            message_type="response",
            receiver_id=receiver_id,
            content={
                "action": action,
                "result": result
            },
            conversation_id=conversation_id,
            correlation_id=request_message_id,
            cort_data=cort_data,
            standards=standards
        )
        
        # Sign message
        message = self._sign_message(message)
        
        # Send message
        self._send_message(message)
        
        # Store in conversation tracking
        if conversation_id and conversation_id in self.conversations:
            self.conversations[conversation_id].append({
                "type": "response",
                "message_id": message["message_id"],
                "timestamp": message["timestamp"],
                "action": action,
                "request_message_id": request_message_id
            })
        
    def send_event(
        self,
        event_type: str,
        parameters: Dict[str, Any],
        context: Dict[str, Any] = None,
        standards: List[str] = None
    ) -> None:
        """Send an event message.
        
        Args:
            event_type: Type of event
            parameters: Event parameters
            context: Optional context
            standards: Applicable standards
        """
        # Create event message
        message = self._create_message(
            message_type="event",
            receiver_id="broadcast",
            content={
                "action": event_type,
                "parameters": parameters,
                "context": context or {}
            },
            standards=standards
        )
        
        # Sign message
        message = self._sign_message(message)
        
        # Send message
        self._send_message(message)
        
    def send_notification(
        self,
        receiver_id: str,
        notification_type: str,
        parameters: Dict[str, Any],
        context: Dict[str, Any] = None,
        standards: List[str] = None
    ) -> None:
        """Send a notification message.
        
        Args:
            receiver_id: Receiver agent ID
            notification_type: Type of notification
            parameters: Notification parameters
            context: Optional context
            standards: Applicable standards
        """
        # Create notification message
        message = self._create_message(
            message_type="notification",
            receiver_id=receiver_id,
            content={
                "action": notification_type,
                "parameters": parameters,
                "context": context or {}
            },
            standards=standards
        )
        
        # Sign message
        message = self._sign_message(message)
        
        # Send message
        self._send_message(message)
        
    def start_conversation(
        self,
        participants: List[str]
    ) -> str:
        """Start a new conversation.
        
        Args:
            participants: List of participant agent IDs
            
        Returns:
            Conversation ID
        """
        conversation_id = str(uuid.uuid4())
        
        self.conversations[conversation_id] = []
        
        # Notify participants
        for participant in participants:
            self.send_notification(
                receiver_id=participant,
                notification_type="conversation_started",
                parameters={
                    "conversation_id": conversation_id,
                    "participants": participants
                }
            )
        
        return conversation_id
        
    def receive_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Receive and process a message.
        
        Args:
            message: Message to process
            
        Returns:
            Processing result
        """
        # Verify message signature
        if not self._verify_message(message):
            return {
                "status": "error",
                "error": "Invalid message signature"
            }
        
        # Extract message details
        message_type = message["message_type"]
        content = message["content"]
        action = content["action"]
        
        # Store in conversation tracking
        conversation_id = message.get("conversation_id")
        if conversation_id:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            self.conversations[conversation_id].append({
                "type": message_type,
                "message_id": message["message_id"],
                "timestamp": message["timestamp"],
                "action": action,
                "sender_id": message["sender"]["id"]
            })
        
        # Process based on message type
        if message_type == "request":
            return self._process_request(message)
        elif message_type == "response":
            return self._process_response(message)
        elif message_type == "event":
            return self._process_event(message)
        elif message_type == "notification":
            return self._process_notification(message)
        else:
            return {
                "status": "error",
                "error": f"Unknown message type: {message_type}"
            }
        
    def _create_message(
        self,
        message_type: str,
        receiver_id: str,
        content: Dict[str, Any],
        conversation_id: str = None,
        correlation_id: str = None,
        priority: str = "medium",
        requires_human_review: bool = False,
        cort_data: Dict[str, Any] = None,
        standards: List[str] = None,
        sequence_number: int = None
    ) -> Dict[str, Any]:
        """Create a message.
        
        Args:
            message_type: Type of message
            receiver_id: Receiver agent ID
            content: Message content
            conversation_id: Optional conversation ID
            correlation_id: Optional correlation ID
            priority: Message priority
            requires_human_review: Whether human review is required
            cort_data: Optional CoRT data
            standards: Applicable standards
            sequence_number: Optional sequence number
            
        Returns:
            Created message
        """
        # Create receiver information
        if receiver_id == "broadcast":
            receiver = {
                "id": "broadcast",
                "type": "broadcast"
            }
        else:
            # In a real implementation, we would look up receiver details
            receiver = {
                "id": receiver_id,
                "type": "unknown"
            }
        
        # Create sender information
        sender = {
            "id": self.agent_id,
            "type": self.agent_type,
            "capabilities": self.capabilities
        }
        
        if self.component:
            sender["component"] = self.component
        if self.domain:
            sender["domain"] = self.domain
        if self.specialty:
            sender["specialty"] = self.specialty
            
        # Create message
        message = {
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message_type": message_type,
            "content": content,
            "security": {
                "signature": None,
                "verification_token": str(uuid.uuid4())
            }
        }
        
        # Add optional fields
        if conversation_id:
            message["conversation_id"] = conversation_id
            
            # Determine sequence number if not provided
            if sequence_number is None and conversation_id in self.conversations:
                sequence_number = len(self.conversations[conversation_id]) + 1
                
        if correlation_id:
            message["correlation_id"] = correlation_id
            
        if sequence_number is not None:
            message["sequence_number"] = sequence_number
            
        if priority:
            message["priority"] = priority
            
        if requires_human_review:
            message["requires_human_review"] = True
            
        if cort_data:
            message["cort"] = cort_data
            
        if standards:
            message["compliance"] = {
                "standards": standards,
                "verification_status": "pending"
            }
            
        return message
        
    def _sign_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Sign a message.
        
        Args:
            message: Message to sign
            
        Returns:
            Signed message
        """
        # Create a copy without the signature
        message_copy = copy.deepcopy(message)
        message_copy["security"]["signature"] = None
        
        # Serialize the message
        message_json = json.dumps(message_copy, sort_keys=True)
        
        # Compute the signature
        signature = self.private_key.sign(
            message_json.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Add the signature
        message["security"]["signature"] = base64.b64encode(signature).decode('utf-8')
        
        return message
        
    def _verify_message(self, message: Dict[str, Any]) -> bool:
        """Verify a message signature.
        
        Args:
            message: Message to verify
            
        Returns:
            True if signature is valid, False otherwise
        """
        # Get the signature
        signature = message["security"]["signature"]
        if not signature:
            return False
            
        # Create a copy without the signature
        message_copy = copy.deepcopy(message)
        message_copy["security"]["signature"] = None
        
        # Serialize the message
        message_json = json.dumps(message_copy, sort_keys=True)
        
        # Get the sender's public key
        sender_id = message["sender"]["id"]
        public_key = self._get_public_key(sender_id)
        if not public_key:
            return False
            
        # Verify the signature
        try:
            public_key.verify(
                base64.b64decode(signature),
                message_json.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
            
    def _get_public_key(self, agent_id: str) -> Any:
        """Get the public key for an agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Public key or None if not found
        """
        # In a real implementation, this would look up the public key
        # For now, return a dummy key for testing
        return None
        
    def _send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to the A2A server.
        
        Args:
            message: Message to send
            
        Returns:
            Response from the server
        """
        # In a real implementation, this would send the message to the server
        # For now, log the message and return a dummy response
        print(f"Sending {message['message_type']} to {message['receiver']['id']}")
        
        if message["message_type"] == "request":
            # For requests, we expect a response
            return {
                "status": "success",
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "sender": {
                    "id": message["receiver"]["id"],
                    "type": message["receiver"]["type"]
                },
                "receiver": {
                    "id": message["sender"]["id"],
                    "type": message["sender"]["type"]
                },
                "message_type": "response",
                "content": {
                    "action": message["content"]["action"],
                    "result": {"status": "success"}
                },
                "correlation_id": message["message_id"]
            }
        else:
            # For other message types, we just return success
            return {"status": "success"}
            
    def _process_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request message.
        
        Args:
            message: Request message
            
        Returns:
            Processing result
        """
        content = message["content"]
        action = content["action"]
        parameters = content.get("parameters", {})
        context = content.get("context", {})
        
        # Check if we have a handler for this action
        if action in self.message_handlers:
            handler = self.message_handlers[action]
            
            try:
                # Call the handler
                result = handler(parameters, context)
                
                # Send a response
                self.send_response(
                    receiver_id=message["sender"]["id"],
                    request_message_id=message["message_id"],
                    action=action,
                    result=result,
                    conversation_id=message.get("conversation_id")
                )
                
                return {
                    "status": "success",
                    "result": result
                }
            except Exception as e:
                # Send an error response
                self.send_response(
                    receiver_id=message["sender"]["id"],
                    request_message_id=message["message_id"],
                    action=action,
                    result={
                        "status": "error",
                        "error": str(e)
                    },
                    conversation_id=message.get("conversation_id")
                )
                
                return {
                    "status": "error",
                    "error": str(e)
                }
        else:
            # No handler for this action
            self.send_response(
                receiver_id=message["sender"]["id"],
                request_message_id=message["message_id"],
                action=action,
                result={
                    "status": "error",
                    "error": f"Unknown action: {action}"
                },
                conversation_id=message.get("conversation_id")
            )
            
            return {
                "status": "error",
                "error": f"Unknown action: {action}"
            }
            
    def _process_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process a response message.
        
        Args:
            message: Response message
            
        Returns:
            Processing result
        """
        # Nothing to do for responses, as they're handled by the request sender
        return {
            "status": "success"
        }
        
    def _process_event(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an event message.
        
        Args:
            message: Event message
            
        Returns:
            Processing result
        """
        content = message["content"]
        action = content["action"]
        parameters = content.get("parameters", {})
        context = content.get("context", {})
        
        # Check if we have a handler for this action
        if action in self.message_handlers:
            handler = self.message_handlers[action]
            
            try:
                # Call the handler
                result = handler(parameters, context)
                
                return {
                    "status": "success",
                    "result": result
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
        else:
            # No handler for this action
            return {
                "status": "success",
                "result": {
                    "status": "ignored",
                    "reason": f"No handler for event: {action}"
                }
            }
            
    def _process_notification(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process a notification message.
        
        Args:
            message: Notification message
            
        Returns:
            Processing result
        """
        content = message["content"]
        action = content["action"]
        parameters = content.get("parameters", {})
        context = content.get("context", {})
        
        # Check if we have a handler for this action
        if action in self.message_handlers:
            handler = self.message_handlers[action]
            
            try:
                # Call the handler
                result = handler(parameters, context)
                
                return {
                    "status": "success",
                    "result": result
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
        else:
            # No handler for this action
            return {
                "status": "success",
                "result": {
                    "status": "ignored",
                    "reason": f"No handler for notification: {action}"
                }
            }
```

## Integration with HMS-A2A Component

The communication protocol integrates with the HMS-A2A component:

1. **Protocol Implementation**: HMS-A2A implements the core protocol
2. **Server Management**: HMS-A2A manages the A2A server
3. **Client Library**: HMS-A2A provides the A2A client library
4. **MCP Compatibility**: HMS-A2A ensures compatibility with MCP
5. **Deal Framework**: HMS-A2A integrates the protocol with deal framework

## Agent Registration Process

Agents must register with the A2A server to communicate:

1. **Identity Creation**: Generate unique agent identity
2. **Key Generation**: Create cryptographic key pair
3. **Capability Declaration**: Declare agent capabilities
4. **Registration Request**: Submit registration to A2A server
5. **Verification**: Server verifies agent identity and capabilities
6. **Approval**: Server approves registration
7. **Certificate Issuance**: Server issues communication certificate

## Message Routing and Delivery

Messages are routed and delivered based on receiver information:

1. **Receiver Lookup**: A2A server looks up the receiver agent
2. **Capability Check**: Server verifies receiver can handle the message
3. **Access Control**: Server checks sender has permission to contact receiver
4. **Message Delivery**: Server delivers message to receiver
5. **Delivery Confirmation**: Server confirms successful delivery
6. **Retry Mechanism**: Server retries delivery for transient failures
7. **Failure Handling**: Server handles permanent delivery failures

## Error Handling

The protocol defines standard error handling:

1. **Message Format Errors**: Errors in message structure
2. **Validation Errors**: Errors in message validation
3. **Delivery Errors**: Errors in message delivery
4. **Processing Errors**: Errors in message processing
5. **Timeout Errors**: Errors due to response timeouts

Error responses include:

```json
{
  "message_id": "err-uuid",
  "timestamp": "2025-05-04T10:30:00Z",
  "sender": {
    "id": "hms-a2a-server",
    "type": "system"
  },
  "receiver": {
    "id": "hms-api-agent",
    "type": "component",
    "component": "api"
  },
  "message_type": "response",
  "content": {
    "action": "error",
    "error": {
      "type": "validation_error",
      "message": "Invalid message format",
      "details": {
        "field": "content.parameters",
        "issue": "Required field missing"
      }
    }
  },
  "correlation_id": "req-uuid"
}
```

## A2A Protocol Extensions

The base protocol can be extended for specialized needs:

### Deal Framework Extension

For implementing deal-based collaboration:

```json
{
  "message_id": "deal-uuid",
  "timestamp": "2025-05-04T11:00:00Z",
  "sender": {
    "id": "hms-mbl-agent",
    "type": "component",
    "component": "mbl"
  },
  "receiver": {
    "id": "hms-cdf-agent",
    "type": "component",
    "component": "cdf"
  },
  "message_type": "request",
  "content": {
    "action": "create_deal",
    "parameters": {
      "deal_name": "Economic Impact Analysis",
      "deal_type": "analysis",
      "participants": ["hms-mbl-agent", "hms-cdf-agent", "hms-nfo-agent"],
      "problem": {
        "description": "Analyze economic impact of proposed policy",
        "parameters": {
          "policy_id": "pol-123",
          "analysis_type": "full",
          "timeframe": "5-year"
        }
      }
    }
  },
  "deal_framework": {
    "deal_id": "deal-uuid",
    "deal_stage": "initiation",
    "deal_role": "initiator",
    "deal_value": {
      "value_type": "analysis",
      "value_metric": "accuracy"
    }
  },
  "security": {
    "signature": "...",
    "verification_token": "..."
  },
  "conversation_id": "conv-uuid"
}
```

### CoRT Extension

For detailed Chain of Recursive Thoughts integration:

```json
{
  "message_id": "cort-uuid",
  "timestamp": "2025-05-04T11:30:00Z",
  "sender": {
    "id": "hms-cdf-agent",
    "type": "component",
    "component": "cdf"
  },
  "receiver": {
    "id": "hms-mbl-agent",
    "type": "component",
    "component": "mbl"
  },
  "message_type": "response",
  "content": {
    "action": "analyze_policy_impact",
    "result": {
      "impact_assessment": {
        "economic_impact": {
          "gdp_change": 0.03,
          "employment_change": 0.02,
          "confidence": 0.92
        },
        "social_impact": {
          "equity_change": 0.04,
          "confidence": 0.87
        }
      }
    }
  },
  "cort": {
    "reasoning_depth": 3,
    "alternatives_considered": 5,
    "confidence": 0.95,
    "verification_steps": ["economic_model_validation", "consistency_check"],
    "reasoning_trace": {
      "rounds": [
        {
          "round": 1,
          "thoughts": [
            {
              "thought_id": "t1",
              "content": "Initial economic impact assessment based on policy parameters",
              "confidence": 0.75
            },
            {
              "thought_id": "t2",
              "content": "Consideration of alternative economic models",
              "confidence": 0.80
            },
            {
              "thought_id": "t3",
              "content": "Analysis of comparable historical policies",
              "confidence": 0.70
            }
          ],
          "selected": "t2"
        },
        {
          "round": 2,
          "thoughts": [
            {
              "thought_id": "t4",
              "content": "Refined impact assessment using optimal economic model",
              "confidence": 0.85
            },
            {
              "thought_id": "t5",
              "content": "Cross-validation with additional data sources",
              "confidence": 0.90
            }
          ],
          "selected": "t5"
        },
        {
          "round": 3,
          "thoughts": [
            {
              "thought_id": "t6",
              "content": "Final impact assessment with uncertainty quantification",
              "confidence": 0.95
            }
          ],
          "selected": "t6"
        }
      ]
    }
  },
  "security": {
    "signature": "...",
    "verification_token": "..."
  },
  "correlation_id": "req-uuid",
  "conversation_id": "conv-uuid"
}
```

## A2A Protocol Management

The protocol is managed by the HMS-A2A component:

1. **Protocol Documentation**: Comprehensive documentation
2. **Protocol Versioning**: Versioned protocol specifications
3. **Protocol Compatibility**: Backward compatibility mechanisms
4. **Protocol Extensions**: Standardized extension process
5. **Protocol Governance**: Clear governance process

## Conclusion

The HMS A2A Communication Protocol provides a standardized, secure, and verifiable communication mechanism for all agents in the HMS ecosystem. By building on the Model Context Protocol and extending it with HMS-specific requirements, the protocol enables robust agent collaboration while ensuring security, compliance, and reliability.

The protocol's flexible design accommodates diverse agent types and communication patterns, from simple request-response interactions to complex multi-agent conversations. The integrated security mechanisms ensure that all communications are authenticated, authorized, and protected against tampering.

By implementing this protocol, HMS components can communicate through their respective agents in a consistent and reliable manner, enabling the creation of a powerful, integrated agent ecosystem across the entire HMS platform.