---
name: "explain-code"
description: "Explain what a piece of code, a file or a project does and why, pitched at the reader. Give its purpose in one sentence, walk through the important parts in the order data flows, trace one invented input through it, and name the side effects, edge cases and surprises. Use when someone asks \"what does this do\", \"how does this work\", \"walk me through\", or is new to a codebase."
---

# Explain Code

An explanation succeeds when the reader could predict what the code does with
a new input. Aim for that, not for describing every line.

## 1. Know the reader

Pick the level from how they asked and what they said about themselves:

- **New to programming:** plain words, define each term once ("a dictionary
  is a lookup table of keys and values"), no jargon without a gloss.
- **A developer new to this code:** the design, the flow, where things live,
  conventions to follow.
- **An expert asking about one detail:** answer that detail first, briefly.

If you can't tell, aim for a developer new to the code and offer to go
simpler or deeper.

## 2. Read before you explain

- Read the whole function or file, and what calls it. For a project, read
  the README, the entry point (main, the routes, the CLI) and the folder
  layout first. Use `workspace.files` for the user's files and
  `workspace.git` to clone a public repository.
- Run it when that is the quickest way to be sure (`workspace.python` with a
  tiny input). An explanation checked by running is worth more than one
  inferred.
- Separate what the code does from what its names and comments claim. When
  they disagree, say so.

## 3. Structure the answer

1. **Purpose, in one sentence.** "parse_invoice turns the text of a supplier
   invoice into a dict of line items and a total."
2. **The big picture** (for anything larger than one function): the parts
   and how data moves between them, as a short list or a small diagram:

   ```
   upload -> parse_invoice -> validate_totals -> save_to_ledger
   ```

3. **Walk through the important parts** in the order data flows, quoting
   short snippets with file and line. Skip the boilerplate.
4. **A worked example:** trace one invented input all the way through.

   ```
   Input:  "Blue Kettle x2 @ 18.00"
   split   -> ["Blue Kettle", "2", "18.00"]
   result  -> {"item": "Blue Kettle", "qty": 2, "unit": 18.0, "line": 36.0}
   ```

5. **Watch out for:** side effects (writes files, sends email, changes a
   global), edge cases (an empty invoice, a comma as decimal point), error
   handling, performance traps, and anything surprising.

## 4. Make it stick

- Prefer concrete values to abstract descriptions.
- Explain why when the code shows a deliberate choice ("it sorts first so the
  binary search below works").
- Keep each paragraph to one idea. Use the code's own names in backticks.
- End with one line on where to look next, if they want to go further.

## Rules

- Never invent behaviour you didn't read or run. Say "I didn't see where X is
  set" instead of guessing.
- Don't rewrite or review the code unless asked; offer it in one line if you
  saw a real bug.
