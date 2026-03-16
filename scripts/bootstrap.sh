#!/usr/bin/env bash

set -euo pipefail



SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

SKILLS_SOURCE="$REPO_ROOT/skills"



TARGET="both"

SCOPE="global"

PROJECT_DIR=""

DRY_RUN=false

MODE="symlink"

FORCE=false

LIST_ONLY=false

SKILLS_FILTER=""

TYPE_FILTER=""

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

INSTALLED_COUNT=0

SKIPPED_COUNT=0

UNCHANGED_COUNT=0

SELECTED_SKILLS=""



usage() {

  cat <<'EOF'

Usage:

  ./scripts/bootstrap.sh [options]



Options:

  --target <codex|claude|gemini|both> Which tool to install for (default: both)

  --scope <global|project>        Install scope (default: global)

  --project-dir <path>            Required when --scope project

  --skills <a,b,c>                Install only specific skill names

  --type <economists,general>     Install all skills under one or more types

  --list                          Print available skills and types, then exit

  --copy                          Copy skills instead of symlink

  --force                         Replace conflicting paths (default: skip conflicts)

  --dry-run                       Print actions without applying

  -h, --help                      Show this help message



Notes:

  - If --skills/--type are not provided, all skills are installed.

  - If both --skills and --type are provided, the selection is a union.

  - Skill discovery supports:

      skills/<skill>/SKILL.md

      skills/<type>/<skill>/SKILL.md

EOF

}



log() {

  printf '[bootstrap] %s\n' "$1"

}



run() {

  if [[ "$DRY_RUN" == "true" ]]; then

    printf '[dry-run] %s\n' "$*"

  else

    "$@"

  fi

}



ensure_dir() {

  local dir="$1"

  if [[ ! -d "$dir" ]]; then

    run mkdir -p "$dir"

  fi

}



csv_to_lines() {

  printf '%s\n' "$1" | tr ',' '\n' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | sed '/^$/d'

}



discover_skill_entries() {

  local skill_md=""

  local dir=""

  local rel=""

  local skill_name=""

  local skill_type=""

  local base_dir_name=""



  # Use a temporary file to store entries and ensure uniqueness

  local tmp_entries

  tmp_entries=$(mktemp)



  while IFS= read -r skill_md; do

    dir="$(dirname "$skill_md")"

    base_dir_name="$(basename "$dir")"

    

    # If the SKILL.md is inside a tool-specific folder, the skill root is the parent

    if [[ "$base_dir_name" == "claude" || "$base_dir_name" == "gemini" || "$base_dir_name" == "codex" ]]; then

      dir="$(dirname "$dir")"

    fi

    

    rel="${dir#$SKILLS_SOURCE/}"



    case "$rel" in

      groups|groups/*|""|.)

        continue

        ;;

    esac



    skill_name="$(basename "$dir")"

    skill_type="uncategorized"

    if [[ "$rel" == */* ]]; then

      skill_type="${rel%%/*}"

    fi



    printf '%s|%s|%s|%s\n' "$skill_name" "$skill_type" "$dir" "$rel" >> "$tmp_entries"

  done < <(find "$SKILLS_SOURCE" -type f -name 'SKILL.md' | sort)



  # Output unique entries based on skill_name

  sort -u -t'|' -k1,1 "$tmp_entries"

  rm -f "$tmp_entries"

}



detect_duplicate_skill_names() {

  local dups=""

  dups="$(discover_skill_entries | cut -d'|' -f1 | sort | uniq -d)"

  if [[ -n "$dups" ]]; then

    printf 'Error: duplicate skill directory names detected. Skill names must be globally unique:\n' >&2

    printf '%s\n' "$dups" | sed 's/^/  - /' >&2

    exit 1

  fi

}



list_available_skills() {

  discover_skill_entries | cut -d'|' -f1 | sort -u

}



list_available_types() {

  discover_skill_entries | cut -d'|' -f2 | sort -u

}



skill_exists() {

  local skill_name="$1"

  local current=""

  while IFS= read -r current; do

    if [[ "$current" == "$skill_name" ]]; then

      return 0

    fi

  done < <(list_available_skills)

  return 1

}



type_exists() {

  local skill_type="$1"

  local current=""

  while IFS= read -r current; do

    if [[ "$current" == "$skill_type" ]]; then

      return 0

    fi

  done < <(list_available_types)

  return 1

}



skills_for_type() {

  local wanted_type="$1"

  discover_skill_entries | awk -F'|' -v t="$wanted_type" '$2 == t { print $1 }' | sort -u

}



skill_dir_for_name() {

  local wanted_skill="$1"

  local skill_name=""

  local _skill_type=""

  local skill_dir=""

  local _rel=""



  while IFS='|' read -r skill_name _skill_type skill_dir _rel; do

    if [[ "$skill_name" == "$wanted_skill" ]]; then

      printf '%s\n' "$skill_dir"

      return 0

    fi

  done < <(discover_skill_entries)



  return 1

}



print_catalog() {

  local found_any=false



  echo "Available types:"

  if list_available_types | grep -q .; then

    while IFS= read -r t; do

      echo "  - $t"

    done < <(list_available_types)

  else

    echo "  (none)"

  fi



  echo ""

  echo "Available skills:"

  while IFS='|' read -r skill_name skill_type _abs rel; do

    found_any=true

    echo "  - $skill_name (type: $skill_type, path: skills/$rel)"

  done < <(discover_skill_entries)



  if [[ "$found_any" == "false" ]]; then

    echo "  (none)"

  fi

}



backup_path() {

  local path="$1"

  local backup="${path}.backup.${TIMESTAMP}"

  log "Backing up existing path: $path -> $backup"

  run mv "$path" "$backup"

}



install_skill_symlink() {

  local src="$1"

  local dest="$2"



  ensure_dir "$(dirname "$dest")"



  if [[ -L "$dest" ]]; then

    local current=""

    current="$(readlink "$dest")"

    if [[ "$current" == "$src" ]]; then

      log "Already linked: $dest -> $src"

      ((UNCHANGED_COUNT += 1))

      return 0

    fi

    if [[ "$FORCE" == "true" ]]; then

      log "Replacing symlink: $dest (was -> $current)"

      run rm "$dest"

    else

      log "Skipping conflict: $dest already points to $current (use --force to replace)"

      ((SKIPPED_COUNT += 1))

      return 0

    fi

  elif [[ -e "$dest" ]]; then

    if [[ "$FORCE" == "true" ]]; then

      backup_path "$dest"

    else

      log "Skipping conflict: $dest already exists (use --force to replace)"

      ((SKIPPED_COUNT += 1))

      return 0

    fi

  fi



  log "Linking: $dest -> $src"

  run ln -s "$src" "$dest"

  ((INSTALLED_COUNT += 1))

}



install_skill_copy() {

  local src="$1"

  local dest="$2"



  if [[ -e "$dest" ]]; then

    if [[ "$FORCE" == "true" ]]; then

      backup_path "$dest"

    else

      log "Skipping conflict: $dest already exists (copy mode does not overwrite without --force)"

      ((SKIPPED_COUNT += 1))

      return 0

    fi

  fi



  ensure_dir "$dest"



  if command -v rsync >/dev/null 2>&1; then

    log "Copying with rsync: $src -> $dest"

    run rsync -a "$src/" "$dest/"

  else

    log "Copying with cp: $src -> $dest"

    run cp -R "$src/." "$dest/"

  fi

  ((INSTALLED_COUNT += 1))

}



append_csv_value() {

  local existing="$1"

  local value="$2"

  if [[ -z "$existing" ]]; then

    printf '%s' "$value"

  else

    printf '%s,%s' "$existing" "$value"

  fi

}



validate_filters() {

  local missing_skills=""

  local missing_types=""

  local skill_name=""

  local skill_type=""

  local available=""



  if [[ -n "$SKILLS_FILTER" ]]; then

    while IFS= read -r skill_name; do

      if ! skill_exists "$skill_name"; then

        missing_skills="${missing_skills}${skill_name}"$'\n'

      fi

    done < <(csv_to_lines "$SKILLS_FILTER")

  fi



  if [[ -n "$TYPE_FILTER" ]]; then

    while IFS= read -r skill_type; do

      if ! type_exists "$skill_type"; then

        missing_types="${missing_types}${skill_type}"$'\n'

      fi

    done < <(csv_to_lines "$TYPE_FILTER")

  fi



  if [[ -n "$missing_skills" ]]; then

    printf 'Error: unknown skill(s):\n' >&2

    printf '%s' "$missing_skills" | sed '/^$/d' | sed 's/^/  - /' >&2

    printf 'Run --list to see valid skills.\n' >&2

    exit 1

  fi



  if [[ -n "$missing_types" ]]; then

    printf 'Error: unknown type(s):\n' >&2

    printf '%s' "$missing_types" | sed '/^$/d' | sed 's/^/  - /' >&2

    available="$(list_available_types | paste -sd ',' -)"

    if [[ -n "$available" ]]; then

      printf 'Available types: %s\n' "$available" >&2

    fi

    exit 1

  fi

}



collect_selected_skills() {

  local collected=""

  local skill_name=""

  local skill_type=""



  if [[ -z "$SKILLS_FILTER" && -z "$TYPE_FILTER" ]]; then

    SELECTED_SKILLS="$(list_available_skills)"

    return

  fi



  if [[ -n "$SKILLS_FILTER" ]]; then

    while IFS= read -r skill_name; do

      collected="${collected}${skill_name}"$'\n'

    done < <(csv_to_lines "$SKILLS_FILTER")

  fi



  if [[ -n "$TYPE_FILTER" ]]; then

    while IFS= read -r skill_type; do

      while IFS= read -r skill_name; do

        collected="${collected}${skill_name}"$'\n'

      done < <(skills_for_type "$skill_type")

    done < <(csv_to_lines "$TYPE_FILTER")

  fi



  SELECTED_SKILLS="$(printf '%s' "$collected" | sed '/^$/d' | sort -u)"



  if [[ -z "$SELECTED_SKILLS" ]]; then

    printf 'Error: selection produced no skills.\n' >&2

    exit 1

  fi

}



install_for_tool() {

  local tool="$1"

  local base=""

  local skills_dest=""

  local skill_name=""

  local skill_src=""

  local skill_dest=""



  if [[ "$SCOPE" == "global" ]]; then

    case "$tool" in

      codex) base="$HOME/.codex" ;;

      claude) base="$HOME/.claude" ;;

      gemini) base="$HOME/.gemini" ;;

    esac

  else

    case "$tool" in

      codex) base="$PROJECT_DIR/.codex" ;;

      claude) base="$PROJECT_DIR/.claude" ;;

      gemini) base="$PROJECT_DIR/.gemini" ;;

    esac

  fi



  skills_dest="$base/skills"

  ensure_dir "$skills_dest"



  while IFS= read -r skill_name; do

    [[ -z "$skill_name" ]] && continue

    skill_src="$(skill_dir_for_name "$skill_name")"

    

    # If a tool-specific subdirectory exists, use it as the source

    if [[ -d "$skill_src/$tool" && -f "$skill_src/$tool/SKILL.md" ]]; then

      skill_src="$skill_src/$tool"

    fi

    

    skill_dest="$skills_dest/$skill_name"

    if [[ "$MODE" == "symlink" ]]; then

      install_skill_symlink "$skill_src" "$skill_dest"

    else

      install_skill_copy "$skill_src" "$skill_dest"

    fi

  done < <(printf '%s\n' "$SELECTED_SKILLS")

}



while [[ $# -gt 0 ]]; do

  case "$1" in

    --target)

      TARGET="${2:-}"

      shift 2

      ;;

    --scope)

      SCOPE="${2:-}"

      shift 2

      ;;

    --project-dir)

      PROJECT_DIR="${2:-}"

      shift 2

      ;;

    --skills)

      SKILLS_FILTER="$(append_csv_value "$SKILLS_FILTER" "${2:-}")"

      shift 2

      ;;

    --type)

      TYPE_FILTER="$(append_csv_value "$TYPE_FILTER" "${2:-}")"

      shift 2

      ;;

    --list)

      LIST_ONLY=true

      shift

      ;;

    --copy)

      MODE="copy"

      shift

      ;;

    --force)

      FORCE=true

      shift

      ;;

    --dry-run)

      DRY_RUN=true

      shift

      ;;

    -h|--help)

      usage

      exit 0

      ;;

    *)

      printf 'Unknown argument: %s\n\n' "$1" >&2

      usage >&2

      exit 1

      ;;

  esac

done



if [[ ! -d "$SKILLS_SOURCE" ]]; then

  printf 'Error: skills directory not found at %s\n' "$SKILLS_SOURCE" >&2

  exit 1

fi



detect_duplicate_skill_names



if [[ "$LIST_ONLY" == "true" ]]; then

  print_catalog

  exit 0

fi



if [[ "$TARGET" != "codex" && "$TARGET" != "claude" && "$TARGET" != "gemini" && "$TARGET" != "both" ]]; then

  printf 'Error: --target must be codex, claude, gemini, or both\n' >&2

  exit 1

fi



if [[ "$SCOPE" != "global" && "$SCOPE" != "project" ]]; then

  printf 'Error: --scope must be global or project\n' >&2

  exit 1

fi



if [[ "$SCOPE" == "project" ]]; then

  if [[ -z "$PROJECT_DIR" ]]; then

    printf 'Error: --project-dir is required when --scope project\n' >&2

    exit 1

  fi

  if [[ ! -d "$PROJECT_DIR" ]]; then

    printf 'Error: --project-dir does not exist: %s\n' "$PROJECT_DIR" >&2

    exit 1

  fi

fi



validate_filters

collect_selected_skills



log "Repo root: $REPO_ROOT"

log "Skills source: $SKILLS_SOURCE"

log "Target: $TARGET"

log "Scope: $SCOPE"

log "Mode: $MODE"

log "Force: $FORCE"

if [[ "$SCOPE" == "project" ]]; then

  log "Project dir: $PROJECT_DIR"

fi

if [[ -n "$SKILLS_FILTER" ]]; then

  log "Skills filter: $SKILLS_FILTER"

fi

if [[ -n "$TYPE_FILTER" ]]; then

  log "Type filter: $TYPE_FILTER"

fi

log "Selected skill count: $(printf '%s\n' "$SELECTED_SKILLS" | sed '/^$/d' | wc -l | tr -d ' ')"



if [[ "$TARGET" == "codex" || "$TARGET" == "both" ]]; then

  install_for_tool "codex"

fi



if [[ "$TARGET" == "claude" || "$TARGET" == "both" ]]; then

  install_for_tool "claude"

fi



if [[ "$TARGET" == "gemini" || "$TARGET" == "both" ]]; then

  install_for_tool "gemini"

fi



log "Installed: $INSTALLED_COUNT"

log "Unchanged: $UNCHANGED_COUNT"

log "Skipped: $SKIPPED_COUNT"

log "Done."