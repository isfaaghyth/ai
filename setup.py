import os
# setup.py — reads .env and generates all profile config.yaml files.
# Add new profiles to PROFILES dict. Models are resolved with DEFAULT_MODEL as fallback.
import shutil

# CONFIG SCHEMA
# Defines all agent profiles and which env keys control their models.
# To add a new profile, just add an entry here.
PROFILES = {
    "dev_tpm": {
        "telegram_key": "TELEGRAM_TOKEN_DEV_TPM",
        "model_default": "MODEL_DEV_TPM",
        "model_execution": None,  # single-model profile
        "reasoning_effort": "REASONING_DEV_TPM",
    },
    "dev_kotlin_mobile": {
        "telegram_key": "TELEGRAM_TOKEN_DEV_KOTLIN_MOBILE",
        "model_default": "MODEL_DEV_KOTLIN_MOBILE_PLANNING",
        "model_execution": "MODEL_DEV_KOTLIN_MOBILE_EXECUTION",
        "reasoning_effort": "REASONING_DEV_KOTLIN_MOBILE",
    },
    "dev_golang_backend": {
        "telegram_key": "TELEGRAM_TOKEN_DEV_GOLANG_BACKEND",
        "model_default": "MODEL_DEV_GOLANG_BACKEND_PLANNING",
        "model_execution": "MODEL_DEV_GOLANG_BACKEND_EXECUTION",
        "reasoning_effort": "REASONING_DEV_GOLANG_BACKEND",
    },
    "dev_frontend_react": {
        "telegram_key": "TELEGRAM_TOKEN_DEV_FRONTEND_REACT",
        "model_default": "MODEL_DEV_FRONTEND_REACT_PLANNING",
        "model_execution": "MODEL_DEV_FRONTEND_REACT_EXECUTION",
        "reasoning_effort": "REASONING_DEV_FRONTEND_REACT",
    },
    "daily_general": {
        "telegram_key": "TELEGRAM_TOKEN_DAILY_GENERAL",
        "model_default": "MODEL_DAILY_GENERAL",
        "model_execution": None,
        "reasoning_effort": "REASONING_DAILY_GENERAL",
    },
    "daily_learning_buddy": {
        "telegram_key": "TELEGRAM_TOKEN_DAILY_LEARNING_BUDDY",
        "model_default": "MODEL_DAILY_LEARNING_BUDDY",
        "model_execution": None,
        "reasoning_effort": "REASONING_DAILY_LEARNING_BUDDY",
    },
}

PLACEHOLDER_CHECKS = [
    "your_openrouter_api_key_here",
    "your_anthropic_api_key_here",
    "your_github_personal_access_token_here",
]


def parse_env(env_file: str) -> dict:
    config = {}
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                config[key.strip()] = val.strip()
    return config


def sanitize(val: str, placeholder: str = "") -> str:
    """Return empty string if value is a known placeholder."""
    if not val or val in PLACEHOLDER_CHECKS:
        return placeholder
    return val


def generate_config_yaml(profile_name: str, profile_schema: dict, config: dict) -> str:
    """Dynamically generate a config.yaml from env values."""
    # Global defaults — used if a profile-specific var is missing or empty
    global_default_model     = config.get('DEFAULT_MODEL', 'anthropic/claude-sonnet-5')
    global_default_reasoning = config.get('DEFAULT_REASONING', 'medium')

    provider      = sanitize(config.get('PROVIDER', 'openrouter'), 'openrouter')
    base_url      = sanitize(config.get('PROVIDER_BASE_URL', ''), 'https://openrouter.ai/api/v1')
    model_default = sanitize(config.get(profile_schema['model_default'], ''), global_default_model)
    reasoning     = sanitize(config.get(profile_schema['reasoning_effort'], ''), global_default_reasoning)
    max_turns     = sanitize(config.get('AGENT_MAX_TURNS', ''), '90')
    timeout       = sanitize(config.get('AGENT_TIMEOUT', ''), '180')

    lines = ["model:"]
    lines.append(f'  default: "{model_default}"')

    # Add execution model only if profile declares one; falls back to the planning model
    if profile_schema.get('model_execution'):
        model_exec = sanitize(config.get(profile_schema['model_execution'], ''), model_default)
        lines.append(f'  execution: "{model_exec}"')

    lines.append(f'  provider: "{provider}"')
    lines.append(f'  base_url: "{base_url}"')
    lines.append("")
    lines.append("terminal:")
    lines.append('  backend: "local"')
    lines.append('  cwd: "."')
    lines.append(f"  timeout: {timeout}")
    lines.append("")
    lines.append("agent:")
    lines.append(f"  max_turns: {max_turns}")
    lines.append(f'  reasoning_effort: "{reasoning}"')
    lines.append("")
    lines.append("memory:")
    lines.append("  memory_enabled: true")
    lines.append("  user_profile_enabled: true")
    lines.append("")
    lines.append("gateway:")
    lines.append('  provider: "telegram"')
    lines.append("")

    return "\n".join(lines)


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    env_example = os.path.join(root_dir, "env.example")
    env_file = os.path.join(root_dir, ".env")

    if not os.path.exists(env_file):
        shutil.copy(env_example, env_file)
        print("[!] Created `.env` from `env.example`.")
        print("[!] Fill in your keys and tokens, then run this script again.")
        return

    config = parse_env(env_file)

    profiles_data_dir = os.path.join(root_dir, "data", "profiles")
    templates_dir = os.path.join(root_dir, "templates")

    openrouter_key = sanitize(config.get("OPENROUTER_API_KEY", ""))
    anthropic_key = sanitize(config.get("ANTHROPIC_API_KEY", ""))
    github_token = sanitize(config.get("GITHUB_TOKEN", ""))
    allowed_users = config.get("TELEGRAM_ALLOWED_USER_IDS", "")
    git_name = config.get("GIT_AUTHOR_NAME", "")
    git_email = config.get("GIT_AUTHOR_EMAIL", "")

    for profile_name, schema in PROFILES.items():
        profile_dest_dir = os.path.join(profiles_data_dir, profile_name)
        os.makedirs(profile_dest_dir, exist_ok=True)

        # 1. Copy SOUL.md from template
        soul_src = os.path.join(templates_dir, profile_name, "SOUL.md")
        soul_dest = os.path.join(profile_dest_dir, "SOUL.md")
        if os.path.exists(soul_src):
            shutil.copy(soul_src, soul_dest)

        # 2. Generate config.yaml dynamically from env values
        config_yaml = generate_config_yaml(profile_name, schema, config)
        config_dest = os.path.join(profile_dest_dir, "config.yaml")
        with open(config_dest, "w") as cf:
            cf.write(config_yaml)

        # 3. Write profile .env
        token = config.get(schema["telegram_key"], "")
        profile_env_path = os.path.join(profile_dest_dir, ".env")
        with open(profile_env_path, "w") as pf:
            pf.write(f"OPENROUTER_API_KEY={openrouter_key}\n")
            pf.write(f"ANTHROPIC_API_KEY={anthropic_key}\n")
            pf.write(f"GITHUB_TOKEN={github_token}\n")
            pf.write(f"GIT_AUTHOR_NAME={git_name}\n")
            pf.write(f"GIT_AUTHOR_EMAIL={git_email}\n")
            pf.write(f"TELEGRAM_BOT_TOKEN={token}\n")
            pf.write(f"TELEGRAM_ALLOWED_USER_IDS={allowed_users}\n")
            pf.write(f"HERMES_HOME=/opt/data/profiles/{profile_name}\n")

        print(f"[+] {profile_name}")
        print(f"    model    : {config.get(schema['model_default'], '(default)')}")
        if schema.get("model_execution"):
            print(
                f"    execution: {config.get(schema['model_execution'], '(fallback to default)')}"
            )
        print(f"    reasoning: {config.get(schema['reasoning_effort'], 'medium')}")

    print("\n[✓] All profiles generated. Start with: docker compose up -d")


if __name__ == "__main__":
    main()
