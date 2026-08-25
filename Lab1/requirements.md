# Lab 1 – Requirements Engineering & UML Use-Case Modelling

## Problem Statement #59
### Community Lost & Found Matching Network

## Functional Requirements

| ID | Requirement | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| FR-001 | Lost Item Registration | The system shall allow users to register lost items with details such as category, color, description, location, and date. | High | Pass: A lost item is successfully recorded with all required details. Fail: The system accepts an incomplete lost-item report. | Provides the information required for matching lost items with found items. |
| FR-002 | Found Item Registration | The system shall allow finders to register found items with category, color, description, location, and date. | High | Pass: A found item is successfully recorded with all required details. Fail: The system accepts an incomplete found-item report. | Creates the pool of found items that can be matched against lost-item reports. |
| FR-003 | Lost-and-Found Matching | The system shall match newly logged found-item posts with active lost-item reports based on category, color tags, and location radius. | High | Pass: A compatible match is identified and its match probability is calculated. Fail: Incompatible item categories are matched. | Helps owners locate potentially recovered belongings efficiently. |
| FR-004 | Match Notification | The system shall notify potential owners when a found item has a sufficiently strong match with their lost-item report. | Medium | Pass: A notification is dispatched to the potential owner after a valid match. Fail: No notification is sent for a valid match. | Ensures potential owners are informed about relevant found items. |
| FR-005 | Ownership Verification | The system shall require a claimant to answer private security questions set by the finder before contact details are revealed. | High | Pass: Correct answers allow contact details to be revealed. Fail: Incorrect answers reveal contact details. | Provides proof-of-ownership verification before item handover. |

## Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| NFR-001 | Performance & Security | Claimants must answer private security questions set by the finder before item handover contact details are revealed. | High | Pass: Benchmarking tests confirm the required security standards and acceptable response latency under simulated peak load. Fail: Contact details are revealed without successful verification. | Protects user privacy and prevents unauthorized claims. |
| NFR-002 | Performance | The system shall calculate item matches and dispatch notifications within an acceptable response time under simulated peak load. | Medium | Pass: Benchmarking tests confirm the target latency under simulated peak load. Fail: Matching and notification processing exceeds the target latency. | Ensures the matching network remains responsive when many reports are active. |
