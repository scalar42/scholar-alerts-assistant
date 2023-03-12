import time


class Formatter:
    def __init__(self):
        pass

    def convert_to_html(self, entries):
        html_start = "<html><body>"
        html_end = "</body></html>"
        content = f"<h2>Scholar Alerts Assistant</h2>"
        content += '<h4>&mdash; An automation tool by Scalar42 <a href="https://github.com/scalar42/scholar-alerts-assistant" target="_blank">[Code]</a><h4>'
        content += f'<h3>[Stats] {len(entries)} unique papers found, updated at {time.strftime("%Y-%m-%d %H:%M")}.</h3>'
        for index, entry in enumerate(entries):
            # title with link
            content += (
                f'<div style="margin-bottom: 1em;"><b>[{index+1}/{len(entries)}] </b><a href="'
                + entry.source_link
                + '"><b>'
                + entry.title
                + "</b></a>"
            )
            # star link button
            content += (
                '<a href="'
                + entry.star_link
                + '" style="margin-left: 0.5em;">'
                + "<button>Star</button>"
                + "</a><br>"
            )
            # authr and publication
            content += entry.authr_and_pub + "<br>"
            # abstract
            content += entry.abstract + "<br> </div>"

        return html_start + content + html_end
