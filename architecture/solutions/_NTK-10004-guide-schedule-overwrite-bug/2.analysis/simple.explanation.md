# Simple Explanation: Guide Schedule Overwrite Bug

## What is happening

Guides enter personal schedule information - vacation days, training blocks, medical notes, group size limits - through the Guide Portal. This information is stored by the guide management service.

A separate scheduling service runs optimization overnight (and on-demand) to assign guides to trails efficiently. When it finishes optimizing, it saves the new schedule by completely replacing the old one. But it only knows about trail assignments and shift patterns. It does not know about vacations, notes, or any other information the guide entered manually.

The result: every time optimization runs, all manual guide entries are erased.

## Why it matters

- Guides lose vacation blocks and get assigned to trails during their PTO
- Medical restrictions (like altitude limits) are silently removed, creating safety risk
- Guides must re-enter their information after every optimization, causing frustration
- When multiple regions optimize at the same time, a guide's schedule can be corrupted by competing writes

## The core problem

The scheduling service treats the guide schedule as something it fully owns, but it is actually shared data. The scheduling service only owns trail assignments and shifts. The guide management service owns availability, notes, and overrides. When the scheduling service overwrites the entire document, it destroys data that belongs to the other service.
