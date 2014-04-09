# Beets Web plugin for Rhythmbox

## Requirements

* Rhythmbox 3.0.2+ (http://www.rhythmbox.org)
* Beets (http://beets.radbox.org/)
  * Web Plugin (http://beets.readthedocs.org/en/latest/plugins/web.html)

## Installation

    mkdir -p ~/.local/share/rhythmbox/plugins
    cd ~/.local/share/rhythmbox/plugins
    git clone https://github.com/BHSPitMonkey/rhythmbox-beets-web.git
    mv rhythmbox-beets-web beets-web
    xdg-open beets-web/beets/__init__.py

1. Find the line that starts with `BEETS_WEB_URL =`
2. Replace the URL shown with one that matches your Beets Web setup
3. Save your changes and exit your editor
4. Open Rhythmbox
5. From the menu, select **Plugins**
6. Activate the checkbox next to "Beets Web Library"

You should now have a "Beets Library" entry in the sidebar.

## License

Something suitable for a Rhythmbox plugin. I'm not sure yet.
