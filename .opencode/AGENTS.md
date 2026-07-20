{
  "skills": {
    "paths": [
      ".opencode/skills",
      "~/.config/opencode/skills"
    ],
    "enabled": [
      "paper-structure",
      "paper-draft",
      "paper-revision",
      "paper-review-consistency",
      "paper-review-language",
      "paper-humanize",
      "paper-ai-patterns",
      "paper-polish",
      "paper-latex-generate",
      "paper-latex",
      "paper-methodology",
      "paper-results",
      "paper-citation",
      "pdf-extract",
      "data-catalog",
      "data-preprocessing",
      "data-validation",
      "method-library",
      "paper-planning",
      "paper-factory",
      "paper-batch",
      "paper-diff",
      "paper-meta",
      "reproducibility-audit",
      "paper-pipeline"
    ],
    "pipeline": {
      "entry_point": "paper-pipeline",
      "single_paper": {
        "phases": [
          "paper-structure",
          "paper-draft",
          "paper-revision",
          "paper-latex-generate",
          "paper-latex"
        ],
        "revision_sub_phases": [
          "paper-review-consistency",
          "paper-review-language",
          "paper-polish"
        ],
        "revision_anti_ai": [
          "paper-humanize",
          "paper-ai-patterns"
        ]
      },
      "multi_paper": {
        "planning": "paper-planning",
        "factory": "paper-factory",
        "batch": "paper-batch",
        "synthesis": ["paper-diff", "paper-meta"]
      },
      "data_flow": {
        "catalog": "data-catalog",
        "preprocessing": "data-preprocessing",
        "validation": "data-validation",
        "methods": "method-library",
        "audit": "reproducibility-audit"
      }
    }
  },
  "agents": {
    "default_model": "deepseek-v4-pro",
    "permissions": {
      "allow": ["read", "write", "edit", "bash", "glob", "grep", "task", "webfetch"],
      "ask": ["delete", "git_push"],
      "deny": ["git_force_push"]
    }
  },
  "context": {
    "auto_load_files": [
      "AGENT.md",
      "README.md",
      "datasets/catalog/catalog.yml",
      "methods/METHODS.yml",
      "docs/metodologia-original.md",
      "docs/referencias.md"
    ]
  },
  "conventions": {
    "commits": "conventional-commits",
    "language": "espanol-rioplatense",
    "architecture": "multi-paper-factory",
    "formula": "paper = dataset x method x population",
    "coding_style": "header-en-scripts, rutas-relativas, parametros-declarados"
  },
  "pipeline_state": {
    "tracking_file": ".pipeline_state.json",
    "artifacts_dir": "results/reports/",
    "batch_state_dir": "papers/.batch_state/"
  }
}
