#!/bin/bash

set -e

# Clean the build folder
rm -rf build/*

# Create the build directory structure
mkdir -p build/distributions build/sites

# 1. Find all manifest.json files and merge them into manifests.json
find Widgets -type f -name 'manifest.json' -print0 | xargs -0 jq -s 'map(if type == "array" then . else [.] end) | add' > build/manifests.json

# 2. Create widget distribution packages and site data for each manifest.json found
find Widgets -type f -name 'manifest.json' | while read -r manifest; do
    widget_dir=$(dirname "$manifest")
    widget_name=$(basename "$widget_dir")
    echo "Processing $widget_name..."

    # Create a zip file for the widget, skipping the top-level folder
    (cd "$widget_dir" && zip -rq "/app/build/distributions/${widget_name}.zip" .)

    # 3. Create site data for the widget
    site_dir="build/sites/$widget_name"
    mkdir -p "$site_dir"

    # Find and process images and markdown files.
    cover_image=$(find "$widget_dir" -maxdepth 2 -name "cover.png" | head -n 1)
    readme_file=$(find "$widget_dir" -maxdepth 2 -name "README.md" | head -n 1)

    if [ -f "$cover_image" ]; then
        echo "  - Converting cover image..."
        # Create a larger version of the cover image
        convert "$cover_image" -resize 460x300\! "${site_dir}/${widget_name}_460x300.png"
        # Create a smaller thumbnail version
        convert "$cover_image" -resize 130x100\! "${site_dir}/${widget_name}_130x100.png"
    else
        echo "  - WARNING: No cover.png found for $widget_name"
    fi

    if [ -f "$readme_file" ]; then
        echo "  - Copying README.md..."
        cp "$readme_file" "${site_dir}/${widget_name}.md"
    else
        echo "  - WARNING: No README.md found for $widget_name"
    fi
done

echo "Build process completed."
