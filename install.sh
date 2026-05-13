#!/bin/bash

set -e

echo "🚀 Installing SOS Meshtastic Keyboard..."

# =========================
# 1. DETECT USER + HOME
# =========================
USER_NAME=$(whoami)
USER_HOME=$HOME

APP_DIR="$USER_HOME/sos-keyboard"

echo "👤 User: $USER_NAME"
echo "📁 Install dir: $APP_DIR"

# =========================
# 2. SYSTEM DEPENDENCIES
# =========================
echo "📦 Installing system dependencies..."

sudo apt update
sudo apt install -y python3-venv python3-pip git gpiod python3-libgpiod

# =========================
# 3. GET PROJECT
# =========================
if [ -d "$APP_DIR" ]; then
    echo "🔄 Updating existing installation..."
    cd "$APP_DIR"
    git pull
else
    echo "⬇️ Cloning repository..."
    git clone https://github.com/USER/sos-meshtastic-keyboard.git "$APP_DIR"
    cd "$APP_DIR"
fi

# =========================
# 4. PYTHON VENV
# =========================
echo "🐍 Creating virtual environment..."

python3 -m venv myenv

myenv/bin/pip install --upgrade pip
myenv/bin/pip install -r requirements.txt

# =========================
# 5. SYSTEMD USER SERVICE
# =========================
echo "⚙️ Creating systemd user service..."

mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/sos-keyboard.service <<EOF
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
# 6. ENABLE SERVICE
# =========================
echo "🔌 Enabling auto-start..."

systemctl --user daemon-reload
systemctl --user enable sos-keyboard.service

# garante que arranca sem login
loginctl enable-linger $USER_NAME || true

# =========================
# DONE
# =========================
echo ""
echo "✅ INSTALL COMPLETE"
echo ""
echo "▶ Run now:"
echo "   systemctl --user start sos-keyboard"
echo ""
echo "📊 Logs:"
echo "   journalctl --user -u sos-keyboard -f"