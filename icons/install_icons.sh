#!/bin/bash
ICON_NAME="TuxKatana"
SIZES=(16 24 32 48 64 128 256)
SRC_DIR=$(pwd)
DEST_DIR="/usr/local/share/icons/hicolor"
install_icons() {
    for SIZE in "${SIZES[@]}"; do
        SRC_FILE="${SRC_DIR}/${ICON_NAME}_${SIZE}.png"
        DEST_FILE="${DEST_DIR}/${SIZE}x${SIZE}/apps/${ICON_NAME}.png"
        mkdir -p "$(dirname "$DEST_FILE")"
        ln -sf "$SRC_FILE" "$DEST_FILE"
        echo "Added Symbolic link : $SRC_FILE to $DEST_FILE"
    done
    gtk-update-icon-cache
    echo "Icons Install terminated"
}
uninstall_icons() {
    for SIZE in "${SIZES[@]}"; do
        DEST_PATH="${DEST_DIR}/${SIZE}x${SIZE}/apps/${ICON_NAME}.png"
        if [ -L "$DEST_PATH" ]; then
            rm "$DEST_PATH"
            echo "Removed SymLink : $DEST_PATH"
        fi
    done
    gtk-update-icon-cache
    echo "Uninstall OK."
}
echo "1) Install icons"
echo "2) Remove icons symlinks"
echo "3) Quit"
read -p "Choice [1-3] : " CHOICE

case $CHOICE in
    1)
        echo "Install icons..."
        install_icons
        ;;
    2)
        echo "Uninstall icons..."
        uninstall_icons
        ;;
    3)
        exit 0
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac

