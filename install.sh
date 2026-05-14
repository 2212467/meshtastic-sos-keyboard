#!/bin/bash

set -e

echo "🚀 Installing SOS Meshtastic Keyboard..."

# =========================
# USER + PATHS
# =========================

USER_NAME=$(whoami)
USER_HOME=$HOME

APP_DIR="$USER_HOME/sos-keyboard"

echo "👤 User: $USER_NAME"
echo "📁 Install dir: $APP_DIR"

# =========================
# SYSTEM DEPENDENCIES
# =========================

echo "📦 Installing system dependencies..."

sudo apt update

sudo apt install -y \
python3 \
python3-venv \
python3-pip \
git \
gpiod \
python3-libgpiod

sudo usermod -aG dialout,gpio $USER_NAME

# =========================
# CLONE / UPDATE
# =========================

if [ -d "$APP_DIR/.git" ]; then

    echo "🔄 Updating existing installation..."

    cd "$APP_DIR"
    git pull

else

    echo "⬇️ Cloning repository..."

    git clone https://github.com/2212467/meshtastic-sos-keyboard.git "$APP_DIR"

fi

cd "$APP_DIR"

# =========================
# CONFIG FILE
# =========================

if [ ! -f "$APP_DIR/config.py" ]; then

    echo "⚙️ Creating config.py"

    cp "$APP_DIR/config.py.example" "$APP_DIR/config.py"

fi

# =========================
# PYTHON VENV
# =========================

echo "🐍 Setting up Python environment..."

if [ ! -d "$APP_DIR/myenv" ]; then

    python3 -m venv "$APP_DIR/myenv"

fi

"$APP_DIR/myenv/bin/pip" install --upgrade pip wheel setuptools

"$APP_DIR/myenv/bin/pip" install -r "$APP_DIR/requirements.txt"

# =========================
# SYSTEMD USER SERVICE
# =========================

echo "⚙️ Creating systemd service..."

mkdir -p "$USER_HOME/.config/systemd/user"

cat > "$USER_HOME/.config/systemd/user/sos-keyboard.service" <<EOF
[Unit]
Description=SOS Meshtastic Keyboard
After=default.target

[Service]
Type=simple

WorkingDirectory=$APP_DIR

ExecStart=$APP_DIR/myenv/bin/python $APP_DIR/sos_keyboard.py

Restart=always
RestartSec=3

Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
EOF

# =========================
# ENABLE SERVICE
# =========================

echo "🔌 Enabling auto-start..."

export XDG_RUNTIME_DIR="/run/user/$(id -u)"

systemctl --user daemon-reload
systemctl --user enable sos-keyboard.service
systemctl --user restart sos-keyboard.service

loginctl enable-linger $USER_NAME || true

# =========================
# TEST MESHTASTIC
# =========================

echo "📡 Testing Meshtastic connection..."

if meshtastic --info > /dev/null 2>&1; then

    echo "✅ Meshtastic device detected"

else

    echo "⚠️ WARNING: No Meshtastic device detected"

fi

# =========================
# DONE
# =========================

echo ""
echo "✅ INSTALL COMPLETE"
echo ""
echo "⚠️ Reboot recommended to apply GPIO permissions."
echo ""
echo "After reboot:"
echo "systemctl --user status sos-keyboard"
echo ""