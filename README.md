# Legacy Node.js Refactor Demo

This repository intentionally starts with a messy Node.js order API and then refactors it into a typed, tested TypeScript service. It is designed as an inheritance exercise for a senior engineer joining a legacy codebase.

## Run it

```bash
npm install
npm run legacy   # poorly structured JavaScript version
npm run build    # TypeScript compile
npm test         # unit and integration tests
npm start        # compiled refactored service
```

## Step 1: Poorly structured legacy project

The legacy implementation lives in [`legacy/before/app.js`](legacy/before/app.js). It intentionally includes:

- tight coupling between Express routes, storage, validation, discount calculation, inventory mutation, and response formatting
- repeated logic for total calculation and validation
- no separation of concerns
- minimal comments and many implicit assumptions
- inconsistent error responses

### Before: one route owns everything

```js
app.post('/orders', (req, res) => {
  console.log('POST /orders');
  var body = req.body || {};

  if (!body.customerName || body.customerName.length < 2) {
    res.status(400).json({ error: 'bad customerName' });
    return;
  }

  // validation, inventory, pricing, persistence, logging, and HTTP formatting
  // are all mixed together in the same function.
});
```

## Step 2: Refactored TypeScript architecture

The refactored implementation lives under [`src`](src) and uses an MVC-style HTTP boundary with clean service and repository layers:

```text
src/
  app.ts                         # application composition
  server.ts                      # process entry point
  domain/
    order.ts                     # typed entities and commands
    errors.ts                    # typed application errors
    orderService.ts              # business rules
  repositories/
    orderRepository.ts           # persistence contract
    inMemoryOrderRepository.ts   # storage implementation
  validation/
    orderSchemas.ts              # request validation
  logging/
    logger.ts                    # logging abstraction
  http/
    controllers/orderController.ts
    middleware/errorMiddleware.ts
```

### After: controller delegates to validation and domain services

```ts
router.post(
  '/',
  asyncHandler(async (req, res) => {
    const command = createOrderSchema.parse(req.body);
    const order = await orderService.createOrder(command);

    res.status(201).json(order);
  }),
);
```

## Step 3: Major refactor decisions

### 1. Route handlers no longer contain business logic

**What was wrong:** `legacy/before/app.js` calculated totals, validated inputs, generated IDs, saved data, and shaped HTTP responses in one place. Any change to pricing or validation required editing route handlers.

**Why this is better:** `OrderService` now owns business rules. Controllers only translate HTTP into application commands and responses. This makes order creation testable without Express.

**Tradeoff:** There are more files and constructor wiring. The extra structure is justified because behavior is now isolated and reusable.

### 2. Repeated pricing code became a single domain calculation

**What was wrong:** Subtotal, discount, and tax calculations were duplicated in `POST /orders` and `GET /orders/:id/summary`, risking drift.

**Why this is better:** `OrderService` is the only place that calculates money. Created orders and later reads use the same persisted total model.

**Tradeoff:** Pricing changes now happen through the service instead of quick inline edits, which is a small ceremony increase for a safer invariant.

### 3. Runtime validation is explicit

**What was wrong:** Legacy validation used scattered `if` statements and accepted invalid shapes such as non-array `items` until later code failed.

**Why this is better:** Zod schemas define the HTTP contract and produce structured validation errors before domain code runs.

**Tradeoff:** Validation has a dependency and schema definitions must be kept aligned with TypeScript types. The payoff is clearer input boundaries.

### 4. Typed errors replaced ad hoc responses

**What was wrong:** The legacy code returned different error formats and sometimes leaked operational details.

**Why this is better:** `AppError`, `ValidationError`, and `NotFoundError` carry stable status codes and machine-readable codes. Central middleware turns them into consistent JSON.

**Tradeoff:** Developers need to choose the right error class. In return, clients get predictable failures.

### 5. Logging moved behind a small module

**What was wrong:** `console.log` was scattered through handlers without structure.

**Why this is better:** Pino creates structured logs with request-relevant metadata and can be replaced or configured centrally.

**Tradeoff:** Structured logging is a little less casual than `console.log`, but it is much more useful in production.

### 6. Persistence is behind an interface

**What was wrong:** The legacy global arrays were directly read and mutated by routes.

**Why this is better:** `OrderRepository` gives the service a contract. The current in-memory implementation is simple, while future database persistence can be added without rewriting HTTP controllers or business rules.

**Tradeoff:** The repository adds indirection. It prevents storage details from leaking across the app.

## Step 4: Tests

Tests live in [`tests`](tests):

- unit tests cover `OrderService` business behavior and error paths
- integration tests exercise the Express app with validation, creation, lookup, payment status updates, and 404 handling

## Step 5: Conceptual diff-style summary

```diff
- JavaScript-only Express file with global mutable state
+ TypeScript project with typed domain models and strict compiler settings

- Route handlers perform validation, pricing, persistence, and response formatting
+ Controllers delegate validation to schemas and business rules to services

- Duplicated subtotal/discount/tax logic
+ Single total calculation path in OrderService

- Inconsistent { error: string } responses
+ Central error middleware with status, code, and message

- console.log scattered across routes
+ Structured Pino logger module

- No tests
+ Unit tests for domain behavior and integration tests for HTTP behavior

- No clear migration story
+ Legacy implementation preserved under legacy/before and refactored implementation under src
```
