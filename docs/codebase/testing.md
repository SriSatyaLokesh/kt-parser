# Testing Patterns

**Analysis Date:** [YYYY-MM-DD]

## Test Framework

**Runner:**
- pytest
- pytest.ini (if present), pyproject.toml

**Assertion Library:**
- pytest, pytest-mock

**Run Commands:**
```bash
pytest -m "not integration"
pytest -m integration
```

## Test File Organization

**Location:**
- [Pattern]

**Naming:**
- [Pattern]

## Test Structure

**Suite Organization:**
```typescript
[Pattern]
```

**Patterns:**
- [Guidelines]

## Mocking

**Framework:**
- [Tool]

**Patterns:**
```typescript
[Example]
```

**What to Mock:**
- [List]

## Fixtures and Factories

**Test Data:**
```typescript
[Pattern]
```

## Coverage

**Requirements:**
- [Level/Policy]

## Test Types

**Unit Tests:**
- [Scope]

**Integration Tests:**
- [Scope]

**E2E Tests:**
- [Scope]

---
*Testing analysis: [date]*
