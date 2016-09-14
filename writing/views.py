from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Story
from django.http import HttpResponse, HttpResponseRedirect
import bleach
from ebooklib import epub

allowed_tags = "a b blockquote code del dd dl dt em h1 i img kbd li ol p pre s sup sub strong strike u ul br hr div".split() + bleach.ALLOWED_TAGS
allowed_attributes = {
    'img': 'src width height alt title'.split(),
    'a': 'href title'.split(),
}


# Create your views here.
def submit(request):
    if request.method == 'POST':
        story = Story(upload=request.POST['upload'])
        story.save()
        return HttpResponse("Story id is: " + str(story.id))

    try:
        unsafe_storyhtml = Story.objects.latest('id').upload
    except:
        unsafe_storyhtml = ""
    safe_storyhtml = bleach.clean(unsafe_storyhtml, tags=allowed_tags, attributes=allowed_attributes)

    return render(request, 'writing/submit.html', {'storyhtml': safe_storyhtml})

    """
def generate_epub(request, pk):
    try:
        unsafe_storyhtml = Story.objects.filter(pk=pk) #perhaps add option so that epub can be disabled
        safe_storyhtml = bleach.clean(unsafe_storyhtml, tags=allowed_tags, attributes=allowed_attributes)

    except:
        return None # book DNE

    book = epub.EpubBook()

    # set metadata
    book.set_identifier('id123456') # get 
    book.set_title('Sample book') # get owner
    book.set_language('en')

    book.add_author('Author Authorowski')
    book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')

    # create chapter
    c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
    c1.content=

    # add chapter
    book.add_item(c1)

    # define Table Of Contents
    book.toc =  (
                epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
                (epub.Section('Simple book'),
                (c1, ))
    )

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    book.add_item(nav_css)

    # basic spine
    book.spine = ['nav', c1]

    # write to the file
    epub.write_epub('test.epub', book, {}) # need to write to file-like object

    #need to return the file-like object
"""