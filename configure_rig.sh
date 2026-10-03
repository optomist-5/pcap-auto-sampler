#!/usr/bin/env zsh

echo "==================================================================="
echo "          SECOPS RIG & ENVIRONMENT CONFIGURATION SETUP            "
echo "==================================================================="
echo ""

# 1. Working Directory
default_dir="$HOME/secops"
read "user_dir?1. Enter your primary working directory [$default_dir]: "
user_dir="${user_dir:-$default_dir}"

# Expand ~ if present
eval user_dir=$user_dir

if [[ ! -d "$user_dir" ]]; then
    echo "   [!] Directory $user_dir does not exist. Creating it now..."
    mkdir -p "$user_dir"
fi

# 2. Local Timezone
default_tz="America/Los_Angeles"
read "user_tz?2. Enter your primary timezone [$default_tz]: "
user_tz="${user_tz:-$default_tz}"

# 3. Primary Google Account Email
default_email="mquija9@noviascentialabs.com"
read "user_email?3. Enter your primary Google Workspace email [$default_email]: "
user_email="${user_email:-$default_email}"

# 4. Python Interpreter / Virtual Environment Check
echo ""
echo "4. Checking Python Virtual Environment status..."
if [[ -n "$VIRTUAL_ENV" ]]; then
    python_path="$(which python3)"
    echo "   [✓] Active Virtual Environment Detected: $VIRTUAL_ENV"
    echo "   [✓] Using Python Binary: $python_path"
else
    echo "   [!] WARNING: No active virtual environment detected."
    if [[ -f "$user_dir/venv/bin/activate" ]]; then
        echo "   [*] Found virtual environment at $user_dir/venv. Activating now..."
        source "$user_dir/venv/bin/activate"
        python_path="$(which python3)"
    else
        python_path="$(which python3)"
        echo "   [*] Using system Python binary: $python_path"
    fi
fi

# Save Configuration to Environment File
config_file="$user_dir/rig_config.env"
cat << EOC > "$config_file"
# SecOps Rig Environment Configuration
SECOPS_DIR="$user_dir"
SECOPS_TZ="$user_tz"
SECOPS_EMAIL="$user_email"
SECOPS_PYTHON="$python_path"
EOC

echo ""
echo "==================================================================="
echo "              CONFIGURATION SAVED SUCCESSFULLY!                    "
echo "==================================================================="
echo " Saved to: $config_file"
echo ""
echo " Confirmed Parameters:"
echo " - Working Dir : $user_dir"
echo " - Timezone    : $user_tz"
echo " - Email       : $user_email"
echo " - Python Path : $python_path"
echo "==================================================================="
