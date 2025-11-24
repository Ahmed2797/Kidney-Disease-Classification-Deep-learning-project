# from pathlib import Path

# CONFIG_YAML_FILE = Path("yamlfile/config.yaml")
# PARAM_YAML_FILE = Path("yamlfile/param.yaml")
# SECRET_YAML_FILE = Path("yamlfile/secrets.yaml")



from pathlib import Path

def get_project_root():
    path = Path(__file__).resolve()
    for parent in path.parents:
        # Detect project root by checking for setup.py
        if (parent / "setup.py").exists():
            return parent
    return Path.cwd()  # fallback

ROOT_DIR = get_project_root()

CONFIG_YAML_FILE = ROOT_DIR / "yamlfile" / "config.yaml"
PARAM_YAML_FILE  = ROOT_DIR / "yamlfile" / "param.yaml"
SECRET_YAML_FILE = ROOT_DIR / "yamlfile" / "secrets.yaml"
