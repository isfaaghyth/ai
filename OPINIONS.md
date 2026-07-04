# Isfa's Engineering & Architectural Viewpoints

This document outlines Isfa's technical philosophies, preferences, and architecture patterns. Refer to these guidelines when making design decisions.

---

## 1. Programming Languages & Stacks
*   **Kotlin Multiplatform (KMP)**: Prefer KMP for shared business logic, networking, and state management in mobile apps. Keep native UI code (Jetpack Compose for Android, SwiftUI for iOS) clean and decoupled from business logic.
*   **Go (Golang)**: Prefer Go for backend APIs and microservices. Keep packages idiomatic and follow standard project layouts. Avoid heavy ORMs when writing performance-critical paths; raw SQL or query builders (like sqlc or Ent) are preferred.
*   **React & Tailwind CSS**: Build modular components. Avoid deep nesting of divs. Use Tailwind utilities utility-first, and leverage components or libraries (like shadcn/ui or Radix) for accessibility.

---

## 2. Code Quality & Technical Debt
*   **Quality Over Speed**: Never rush code structure. Take the time to write unit tests, handle edge cases, and type out interfaces cleanly.
*   **Testing Philosophy**: Write testable code. Every critical service, model, or repository layer should have unit tests. Flaky tests are bugs; fix them immediately.

---

## 3. Tooling & Hosting Preferences
*   **Containers**: Use Docker Compose for local environments and orchestration.
*   **Deployment**: Prefer Git-based automated pipelines. Keep server infrastructure simple and easy to maintain.
