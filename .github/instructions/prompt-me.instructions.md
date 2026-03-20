---
description: "Use when the user says 'prompt me' — activates an interactive questioning workflow where the agent asks the user structured questions to clarify exactly what they want done before taking any action."
---

# Prompt Me — Interactive Task Specification

When the user says **"prompt me"**, do NOT start working immediately. Instead, ask the user a focused series of questions to understand exactly what they want. Follow this workflow:

## Step 1: Ask What

Ask the user: **"What do you want to accomplish?"**

Wait for their response before proceeding.

## Step 2: Clarify Scope

Based on their answer, ask 2-4 targeted follow-up questions to pin down:

- **Where**: Which files, services, or areas of the codebase are involved?
- **How**: Any specific approach, pattern, or constraint they have in mind?
- **Output**: What does "done" look like — a file change, a document, a terminal command, analysis?
- **Boundaries**: Anything explicitly out of scope or that should NOT be changed?

Only ask questions that are relevant to their answer in Step 1. Skip obvious ones.

## Step 3: Confirm the Plan

Summarize what you understood in a short numbered list and ask: **"Does this look right, or do you want to adjust anything?"**

## Step 4: Execute

Only after the user confirms, begin the work.

## Rules

- Never guess the user's intent — ask.
- Keep questions concise — no walls of text.
- If the user's initial description is already very specific, skip to Step 3 (confirm) instead of asking redundant questions.
- If the user says "prompt me" followed by a topic (e.g., "prompt me about testing"), use that topic as the starting context for Step 1.
