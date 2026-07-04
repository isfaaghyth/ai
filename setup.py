import os
import shutil

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    env_example = os.path.join(root_dir, 'env.example')
    env_file = os.path.join(root_dir, '.env')

    if not os.path.exists(env_file):
        shutil.copy(env_example, env_file)
        print("[!] Created `.env` from `env.example`.")
        print("[!] Please edit the `.env` file at the root of the project to add your API keys and Telegram tokens, then run this setup script again.")
        return

    # Parse .env
    config = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()

    profiles = {
        'dev_kotlin_mobile': 'TELEGRAM_TOKEN_DEV_KOTLIN_MOBILE',
        'dev_golang_backend': 'TELEGRAM_TOKEN_DEV_GOLANG_BACKEND',
        'dev_frontend_react': 'TELEGRAM_TOKEN_DEV_FRONTEND_REACT',
        'daily_general': 'TELEGRAM_TOKEN_DAILY_GENERAL',
        'daily_learning_buddy': 'TELEGRAM_TOKEN_DAILY_LEARNING_BUDDY'
    }

    data_dir = os.path.join(root_dir, 'data')
    profiles_data_dir = os.path.join(data_dir, 'profiles')
    templates_dir = os.path.join(root_dir, 'templates')

    for profile_name, token_key in profiles.items():
        profile_template_dir = os.path.join(templates_dir, profile_name)
        profile_dest_dir = os.path.join(profiles_data_dir, profile_name)

        os.makedirs(profile_dest_dir, exist_ok=True)

        # Copy SOUL.md
        soul_src = os.path.join(profile_template_dir, 'SOUL.md')
        soul_dest = os.path.join(profile_dest_dir, 'SOUL.md')
        if os.path.exists(soul_src):
            shutil.copy(soul_src, soul_dest)

        # Copy config.yaml
        config_src = os.path.join(profile_template_dir, 'config.yaml')
        config_dest = os.path.join(profile_dest_dir, 'config.yaml')
        if os.path.exists(config_src):
            shutil.copy(config_src, config_dest)

        # Write .env for this profile
        profile_env_file = os.path.join(profile_dest_dir, '.env')
        token = config.get(token_key, '')
        allowed_users = config.get('TELEGRAM_ALLOWED_USER_IDS', '')
        openrouter_key = config.get('OPENROUTER_API_KEY', '')
        anthropic_key = config.get('ANTHROPIC_API_KEY', '')

        # Standardizing defaults or fallbacks
        if not openrouter_key or openrouter_key == "your_openrouter_api_key_here":
            openrouter_key = ""
        if not anthropic_key or anthropic_key == "your_anthropic_api_key_here":
            anthropic_key = ""

        with open(profile_env_file, 'w') as pf:
            pf.write(f"OPENROUTER_API_KEY={openrouter_key}\n")
            pf.write(f"ANTHROPIC_API_KEY={anthropic_key}\n")
            pf.write(f"TELEGRAM_BOT_TOKEN={token}\n")
            pf.write(f"TELEGRAM_ALLOWED_USER_IDS={allowed_users}\n")
            pf.write(f"HERMES_HOME=/opt/data/profiles/{profile_name}\n")

        print(f"[+] Initialized profile: {profile_name}")

    print("\n[✓] Setup complete! Once you fill in your `.env` keys, start the containers with: docker compose up -d")

if __name__ == '__main__':
    main()
