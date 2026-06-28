## Context

This project aims to create a comprehensive comparison of Python frontend frameworks by building the same barbershop management SaaS application using 6 different Python frontend frameworks, all sharing a common FastAPI backend backend. The project addresses the need for concrete, hands-on comparisons of Python frontend ecosystems beyond theoretical discussions.

Current state: Greenfield project with no existing codebase.
Stakeholders: Developers, technical architects, and technology decision-makers evaluating Python frontend options.
Constraints: 
- Must use Python 3.13+ for both backend and frontend
- Backend must follow clean architecture, DDD principles, and TDD
- All frontends must implement identical feature sets for fair comparison
- Project must remain functional at each milestone

## Goals / Non-Goals

**Goals:**
- Create 6 fully functional frontend applications using Reflex, Solara, FastUI, Streamlit, Flet, and Kivy
- Share a single FastAPI backend implementation following clean architecture principles
- Implement identical barbershop SaaS features across all frontends
- Document architectural decisions, trade-offs, and developer experience for each stack
- Provide deployment guidance for each frontend type (web, desktop, mobile)
- Enable direct comparison of performance, development velocity, and scalability characteristics

**Non-Goals:**
- Creating pixel-perfect identical UIs across frameworks (leveraging framework strengths instead)
- Implementing enterprise-scale features beyond MVP scope (payments, advanced integrations)
- Supporting legacy Python versions (<3.13)
- Building native iOS/Android apps via separate toolchains (Flet and Kivy cover cross-platform)
- Implementing advanced real-time collaboration features beyond basic updates

## Decisions

### Backend Architecture: Clean Architecture with Domain-Driven Design
**Decision:** Use Clean Architecture with hexagonal (ports and adapters) pattern, organizing code into layers: domain, application, infrastructure, and API.
**Alternatives Considered:**
- Simple MVC structure: Rejected for not scaling well with complex business logic
- Traditional 3-layer architecture: Revealed insufficient separation of concerns
- Microservices: Overhead not justified for this scope
**Rationale:** Provides clear separation between business logic and framework concerns, enables independent frontend development, aligns with DDD principles, and supports testing independence.

### Backend Technology Stack
**Decision:** FastAPI with SQLAlchemy 2.0, PostgreSQL, Redis, and Pydantic v2.
**Alternatives Considered:**
- Django ORM: Excellent but less suitable for API-first approach
- Tortoise ORM: Good async support but less mature ecosystem
- Pydantic v1: Lacking performance improvements of v2
**Rationale:** FastAPI provides excellent OpenAPI support, automatic docs, and performance. SQLAlchemy 2.0 offers modern SQL expression language. Pydantic v2 provides superior validation performance.

### Backend Project Structure
**Decision:** Monorepo structure with clearly bounded contexts:
```
backend/
├── apps/
│   ├── auth/
│   ├── tenants/
│   ├── customers/
│   ├── barbers/
│   ├── services/
│   └── appointments/
├── core/
│   ├── database/
│   ├── messaging/
│   └── security/
└── shared/
    ├── kernel/
    └── exceptions/
```
**Alternatives Considered:**
- Single monolithic module: Would create coupling issues as project grows
- Separate repos for each bounded context: Overhead not justified for this scope
**Rationale:** Balances modularity with simplicity, enables clear ownership boundaries, and keeps all code in one repository for easier comparison.

### Backend Communication Patterns
**Decision:** 
- Synchronous: REST APIs via FastAPI for CRUD operations
- Asynchronous: Redis pub/sub for real-time notifications (appointment updates, etc.)
- Background Tasks: Celery for email/SMS notifications and report generation
**Alternatives Considered:**
- GraphQL: Added complexity not needed for current scope
- WebSocket direct connections: More complex scaling vs pub/sub approach
- RQ instead of Celery: Celery offers better ecosystem and monitoring
**Rationale:** Provides appropriate sync/async patterns for different use cases while leveraging mature Python ecosystem tools.

### Frontend Framework Selection Rationale

**Reflex:** Chosen for true fullstack Python experience - enables React-like SPA development without writing JavaScript, ideal for traditional web applications requiring rich interactivity.

**Solara:** Selected for data-intensive dashboards and analytics - built on ipywidgets, excels at data visualization and scientific computing interfaces, perfect for the financial/dashboard components.

**FastUI:** Chosen for API-driven UI approach - generates UI from backend-defined JSON schemas, excellent for admin panels and internal tools where backend drives presentation.

**Streamlit:** Selected for rapid MVP development - unmatched speed for data apps and internal tools, ideal for validating concepts quickly despite limited customization options.

**Flet:** Chose for true cross-platform capabilities - single codebase targeting web, desktop (Windows/macOS/Linux), and mobile (via webview), perfect for demonstrating Flutter-like capabilities in Python.

**Kivy:** Selected for native mobile experiences - provides access to native controls and offline capabilities, ideal for tablet/kiosk mode usage in barbershops.

### State Management Approach

**Decision:** Framework-specific state management approaches:
- Reflex: Built-in reactive state management
- Solara: Reactive variables similar to Vue.js reactivity
- FastUI: Server-driven state via JSON schemas
- Streamlit: Session state and callbacks
- Flet: Page/control-based state with update methods
- Kivy: Property-based binding and event system
**Alternatives Considered:** External state management libraries (Redux-style patterns)
**Rationale:** Leveraging each framework's native state management provides authentic experience comparisons rather than imposing external patterns.

### Data Access Strategy

**Decision:** Backend provides RESTful APIs with synchronous/asynchronous endpoints:
- Standard CRUD operations via REST
- Real-time updates via Server-Sent Events (SSE) or WebSocket adapters per framework
- Background jobs for long-running operations
**Alternatives Considered:**
- GraphQL subscriptions: Added complexity not justified
- Direct database access: Violates security and separation principles
**Rationale:** Provides appropriate abstraction while allowing each frontend to implement real-time updates in framework-appropriate ways.

### Development Experience Standardization

**Decision:** Standardize development workflows across frontends:
- Consistent virtual environment management (UV/venv)
- Standardized testing approaches (unit + E2E where applicable)
- Uniform linting/formatting (Ruff/Black)
- Standardized commit messages and PR templates
**Alternatives Considered:** Framework-specific toolchains only
**Rationale:** Enables fair comparison by reducing environmental variables while still allowing framework-specific optimizations where beneficial.

### Testing Strategy

**Decision:** 
- Backend: Comprehensive unit and integration tests using pytest
- Frontends: Framework-appropriate testing (where available) + E2E testing with Playwright for critical paths
- Contract testing: Ensure all frontends work with same API specifications
**Alternatives Considered:** Exclusive reliance on manual testing
**Rationale:** Ensures reliability while acknowledging varying testing maturity across Python frontend frameworks.

### Deployment Strategy

**Decision:** Environment-specific deployment approaches:
- Web frontends (Reflex, Solara, FastUI, Streamlit): Containerized via Docker, deployable to standard web hosts
- Desktop (Flet): Platform-specific installers or Electron-like wrapping
- Mobile (Kivy/Flet): APK/IPA generation and app store deployment
**Alternatives Considered:** Single deployment target for all
**Rationale:** Honors each framework's deployment strengths while providing realistic deployment scenarios.

## Risks / Trade-offs

**[Scope Creep]** → Mitigation: Strict adherence to defined feature set per phase, explicit out-of-scope items, regular scope reviews
**[Framework Volatility]** → Mitigation: Pin exact versions, document version rationale, plan for periodic updates
**[Inconsistent Feature Implementation]** → Mitigation: Detailed feature specifications, regular comparison reviews, shared backend API contract
**[Learning Curve Overhead]** → Mitigation: Timeboxed learning spikes, leverage existing framework documentation/tutorials
**[Performance Comparison Invalidity]** → Mitigation: Controlled testing environments, baseline measurements, focus on relative rather than absolute performance
**[Deployment Complexity]** → Mitigation: Documented deployment guides per platform, containerized where possible, separate DevOps considerations from core comparison

## Migration Plan

**Phase 0:** Foundation
- Setup repository structure and CI/CD pipeline
- Implement core backend architecture (auth, tenants, database)
- Define API contracts and data models

**Phase 1:** Core Features
- Implement customer, barber, and service management
- Basic CRUD operations for all frontends
- Initial UI implementations focused on functionality over polish

**Phase 2:** Scheduling & Calendar
- Appointment booking system
- Calendar views and conflict detection
- Notification system for reminders

**Phase 3:** Analytics & Reporting
- Financial dashboard
- Business intelligence reports
- Data export capabilities

**Phase 4:** Polish & Deployment
- UI/HP refinements per framework
- Performance optimization
- Documentation and comparison guide
- Deployment scripts for each platform

**Rollback Strategy:** Git-based version control enables straightforward rollback to any phase. Database migrations designed to be backward-compatible where possible.

## Open Questions

**[Authentication Method]** → TBD: JWT vs session-based auth, considering refresh token strategy and CSRF protection
**[Real-time Implementation]** → TBD: WebSocket vs Server-Sent Events vs polling fallback strategies per framework
**[State Persistence]** → TBD: LocalStorage vs IndexedDB vs framework-specific solutions for offline capabilities (especially Kivy/Flet)
**[Testing Approach]** → TBD: Extent of E2E testing per framework given varying testing tool maturity
**[Deployment Automation]** → TBD: CI/CD pipeline complexity for 6 different deployment targets
**[License Considerations]** → TBD: Verify licensing implications of each framework for potential commercial use