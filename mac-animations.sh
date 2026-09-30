#!/usr/bin/env bash
#
# mac-animations.sh — turn macOS UI animations off (or restore the defaults).
#
# Usage:
#   ./mac-animations.sh disable [--no-restart] [--dry-run]
#   ./mac-animations.sh restore [--no-restart] [--dry-run]
#
# Source list: https://apple.stackexchange.com/questions/14001
# Some keys are reportedly ignored on recent macOS releases; writing them is harmless.

set -u

# Each entry is: domain | key | type | value
# NSGlobalDomain is the same as `defaults -g`: it applies to all apps.
SETTINGS=(
  # --- System-wide (all apps) -------------------------------------------

  # Animation when opening and closing windows and popovers.
  "NSGlobalDomain|NSAutomaticWindowAnimationsEnabled|-bool|false"

  # Smooth (animated) scrolling.
  "NSGlobalDomain|NSScrollAnimationEnabled|-bool|false"

  # Animation for sheets (Save/Print dialogs), resizing preference windows
  # and zooming windows. Set to 0.001 rather than 0 because 0 is reportedly
  # ignored. Some users report this key does nothing on newer macOS.
  "NSGlobalDomain|NSWindowResizeTime|-float|0.001"

  # Animation when opening and closing Quick Look previews (Space bar).
  "NSGlobalDomain|QLPanelAnimationDuration|-float|0"

  # Rubber-band "bounce" when scrolling past the edge of content.
  # Does not affect web views.
  "NSGlobalDomain|NSScrollViewRubberbanding|-bool|false"

  # Window resize animation around the document version browser
  # (File > Revert To > Browse All Versions). Also covered by
  # NSWindowResizeTime.
  "NSGlobalDomain|NSDocumentRevisionsWindowTransformAnimation|-bool|false"

  # Animation when the toolbar or menu bar slides in and out in full screen.
  "NSGlobalDomain|NSToolbarFullScreenAnimationDuration|-float|0"

  # Animation when scrolling column views (e.g. Finder column view).
  "NSGlobalDomain|NSBrowserColumnAnimationSpeedMultiplier|-float|0"

  # --- Dock ---------------------------------------------------------------

  # Duration of the slide animation when an auto-hidden Dock shows or hides.
  "com.apple.dock|autohide-time-modifier|-float|0"

  # Delay before an auto-hidden Dock starts to appear.
  "com.apple.dock|autohide-delay|-float|0"

  # Mission Control show/hide animation. Reported not to work on
  # Big Sur and Monterey; unconfirmed on newer releases.
  "com.apple.dock|expose-animation-duration|-float|0"

  # --- Finder -------------------------------------------------------------

  # Finder animations, such as opening Get Info panels. Finder relaunches
  # when this script runs.
  "com.apple.finder|DisableAllAnimations|-bool|true"

  # --- Mail ---------------------------------------------------------------

  # Animation when sending a message.
  "com.apple.Mail|DisableSendAnimations|-bool|true"

  # Animation when opening a reply window.
  "com.apple.Mail|DisableReplyAnimations|-bool|true"
)

usage() {
  sed -n '3,9p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-1}"
}

MODE="${1:-}"
[ -n "$MODE" ] && shift
RESTART=1
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --no-restart) RESTART=0 ;;
    --dry-run)    DRY_RUN=1 ;;
    -h|--help)    usage 0 ;;
    *) echo "Unknown option: $arg" >&2; usage 1 ;;
  esac
done

case "$MODE" in
  disable|restore) ;;
  -h|--help) usage 0 ;;
  *) usage 1 ;;
esac

if [ "$DRY_RUN" -eq 0 ] && [ "$(uname -s)" != "Darwin" ]; then
  echo "This script only works on macOS." >&2
  exit 1
fi

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '[dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

for entry in "${SETTINGS[@]}"; do
  IFS='|' read -r domain key type value <<< "$entry"
  if [ "$MODE" = "disable" ]; then
    run defaults write "$domain" "$key" "$type" "$value"
  else
    # Deleting a key that was never set prints an error; that's fine.
    if [ "$DRY_RUN" -eq 1 ]; then
      run defaults delete "$domain" "$key"
    else
      defaults delete "$domain" "$key" 2>/dev/null || true
    fi
  fi
done

if [ "$RESTART" -eq 1 ]; then
  # Dock and Finder pick up changes on relaunch; they restart automatically.
  run killall Dock
  run killall Finder
fi

echo "Done (${MODE})."
echo "Notes:"
echo "  - Quit and reopen Mail for its settings to apply."
echo "  - Other apps need a relaunch; a few settings may need a log out/in."
