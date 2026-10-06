#!/usr/bin/env bash
# TASK-04: Dynamic Student Lab Classifier & README Indexer

BASE_DIR="$HOME/secops"
DOCS_DIR="$BASE_DIR/docs"

echo "🔍 Sorting and indexing lab documentation..."

# Auto-sort coursework and cert files
find "$BASE_DIR" -maxdepth 2 -type f \( -iname "*wgu*" -o -iname "*coursework*" \) -exec mv {} "$DOCS_DIR/wgu_coursework/" \; 2>/dev/null
find "$BASE_DIR" -maxdepth 2 -type f \( -iname "*cert*" -o -iname "*lab*" \) -exec mv {} "$DOCS_DIR/cert_labs/" \; 2>/dev/null

# Generate README Indexer
echo "# SecOps Lab & Coursework Index" > "$DOCS_DIR/README.md"
echo "Updated: $(date)" >> "$DOCS_DIR/README.md"
echo "" >> "$DOCS_DIR/README.md"
echo "## 📚 WGU Coursework" >> "$DOCS_DIR/README.md"
ls -1 "$DOCS_DIR/wgu_coursework" 2>/dev/null | sed 's/^/- /' >> "$DOCS_DIR/README.md"
echo "" >> "$DOCS_DIR/README.md"
echo "## 🛡️ Certification Labs" >> "$DOCS_DIR/README.md"
ls -1 "$DOCS_DIR/cert_labs" 2>/dev/null | sed 's/^/- /' >> "$DOCS_DIR/README.md"

echo "✅ TASK-04 Execution Complete: Documentation indexed at $DOCS_DIR/README.md"
