# Chapter 1: Core System Platform (HMS-SYS)

Welcome to HMS-NFO! In this chapter, we’ll explore **HMS-SYS**, the foundational “infrastructure backbone” that makes every other module in our system run smoothly—just like electricity, water, and HVAC in a government building.

---

## 1. Motivation: Why HMS-SYS Matters

Imagine the Office of Postsecondary Education (OPE) is collecting grant applications from schools across the country. They need:

1. **Reliable storage** for each application form.  
2. **Secure message passing** so one system can notify another when a form is submitted.  
3. **Global configuration** for things like database URLs or SMTP servers.  

Without a solid backbone, each microservice would reinvent these utilities, leading to broken “plumbing,” misrouted messages, or mismatched settings. HMS-SYS solves these problems once and for all.

---

## 2. Key Concepts

HMS-SYS provides three main services:

1. **Database Service**  
   - Acts like a secure filing cabinet to store and retrieve data.  
2. **Messaging Bus**  
   - Works like an internal mailroom to pass notifications or events between modules.  
3. **Configuration Service**  
   - Serves as the central thermostat and breaker box, holding environment settings and feature flags.

---

## 3. Using HMS-SYS: A Simple Workflow

Let’s walk through a minimal example: submitting a grant application form.

### 3.1 Store the Application

```python
# 1. Connect to the database
from hms_sys.db import HMSDatabase
db = HMSDatabase.connect("app_db")

# 2. Save the application
application = {
    "applicant": "State University",
    "program": "STEM Grant 2024",
    "amount_requested": 500000
}
record = db.save("grant_applications", application)
# record => {"id": 123, "status": "saved"}
```
After calling `save`, you get back a record ID. This is like putting a folder into a filing cabinet drawer and getting its drawer number.

### 3.2 Publish a Submission Event

```python
# 1. Connect to the messaging bus
from hms_sys.bus import HMSBus
bus = HMSBus.connect()

# 2. Publish an event
event = {"application_id": record["id"], "status": "submitted"}
bus.publish("application.submitted", event)
```
This is like dropping a memo in the internal mailroom so the “Notification Service” or “Review Service” can pick it up.

### 3.3 Load Global Configuration

```python
from hms_sys.config import ConfigService

# Fetch SMTP settings for email notifications
smtp_config = ConfigService.get("email.smtp_server")
# smtp_config => "smtp.ope.gov:587"
```
Think of this as checking the breaker box for the right voltage before plugging in a device.

---

## 4. Under the Hood: What Happens Step-by-Step

Here’s a simplified sequence of calls during our “submit application” flow:

```mermaid
sequenceDiagram
  participant App as GrantApp
  participant Config as ConfigSvc
  participant DB as DB Service
  participant Bus as Msg Bus

  App->>Config: get("db_connection")
  Config-->>App: "postgres://..."
  App->>DB: connect("postgres://...")
  App->>DB: save("grant_applications", {...})
  DB-->>App: {"id":123}
  App->>Bus: publish("application.submitted", {"id":123})
  Bus-->>App: acknowledgment
```

---

## 5. Peek at the Code

### 5.1 Database Service (src/hms_sys/db.py)

```python
class HMSDatabase:
    @staticmethod
    def connect(name):
        # In reality: lookup URL in ConfigService, open pool, etc.
        print(f"Connected to database '{name}'")
        return HMSDatabase()

    def save(self, table, data):
        # Imagine INSERT INTO table ... RETURNING id
        new_id = 123  # dummy
        print(f"Saved record to {table}, id={new_id}")
        return {"id": new_id}
```

*Explanation:*  
- `connect` returns a handle to talk to the DB.  
- `save` inserts data and returns a new ID.

### 5.2 Messaging Bus (src/hms_sys/bus.py)

```python
class HMSBus:
    @staticmethod
    def connect():
        print("Connected to messaging bus")
        return HMSBus()

    def publish(self, topic, message):
        # In reality: serialize, authenticate, push to queue
        print(f"Published to '{topic}': {message}")
        return True
```

*Explanation:*  
- `connect` opens a channel to the bus.  
- `publish` sends events to whoever is listening.

### 5.3 Configuration Service (src/hms_sys/config.py)

```python
_CONFIG = {
    "db_connection": "postgres://user:pass@db.gov/app_db",
    "email.smtp_server": "smtp.ope.gov:587"
}

class ConfigService:
    @staticmethod
    def get(key):
        return _CONFIG.get(key)
```

*Explanation:*  
- A simple in-memory map. In real life, this might query a secure vault.

---

## 6. Conclusion

In this chapter, you learned how **HMS-SYS** provides core utilities—database, messaging, and configuration—that every government-focused microservice relies on. You saw analogies to building utilities, walked through a real example (submitting a grant application), and peeked at both high-level flows and simple implementation code.

Next up, we’ll see how individual services plug into this backbone and communicate using a **Microservices Architecture**.  

[Microservices Architecture](02_microservices_architecture_.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)