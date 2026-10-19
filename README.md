# openrouter-top

> **Archived.** This tracker now runs in [Nitjsefnie/ai-researcher](https://github.com/Nitjsefnie/ai-researcher) (`data/openrouter-trending.json`, refreshed hourly by its `refresh` workflow). This repository is no longer updated.

OpenRouter's top 10 models by weekly tokens — just the model slugs, in
OpenRouter's order (`https://openrouter.ai/api/frontend/v1/models/find?order=top-weekly`),
fetched every hour into [`top.json`](top.json). Each data commit announces
what moved: models new to the top 10, models that left it, and rank changes,
so `git log` is the history.

Run by [`update.py`](update.py) from the hourly `update` workflow.
