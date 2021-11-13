import datetime
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dataclasses import dataclass

PATH_TO_TEMPLATES = Path('TEMPLATES/')
PATH_TO_RESOURCES = Path('../generator/RESOURCES/')
PATH_TO_OUTPUT = Path('../docs/')
URL_ROOT = "https://signiffer.eu/"

link_to_homepage = "/"  # TODO: always / in production
html_file_suffix = ".html"


@dataclass()
class Page(object):
    title: str
    keywords: str
    description: str
    content_file: str
    url: str
    language: str
    last_mod: datetime.datetime
    phone = "+420 753 258 951"  # TODO: Change
    email = "info@signiffer.eu"  # TODO: Change

    def keys(self):
        """Get keys that allows conversion of this class to dictionary.

        Returns:
            List[str]: List of the keys to be passed to template.
        """
        return ['title', 'keywords', 'description', 'url', 'content_file',
                'language', 'email', 'phone']

    def __getitem__(self, key):
        """Allows conversion of this class to dictionary.
        """
        return getattr(self, key)

    def generate_site(self):
        with open(PATH_TO_TEMPLATES.joinpath('page.html')) as tem_han:
            template = Environment(
                loader=FileSystemLoader(PATH_TO_TEMPLATES)
            ).from_string(tem_han.read())
            html_str = template.render(
                **dict(self),
                link_to_homepage=link_to_homepage
            )
            return html_str

    @property
    def absolute_url(self):
        if self.url != 'index':
            return URL_ROOT + self.url + html_file_suffix
        return URL_ROOT

    @property
    def last_modified(self):
        if self.last_mod is None:
            return None
        return self.last_mod.strftime('%Y-%m-%d')


pages = [
    Page(title="Signiffer z. s.",
         keywords="spolek, osvěta, publikace, přednášky",  # noqa: E501
         description="Nezisková organizace specializující se na osvětovou a publikační činnost za účelem propagace, podpora a rozvoj celoživotního učení s cílem zvyšování všestranné kvality osobnosti jednotlivce.",  # noqa: E501
         url="index",
         content_file='page_home.html',
         language="en",
         last_mod=datetime.datetime(2020, 12, 6)
         ),
    # Page(title="DComplex Czechia: About us",
    #      keywords="automation, machine vision, production",  # noqa: E501
    #      description="We can help you with the automation of processes in your factory. Increase your production and cost efficiency with a lite help from our team of experts.",  # noqa: E501
    #      url="about",
    #      content_file='page_about.html',
    #      language="en",
    #      last_mod=datetime.datetime(2020, 12, 6)
    #      ),
    # Page(title="DComplex Czechia: Services",
    #      keywords="automation, machine vision, production",  # noqa: E501
    #      description="We can help you with the automation of processes in your factory. Increase your production and cost efficiency with a lite help from our team of experts.",  # noqa: E501
    #      url="services",
    #      content_file='page_services.html',
    #      language="en",
    #      last_mod=datetime.datetime(2020, 12, 6)
    #      ),
    # Page(title="DComplex Czechia: Contact",
    #      keywords="automation, machine vision, production",  # noqa: E501
    #      description="We can help you with the automation of processes in your factory. Increase your production and cost efficiency with a lite help from our team of experts.",  # noqa: E501
    #      url="contact",
    #      content_file='page_contact.html',
    #      language="en",
    #      last_mod=datetime.datetime(2020, 12, 6)
    #      )
]

# Remove all existing resources
if PATH_TO_OUTPUT.exists():
    shutil.rmtree(PATH_TO_OUTPUT)

# Create new dir
PATH_TO_OUTPUT.mkdir()

for page in pages:
    content = page.generate_site()
    with PATH_TO_OUTPUT.joinpath(page.url + html_file_suffix).open('w') as fp:
        fp.write(content)

# Copy resources
shutil.copytree(PATH_TO_RESOURCES, PATH_TO_OUTPUT, dirs_exist_ok=True)

# Generate resource map:
with open(PATH_TO_TEMPLATES.joinpath('site_map.xml')) as tem_han:
    template = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPLATES)
    ).from_string(tem_han.read())
    html_str = template.render(
        sites=pages
    )
    with PATH_TO_OUTPUT.joinpath('sitemap.xml').open('w') as f_xml:
        f_xml.write(html_str)

robots_txt_content = f"""User-agent: *
Allow: /
Sitemap: {URL_ROOT}sitemap.xml"""
with PATH_TO_OUTPUT.joinpath('robots.txt').open('w') as robots_txt_h:
    robots_txt_h.write(robots_txt_content)