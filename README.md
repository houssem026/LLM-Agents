# LLM Agents

Workspace for collaborating on agent-specific projects, prompts, experiments, and shared documentation.

## Structure

- `agents/`: one folder per agent implementation or agent-specific notes.
- `shared/`: reusable code, utilities, datasets, or references shared by multiple agents.
- `prompts/`: prompt templates and prompt experiments.
- `experiments/`: prototypes, evaluations, and scratch projects worth tracking.
- `docs/`: documentation, decisions, and setup notes.

## Agent Workspaces

- `agents/ai_blog_to_podcast_agent/`: local Streamlit agent that turns public blog URLs into WAV podcast episodes with Agno, Ollama, trafilatura, and Piper. See `agents/ai_blog_to_podcast_agent/README.md` for architecture and technical choices.

## Git Workflow

1. Create or edit files in the relevant folder.
2. Check changes with `git status`.
3. Commit with `git add .` and `git commit -m "message"`.
4. Push with `git push` once a remote is configured.
