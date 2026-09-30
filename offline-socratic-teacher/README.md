# Offline Socratic Artificial Teacher Validation

## Overview

This folder validates the prompt-building design for the Socratic Artificial
Teacher.

The goal is to make Gemma behave like an Artificial Teacher rather than a
normal chatbot.

The teacher should:

- Explain concepts clearly.
- Ask guiding questions.
- Give useful hints.
- Adapt explanations to the student's level.
- Adapt explanations to known student weaknesses.
- Use retrieved educational content.
- Avoid unnecessarily revealing the final answer immediately.

## Scope

This validation covers:

1. Teaching system instructions.
2. Student context.
3. Student learning level.
4. Student weakness.
5. Retrieved educational content.
6. Student question.
7. Prompt construction.
8. Hint and guiding-question behavior instructions.
9. Prevention of unnecessary direct answers.

## Out of Scope

The following are not implemented here:

- Retrieval implementation.
- Vector databases.
- Embeddings.
- Gemma model inference.
- API routes.
- Production backend integration.
- Frontend implementation.

This folder only validates the prompt-building logic before it is integrated
into the production application.

## Call Chain

The intended call chain is:

```text
Student Context
       +
Retrieved Knowledge
       +
Student Question
       |
       v
Prompt Builder
       |
       v
Teaching Prompt
       |
       v
Gemma