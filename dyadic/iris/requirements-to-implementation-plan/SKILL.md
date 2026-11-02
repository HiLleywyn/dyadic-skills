---
name: "requirements-to-implementation-plan"
description: "Turn a feature request or requirements into an implementation plan someone can build from. Restate the goal, write checkable acceptance criteria, ask only the questions that change the design, look at the existing code, choose a design and say why, break the work into small ordered steps each with its test, and list risks, what is out of scope and a rough size. Use when someone asks to plan a feature, scope work, \"how would we build this\", or before writing a large change."
---

# Requirements to Implementation Plan

A plan is good when someone could build the feature from it without another
meeting, and could tell when they were done. Keep it as short as that allows.

## 1. Restate the goal

One or two sentences in the user's terms: who needs what, and why.

> Shop owners want to offer a discount code at checkout, so they can run
> promotions without changing prices by hand.

## 2. Acceptance criteria

Write what must be true when it's done, each one checkable:

```
- A customer can enter a code at checkout and sees the discounted total.
- An unknown or expired code shows "This code isn't valid" and changes nothing.
- A code can be a percentage (1 to 90) or a fixed amount, never below 0.
- Each order records the code it used.
- The owner can create, pause and delete codes.
```

Mark each **must**, **should** or **later**. Anything not listed is out of
scope; say so explicitly ("no per-customer limits in this version").

## 3. Questions that change the design

Ask only what would change the plan, each with your proposed default so work
can go on:

```
1. Can two codes apply to one order? (Proposed: no, one code per order.)
2. Does the discount apply before or after shipping? (Proposed: before.)
```

Don't block on questions with an obvious default; state the assumption.

## 4. Look at what exists

When there is code, read the parts this touches (with `workspace.files`, or
`workspace.git` for a public repository): the models, where checkout totals
are computed, how other settings are stored, the test setup. Reuse existing
patterns rather than inventing new ones, and note what will have to change.

## 5. Design

Describe the approach in a few lines: the data (new tables or fields), the
interfaces (endpoints, functions, screens), and where the logic lives. Give
the one or two alternatives you rejected and why, in a sentence each.

```
Data: discount_codes(code, kind percent|amount, value, active, expires_at);
orders.discount_code.
Logic: pricing.apply_discount(total, code) used by checkout and the order
summary, so both always agree.
Rejected: storing the discounted price only (loses what the discount was).
```

## 6. Steps

Small steps in a safe order, each one shippable or at least testable on its
own, each with how to check it:

```
1. Add the discount_codes table and migration.
   Test: migration runs up and down on an empty database.
2. pricing.apply_discount with its rules.
   Test: unit tests for percent, amount, floor at 0, unknown and expired codes.
3. Checkout accepts a code and shows the new total.
   Test: an end-to-end checkout with SAVE10 totals 45.00 for a 50.00 basket.
4. Orders record the code used.
   Test: the saved order has discount_code = "SAVE10".
5. Owner screen: create, pause, delete.
   Test: a paused code is refused at checkout.
```

Data and core logic first, then what uses it, then the screens. Put anything
risky or uncertain early, so surprises arrive while they are cheap.

## 7. Risks and size

- **Risks:** what could go wrong and how the plan guards against it
  (rounding money: store cents as integers; abuse: rate-limit code attempts).
- **Migration and rollout:** existing data, a feature switch, how to undo.
- **Size:** a rough range per step (hours or days), and the total. Say what
  the estimate depends on.

## Rules

- Every requirement maps to at least one step, and every step to a test.
- Don't pad the plan: no steps that only restate others.
- If the request is too vague to plan, write the questions first and stop.
