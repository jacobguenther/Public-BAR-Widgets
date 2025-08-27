#!/bin/bash

set -e

# Clean the build folder
rm -rf build/*

# Create the build directory structure
mkdir -p build/distributions build/sites

# 1. Find all manifest.json files and merge them into manifests.json
find Widgets -type f -name 'manifest.json' -print0 | xargs -0 jq -s 'map(if type == "array" then . else [.] end) | add' > build/manifests.json

# 2. Create widget distribution packages and site data for each manifest.json found

# Track processed widget names to avoid duplicates
declare -A processed_widgets

find Widgets -type f -name 'manifest.json' | while read -r manifest; do
    widget_dir=$(dirname "$manifest")
    widget_name=$(basename "$widget_dir")

    if [[ -n "${processed_widgets[$widget_name]}" ]]; then
        echo "ERROR: Duplicate widget_name '$widget_name' found. Exiting." >&2
        exit 1
    fi
    processed_widgets[$widget_name]=1

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
        # Create a larger version of the cover image, preserving aspect ratio and cropping as needed
        convert "$cover_image" -resize 460x300^ -gravity center -extent 460x300 "${site_dir}/${widget_name}_460x300.png"
        # Create a smaller thumbnail version, preserving aspect ratio and cropping as needed
        convert "$cover_image" -resize 325x100^ -gravity center -extent 325x100 "${site_dir}/${widget_name}_325x100.png"
    else
        echo "  - ERROR: No cover.png found for $widget_name" >&2
        exit 1
    fi

    if [ -f "$readme_file" ]; then
        echo "  - Copying README.md..."
        cp "$readme_file" "${site_dir}/${widget_name}.md"
    else
        echo "  - ERROR: No README.md found for $widget_name" >&2
        exit 1
    fi
done

echo "Build process completed."
