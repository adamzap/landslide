#Landslide presentation <br/> with Lea Verou's CSSS model{: #theheader}

Jean-Philippe ZIMMER - IUT Dijon-Auxerre
{: .attribution #thefooter}

Interesting conference - Auxerre - 22/11/2012
{: .situation}
---

# Landslide

Landslide can generate a slideshow using slides simple to write.
The basic version uses the google slide model.

This version use the model of [Lea Verou's CSSS presentation](http://leaverou.github.com/CSSS/).

Landslide needs the **python** language with the following modules *jinja2*, *markdown* and *pygments* to work.

With **debian** and **ubuntu**, the installation is performed with `apt-get install landslide`. Nevertheless, the
version of the application contained in the landslide repositories does not contain the latest enhancements.
To have access to these improvements, you must follow the installation procedure as shown on the main page
the deposit GitHub.

## How to make your slideshow ?

- Develop your slides with simple tags in the file *slides_en.md*,
- Run the command `landslide leaverou_en.cfg`,
- See the result in the file *presentation_en.html*.

---

# Why using the Lea Verou's CSSS presentation ?

- It is based on the HTML5/CSS3 and takes into account the latest developments of these standards.
- It has a clean design, efficient and enjoyable to watch.
- It is Open Source and can be downloaded [GitHub](https://github.com/LeaVerou/csss).
- The navigation is easy :
    - arrows to move forward or backward finely,
    - SHIFT+arrows for forward or backward slide in slide,
    - Home to go to the first slide, End to go to the last,
    - SHIFT+G to jump to the slide specified slide.
- Size of the page contents is dynamic.
- The page title is the title of the slide.
- ...
 
---

# Why the CSSS presentation with Landslide

In order to make a presentation application that could replace conventional applications 
such as MS PowerPoint or Impress OO I looked for presentations that can be viewable by a browser.

I found this presentation (and also others availables) based on HTML5/CSS3.
This presentation is quite simple to use for someone who knows a little coding to HTML.
However, for a novice or a person reluctant to programming, I looked for a better 
solution to compose the presentation slides.

After various tests and research, I happily test the landslide application.
This is actually the application that I needed to complete my project.

The rest is a bit of coding and adaptation to present a simple, easy to use 
application and to think about some improvements.

---

# Some adaptations and improvements

- I made some modifications to the CSSS basic model so that it matches a
 result more visually according to my expectations.
- The table of contents within the Google model has been reported in the CSSS model.
To make it appear and disappear, use SHIFT+t.
- A class situation that marks where the presentation takes place.
- A header and footer, which include the texts of the title page.
- Coming soon: a timer to allow automatic scrolling slides.

---

# Instructions to use Markdown formatting

- The following instructions are brief. You can find [on this site](http://daringfireball.net/projects/markdown/syntax)
more detailed instructions.
- Separate your slides with a horizontal line (--- with markdown).
    - The first slide will be used as the title of the presentation.
    - Other slides can have a title (it is better to set one).
- The main titles are marked with one #, with the secondaries with ##, ... 

---

# Instructions to use Markdown formatting - 2

- A paragraph consists of one or more consecutive sentences, 
    - To separate paragraphs, you must insert a blank line between them,
    - To force a newline you must insert at least two spaces at the end of the line.
- A word surrounded by :
    - \* is displayed *bold*,
    - \*\* is displayed **italic**.
    - \` is displayed `surlined`. 
- To display marking characters ( \* , \` , \- ,... ), you must precede them by \\ (AltGr-8).

---

# Instructions to use Markdown formatting - 3

To highlight the code you need to insert 4 spaces or 1 tab at the beginning of the line.

You can also insert \!Thelanguage before the first line of code.

First coding block (\!python):

    !python
    while True:
        print "Everything's gonna be allright"

Second coding block (\!php):

    !php
    <?php exec('python render.py --help'); ?>

---

# The links with Markdown

A hyperlink is easily done by placing the link text in brackets (\[ et \]) followed 
by the URL address between brackets () . 

For example:

\[MySafeKey helps you to secure your PC\](http://www.mysafekey.org) gives : 

[MySafeKey helps you to secure your PC](http://www.mysafekey.org).

By following this principle and preceding by a \!, we can also easily insert an image :

For example :
\!\[MySafeKey \](./img/logomysafekey3.png) gives : ![MySafeKey](./img/logomysafekey3.png)

---

# The lists with Markdown

## Simples lists

Making lists is very simple: they use marks \- ,\+ ou \* .
For example :

    - Item 1
    - Item 2
        - Sub item 2.1 (4 space characters to the left of the mark)
            - Sub sub item 2.1.1 (8 space characters to the left of the mark)
    - Item 3 (back to the start of the line)


gives :

- Item 1
- Item 2
    - Sub item 2.1 (4 space characters to the left of the mark)
        - Sub sub item 2.1.1 (8 space characters to the left of the mark)
- Item 3 (back to the start of the line)

---

# The lists with Markdown - 2
## Addings a CSSS style

Items appear one after the other:

- Item
{: .delayed}
    - Sub item
{: .delayed}
         - Sub sub item
{: .delayed}
- This is accomplished by Markdown extensions.
{: .delayed}
    -by inserting {: .delayed} just under the line item.
{: .delayed}

---

# Markdown is magic !

Markdown extensions are very powerful and interesting. You can see the extensions 
list of [Markdown with Python](http://packages.python.org/Markdown/extensions/index.html).

Extensions can be used with Landslide with the option \-x.

## Extension attr_list

It allows, with its syntax, to add different attributes to HTML elements. For example :

	This is a paragraph.
	{: #one_id .one_class }
	
gives

	<p id="one_id" class="one_class">This is a paragraph.</p>
	
It is through this option that the CSSS class called "delayed" presents in the previous slide or the
class "allocation" of the title page of presentation are used.
 
Many other extensions are possible, you can refer to the page mentioned above.

