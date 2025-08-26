# So You Want to Add a Widget to the Hub

Make sure you replace all text in the angle brackets <>.

## Steps
* Fork this repository
* Clone your fork
```
git clone https://github.com/<your_user_name>/Public-BAR-Widgets
cd Public-BAR-Widgets
```

* Add your widget as a submodule
```
git submodule add https://github.com/<your_user_name>/<your_widget_repo> Widgets/<your_widget_repo>
```

* Add a cover image to `Public-Bar-Widgets/widget_cover_images/<your_widget_name>.png`
* Add a metadata file at `Public-Bar-Widgets/widget_metadata/<your_widget_name>.json`
```
{
	"display_name": "<your_widget_name>",
	"author": "<your_name_nickname_or_tag>",
	"submodule_path": "Widgets/<your_widget_repo>",
	"discord_link": "<link_to_discord_post_about_your_widget>",
	"description": "A short description",
	"cover_image_path": "widget_cover_images/<your_widget_name>.png",
	"entry_point": "/"
}
```

* Push your changes to the fork
```
git add *
git commit -m "Add <your_widget_name> to the widget hub."
git push
```

* In github click `create Pull Request`

## Notes on the metadata format
TODO
