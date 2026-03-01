# 3. Context and Scope

> **Help**: Context and scope delimits the system (i.e., your scope of work) from all its communication partners (neighboring systems and users, i.e., the context of the system). It thereby specifies the external interfaces.
>
> If necessary, differentiate the business context (domain-specific inputs and outputs) from the technical context (channels, protocols, hardware).
>
> **Motivation**: The domain interfaces and technical interfaces to communication partners are among your system's most critical aspects. Make sure you completely understand them.
>
> **Form**: Various options:
> - Context diagrams
> - Lists of communication partners and their interfaces
> - Business and technical context diagrams (e.g., UML component, C4 context)

---

## 3.1 Business Context

> **Help**: Specification of **all** communication partners (users, IT-systems, ...) with explanations of domain-specific inputs and outputs or interfaces. Optionally, you can add domain-specific formats or communication protocols.
>
> **Motivation**: All stakeholders should understand which data are exchanged with the system's environment.
>
> **Form**: All kinds of diagrams that show the system as a black box and specify the domain interfaces to communication partners. Alternatively (or additionally), use a table. The title of the table is the name of the system, the three columns contain the name of the communication partner, the inputs, and the outputs.

### Business Context Diagram

_\<Insert a context diagram here showing the system and its communication partners. Consider using PlantUML, Mermaid, or C4 notation.\>_

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│  User /      │──────▶│                  │──────▶│  External   │
│  Actor       │◀──────│   <<System>>     │◀──────│  System A   │
└─────────────┘       │   System Name    │       └─────────────┘
                      │                  │
┌─────────────┐       │                  │       ┌─────────────┐
│  Admin       │──────▶│                  │──────▶│  External   │
│              │◀──────│                  │◀──────│  System B   │
└─────────────┘       └──────────────────┘       └─────────────┘
```

### Communication Partners

| Communication Partner | Input (to System) | Output (from System) |
|----------------------|-------------------|---------------------|
| _\<User/Actor\>_ | _\<What data does this partner send to the system?\>_ | _\<What data does the system provide to this partner?\>_ |
| _\<External System A\>_ | _\<Data/events received\>_ | _\<Data/events sent\>_ |
| _\<External System B\>_ | _\<Data/events received\>_ | _\<Data/events sent\>_ |
| _\<Database/Store\>_ | _\<Queries, commands\>_ | _\<Query results, confirmations\>_ |

---

## 3.2 Technical Context

> **Help**: Technical interfaces (channels and transmission media) linking the system to its environment. In addition, a mapping of domain-specific input/output to the channels, i.e., an explanation about which I/O uses which channel.
>
> **Motivation**: Many stakeholders make architectural decisions based on the technical interfaces between the system and its context. Especially infrastructure or hardware designers typically decide based on these technical interfaces.
>
> **Form**: E.g., UML deployment diagram describing channels to neighboring systems, together with a mapping table showing the relationships between channels and input/output.

### Technical Context Diagram

_\<Insert a technical context diagram here showing protocols, channels, and infrastructure.\>_

```
┌─────────┐  HTTPS/REST   ┌──────────────┐  gRPC        ┌──────────┐
│ Browser  │──────────────▶│              │─────────────▶│ Service  │
│ (SPA)    │◀──────────────│   API        │◀─────────────│ Backend  │
└─────────┘  JSON          │   Gateway    │  Protobuf    └──────────┘
                           │              │
┌─────────┐  HTTPS/REST   │              │  AMQP        ┌──────────┐
│ Mobile   │──────────────▶│              │─────────────▶│ Message  │
│ App      │◀──────────────│              │◀─────────────│ Broker   │
└─────────┘  JSON          └──────────────┘              └──────────┘
```

### Channel Mapping

| Domain Interface | Channel / Protocol | Format | Notes |
|-----------------|-------------------|--------|-------|
| _\<User interaction\>_ | _\<HTTPS/REST\>_ | _\<JSON\>_ | _\<Port 443, TLS 1.3\>_ |
| _\<Service-to-service\>_ | _\<gRPC\>_ | _\<Protocol Buffers\>_ | _\<Internal network only\>_ |
| _\<Event streaming\>_ | _\<AMQP / Kafka\>_ | _\<Avro / JSON\>_ | _\<Async, at-least-once delivery\>_ |
| _\<Database access\>_ | _\<TCP\>_ | _\<SQL / Wire protocol\>_ | _\<Connection pooling enabled\>_ |
| _\<File transfer\>_ | _\<SFTP / S3 API\>_ | _\<CSV / Parquet\>_ | _\<Batch processing\>_ |

---

> Based on the arc42 architecture template (https://arc42.org).  
> Created by Dr. Peter Hruschka and Dr. Gernot Starke.  
> Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
