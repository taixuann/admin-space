# Orchestra Companion

Orchestra Companion coordinates one continuing Agents Ticket across intake, context gathering, human decisions and later work. Plugins represent role owners; skills represent actions. A ticket remains the record of intent, plans, execution evidence and reviews.

## First action

- receiving-ticket reads a selected ticket, checks its identity and category, requests scoped Wiki context when available, records an attributed intake packet, and prepares it for Human review. It stops before downstream work or routing.

This first source draft contains only receiving-ticket. Routing and request actions remain future work until their contracts are agreed.

## Boundaries

Notion remains the ticket authority. Orchestra does not create a parallel tracker, claim that a bot was dispatched when no transport ran, or treat Human review as route approval. Research evidence and scientific execution remain with their owning research workflows. Admin covers workspace tools, skills, agents, bots and their coordination.
