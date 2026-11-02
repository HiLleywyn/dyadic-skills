---
name: algorithmic-art
description: Create original, seeded generative art with interactive controls and a downloadable HTML file. Use for algorithmic art, flow fields, particles and procedural drawings.
license: Complete terms in LICENSE.txt
---

# Algorithmic Art


Build the requested artwork, then verify and deliver it. A skill is guidance,
not a callable function. Use the actual tools offered in this run.

## Read and choose

Read `viewer.html` with `skills.read(name="algorithmic-art", path="viewer.html", full=true)`.
Read larger supporting files using their returned `next_offset`. Do not probe
shell paths or reload a tool already visible just to read this template.

Use the template as a working starting point, not a mandatory layout or brand.
Choose an original algorithm and a few meaningful controls matching the request.
Canvas 2D works without external dependencies. Use p5.js only when the project
already supplies it or its dependency is explicitly handled; do not assume a CDN
is available. Follow the project's existing theme, typography and accessibility.

## Implement

Unless the user asks for a project with separate files, create **one HTML file**
with inline CSS and JavaScript. Include a visible drawing, a seed input, redraw,
and controls that actually affect the algorithm. Keep random generation seeded
and bound loops, particle counts and canvas dimensions. Same seed and settings
must reproduce the same drawing. Do not make a manifesto, extra source files or
unrequested dependencies prerequisites for completing an ordinary art request.

Use `workspace.write(path=<exact destination>, content=<complete file text>)`.
If only legacy `workspace.files` is offered, its write action requires `action`,
`path` and `content` together. Do not guess missing fields, call a nonexistent
`skills.algorithmic-art`, or substitute a text description for a created file.

## Verify and finish

Check that the HTML loads without missing dependencies or JavaScript errors.
Where a permitted browser is available, inspect a phone-sized and desktop view,
change the seed and one parameter, and check the exported image. Test extreme
parameter values without excessive work. Verify gradients or other explicitly
requested effects in the actual drawing, not just in labels or CSS controls.

Persist the finished file and attach it using `workspace.send_file` when offered
and authorized. A saved file is not a delivery receipt. If a runtime, browser or
delivery capability is unavailable, state exactly which checks or delivery are
unverified; do not claim execution or fetch unrelated tools repeatedly. Stop
after the requested artwork, relevant checks and delivery are complete.
