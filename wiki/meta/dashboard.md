---
type: meta
title: "Dashboard"
created: 2026-04-14
updated: 2026-04-14
---

# Wiki Dashboard

## Recent Activity

```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## Seed Pages (Need Development)

```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```

## Entities Missing Sources

```dataview
LIST FROM "wiki/entities" WHERE !sources OR length(sources) = 0
```

## Open Questions

```dataview
LIST FROM "wiki/questions" WHERE answer_quality = "draft" SORT updated DESC
```

## Papers Not Yet Ingested

```dataview
LIST FROM "wiki/sources" WHERE status = "seed" SORT created ASC
```
