#!/usr/bin/python
# -*- coding: utf-8 -*-
u"""
===============================================================================
showcode.py - on a URL query from a client, display any text file in an HTML
page, auto-scrolled both horizontally and vertically, with raw-text view and
download links, and a floating jump-to-Top button if JavaScript is enabled.

Author/Copyright: 2018-2022, M. Lutz (learning-python.com).
License: provided freely, but with no warranties of any kind.

Version: Feb 07, 2022 - don't display files outside the website's folder
         Jun 12, 2021 - in template, add floating Top if JavaScript enabled
         Sep 26, 2020 - format non-ASCII filenames in HTTP reply headers
         Aug 27, 2020 - encode filenames to UTF-8 for non-ASCII in 3.X+Linux
         Apr 05, 2020 - use and doc '[NC]' case-insensitive rewrite rule
         Mar 16, 2020 - flush stdout in 3.X else print() headers are last
         Jun 28, 2019 - edit load-error message to allow for permissions 
         Sep 01, 2018 - note about mixed Unicode files, latin1=>cp1252
         Jun 26, 2018 - allow non-ASCII filenames in Py 2.X, use "UTF-8"
         Jun 18, 2018 - note on avoiding explicit URLs for offline use
         Apr 23, 2018 - robots.txt handling notes
         Apr 15, 2018 - readme.txt note, special-case bad filenames
         Feb 23, 2018 - initial release, for mobile site redesign

This is a Python CGI script: it runs on a web server, reads URL "?"
query parameters, and prints HTTP headers and either HTML or plain text to
the client.  It runs on both Python 2.X and 3.X (2.X on its former host,
and 3.X on its current host as of 2020).

This is also an example and demo (and heavily documented for this role),
not a shrink-wrapped product.  To use it for your site, you must adapt 
some of its code - namely, the use of FOOTER here, and site-specific 
components in the companion showcode-template.txt.


-------------------------------------------------------------------------------
WHAT THIS SCRIPT DOES
-------------------------------------------------------------------------------

When invoked by explicit URL or Apache rewrite, this script dynamically 
builds a reply page containing the subject file's text - as either plain 
text, or formatted HTML with uniform styling and bi-directional scrolling.
Originally written for program code, this works for any type of text file.

While broadly useful, this is done primarily for ease of viewing on small
screens (e.g., mobile devices).  Else, text may be too small to read, 
without tedious zooms and scrolls.  Worse, it may be line-wrapped, which 
is awful for intentionally formatted text like program code.

For HTML replies, links to view and save the file's raw (plain) text are
also generated as options for browsers that handle them well (e.g., opening
text in a local editor).  As installed, this script is automatically run 
for _every_ ".py" and ".txt" file on this site accessed directly, per the 
invocation schemes up next.

As a security measure, this script also rejects requests for files outside
the embedding website's folder, to avoid exposing accessible system files 
by explicit URLs; see the [Feb-2022] note ahead for details.


-------------------------------------------------------------------------------
HOW THIS SCRIPT IS INVOKED
-------------------------------------------------------------------------------

This script is run by both explicit HTML links, and automatic Apache
rewrite rules.  In general, it is invoked with a URL of this form, 
where the subject file's name appears as a query-string parameter:

  https://learning-python.com/cgi/showcode.py?name=filename.py

The site name can be relative in links as usual, and the subject file 
is assumed to live in ".." (the site root, above the cgi/ folder of 
this script), so links in HTML files are coded this way when explicit:

  <A HREF="cgi/showcode.py?name=filename.py">filename.py</A>

The current site uses a few of the explicit links above, but mainly uses
Apache URL rewrite rules in .htaccess files to automatically route all
other requests for both "*.py" and "*.txt" files to this script.  These 
rules use PCRE matching patterns to map basic URLs to the form above 
automatically, thereby avoiding many manual link edits. 

For example, the following rewrite rule maps all URLs not starting in 
'cgi/' but ending in '.py', '.txt', or others to this script, thus 
handling all direct Python and text file links, while skipping script 
invocations (other extensions, including '.css', require explicit URLs,
and the "[NC]" makes this case insensitive: *.txt and *.TXT both match):

  rewriterule ^(?!cgi\/)(.*)\.(py|txt|pyw|sh|c|h)$ 
    "https\:\/\/learning-python\.com\/cgi\/showcode\.py\?name\=$1.$2" [NC]

This works, but makes raw-text displays complex.  Because the Apache 
rule maps *all* Python and text file links to the script's URL (and 
it's weirdly difficult to prevent a rewrite of a rewrite in Apache), 
this script also supports a "rawmode" parameter, primarily for use 
in the template file's precoded URLs meant to fetch a raw-text copy:

  <A HREF="cgi/showcode.py?name=filename.py&rawmode=view">filename.py</A>

  <A HREF="cgi/showcode.py?name=filename.py&rawmode=save">filename.py</A>

A "rawmode=view" triggers inline plain-text output in this script 
instead of HTML; its effect is the same as a direct file link sans
rewrites.  A "rawmode=save" sends plain text as attachment, which asks 
browsers to save immediately; where supported, this is arguably easier
and more reliable than cmd/ctrl-A+C to select text, or link rightclicks.


-------------------------------------------------------------------------------
MORE ON TARGET-FILE URLS
-------------------------------------------------------------------------------

The only files that _require_ an explicit cgi/showcode.py URL for display
are those in this script's folder (cgi/), or otherwise not matched by the
Apache rewrite rule.  In the companion HTML template file, for example, 
the self-display links must be explicit URLs, because files in this 
script's own folder are excluded by the rewrite rule in general.  Coding 
script-file names in showcode URL query parameters also avoids invocation.  

Similarly, CSS files are deliberately not matched by the rewrite rule 
to avoid mutating their code when requested by the browser, and hence 
require explicit showcode URLs for formatted display.  Viewing the raw 
text of HTML files also requires explicit showcode URLs to avoid browser 
rendering.  Most other text files can be displayed by either an explicit 
showcode URL _or_ a simple filename to trigger the Apache rewrite rule.

Although explicit cgi/showcode.py URLs always work when a server is 
present, this site is careful to use them _only_ when required, per 
the rules above.  This better supports offline viewing in the absence 
of Apache URL rewrites (else explicit URLs display script, not target).

Though convenient, Apache rewrite rules also may complicate the handling
of auto-index README files and crawler-directive "robots.txt" files, 
but these are both subtle enough to warrant their own sections.


-------------------------------------------------------------------------------
HANDLING APACHE AUTO-INDEX READMES
-------------------------------------------------------------------------------

Besides making raw-text support complex, the Apache rewrite rule also 
breaks "README.txt" files in auto-generated index pages; their text no
longer appears on the index page, and their names are not shown in 
index lists (the leading theory is that their names are rewritten,
and mod_autoindex doesn't like the HTML reply it gets back).

This can be addressed by coding manual "index.html" pages.  But it's 
simpler to rename or copy to "README.html" with a <PRE> or <P> around
the file's text and a "ReadmeName README.html" in the .htaccess file. 
For less-important cases, rename to "_README.txt" and let the user 
click if they really wish to view; a script can easily automate this:
see learning-python.com/fix-readmes.py for an example.

UPDATE, Apr-2018: server breakage #1

  Oddly, this story differs at a new server to which this site was 
  recently moved.  On the new server (only), auto-index pages list 
  README.txt files, but do not display their content inline, even if 
  named in ReadmeName directives.  Hence, fix-readmes.py is not required,
  and if used must be accommodated by IndexIgnore to hide any _README*s.
  Alas, Apache's wildly implicit design yields radically variable servers!

  In retrospect, README files might also have been excluded from showcode
  by enhanced rewrite-rule patterns (similar to the robot-files handling
  of the upcoming section), but this was proved moot by the next update.

UPDATE, Jul-2018: server breakage #2

  README.txt files have once again vanished from auto-index pages on the
  server hosting this script due to an unknown GoDaddy Apache-configuration
  change, and eliminating README.txt files in the rewrite pattern had no 
  effect.  Hence, _README.txt files and their fix-readmes.py script have
  been reinstated (in .htaccess files).  Lesson: Apache servers are brittle,
  and hosting providers are worse.

UPDATE, Apr-2020: a new server home

  Due to poor response time at its former GoDaddy host, this script's site
  has finally moved to an AWS Lightsail VPS.  Among other things, the new 
  host means that root-level server configuration can subsume .htaccess files,
  and the README issues noted here are now largely legacy.  If you wish to 
  adapt this script, your hosting mileage may naturally vary.  This new 
  server also runs Python 3.X, which forced multiple patches described ahead.


-------------------------------------------------------------------------------
HANDLING CRAWLER ROBOTS.TXT FILES
-------------------------------------------------------------------------------

If your site uses a "robots.txt" file to give guidance to crawlers, you
MAY want to configure your Apache rewrite rules to avoid routing them 
to this script for formatting.  Otherwise, crawlers may invoke a URL
like this and receive an HTML page in response:

  https://learning-python.com/cgi/showcode.py?name=robots.txt

To avoid this, either expand the match pattern to disqualify this filename,
or add a rule to match the name and prune further rewrite processing if 
possible (e.g., with an L or END action code, where they apply).

For example, the following rule, which is the form that this site's main 
.htaccess file actually uses, successfully excludes robot files by using 
a lookahead negative assertion with a nested non-capturing alternation, 
plus two capturing groups (yes, yuck):

  rewriterule ^(?!(?:cgi\/|.*robots.txt))(.*)\.(py|txt|pyw|sh|c|h)$ 
    "https\:\/\/learning-python\.com\/cgi\/showcode\.py\?name\=$1.$2" [NC]

The following alternative, though, placed before the showcode rewrite rule
did not work on the site server, for reasons TBD (this is subtle business):

  rewriterule ^(.*)robots.txt$ "https\:\/\/learning-python\.com\/$1robots.txt" [L]

If your site does NOT use a robots.txt (and this script's site does not),
you probably don't need to care: the error-reply HTML page this script 
issues when a missing robots.txt is requested should be harmless to your
search visibility and crawling results.  Per:

  https://developers.google.com/search/reference/robots_txt#file-format

unrecognized content in HTML replies is simply ignored; which makes the
reply equivalent to an empty file; which is the same as no robots.txt 
at all; which means "crawl everything here."  Redirects may also be 
followed, if your showcode rewrite rule uses one (this site's doesn't).

Note that it's possible that crawlers may still recognize the directives 
text in a robots file even if it HAS been formatted as HTML for display 
by this script.  This would make the above tricks unnecessary, but was
not tested because this site doesn't use these files; your site may vary. 

Disclaimer: this is based on Google behavior which other crawlers may or
may not mimic, and your robots.txt resolution may have to be applied to
any other admin files on your site that match the showcode rewrite rule
(e.g., sitemaps?).  While this script could support a list of such files 
forcibly returned as plain-text or 404 error codes (see sitesearch.py),
it's easier to delegate to servers by coding rules to exclude such files.


-------------------------------------------------------------------------------
UNICODE POLICIES HERE
-------------------------------------------------------------------------------

When loading code from files, this script tries a set of Unicode encodings
in turn, until one works or all fail.  Most Python and text files on this 
site are UTF-8 (or its ASCII subset), but a few cp1252 and Latin-1 files 
crop up as examples.  The UNICODE_IN encodings list reflects this, but may
be changed for use elsewhere (see also the next section).  Once loaded, 
code text is just decoded code points in memory, and is always output as 
UTF-8-encoded bytes in reply pages.  Doing so portably for both Python 3.X 
and 2.X is possible but subtle; see the Jun-26-18 notes ahead.  

The next section goes into more detail on one consequence of the Unicode 
policies applied to displayed file content, and the section following it 
explores additional Unicode concerns addressed for filenames.


-------------------------------------------------------------------------------
AVOID MIXED UNICODE CONTENT ENCODINGS [Sep-2018]
-------------------------------------------------------------------------------

[There is a polished and expanded version of the following note online at
https://learning-python.com/post-release-updates.html#showcodeunicode.]

When using this script, the content of a site's displayable text files 
should generally all use a common Unicode encoding type (e.g., UTF-8) for 
reliable display.  Else, it's possible that some files may be loaded per an
incorrect encoding if their data passes under other schemes.  This is 
especially possible if files use several incompatible 8-bit encoding schemes: 
the first on the encodings list that successfully loads the data will win,
and may munge some characters in the process.

This issue cropped up in an older file created with the CP-1252 (a.k.a. 
Windows-1252) encoding on Windows, whose tools have a nasty habit of 
silently using its native encodings.  This file's slanted quotes failed
to display correctly in showcode because Python happily loads the file as 
Latin-1 (a.k.a. ISO-8859-1), despite its non-Latin-1 quotes.  The loaded 
text encodes as UTF-8 for transmission, but decodes with junk bytes.
 
Here's the story in code.  Python does not allow the character '“' to be
_encoded_ as Latin-1, in either manual method calls or implicit file-object 
writes.  This quote's 0x201c Unicode code point maps to and from byte value
0x93 in Windows' CP-1252, but is not defined in Latin-1's character set:

  >>> c = '“'               # run in Python 3.X 
  >>> hex(ord(c))           # same in 2.X (using u'“', codecs.open(), print)
  '0x201c'

  >>> c.encode('cp1252')    # valid in CP-1252, but not Latin-1
  b'\x93'
  >>> c.encode('latin1')
  UnicodeEncodeError: 'latin-1' codec can't encode character '\u201c'...

Conversely, _decoding_ this character's CP-1252 byte to Latin-1 works 
both in manual method calls and file-object reads.  This is presumably 
because byte value 0x93 maps to an obscure and unprintable "STS" C1 control 
character in some Latin-1 definitions, though the decoder may simply allow
any 8-bit value to pass.  It's not a CP-1252 quote in any event:

  >>> b = b'\x93'
  >>> b.decode('cp1252')    # the proper translation
  '“'
  >>> b.decode('latin1')    # but it's not a quote in latin1
  '\x93'

  >>> n = open('temp', 'wb').write(b)
  >>> open('temp', encoding='cp1252').read()
  '“'
  >>> open('temp', encoding='latin1').read()    # <= what showcode did
  '\x93'

This is problematic in showcode, because this script relies on encoding 
failures to find one which matches the data and translates its content 
to code points correctly.  Because a CP-1252 file loads without error as 
Latin-1, its UTF-8 encoding for reply transmission is erroneous; the 
quote's code point never makes the cut:

  >>> b.decode('cp1252').encode('utf8').decode('utf8')   # load, reply, browser
  '“'
  >>> b.decode('latin1').encode('utf8').decode('utf8')   # the Latin-1 munge...
  '\x93'

The net effect turns the quote into a garbage byte that browsers simply 
ignore (it's a box in Firefox's view-source, but is otherwise hidden). 

If your non-UTF-8 files are _only_ CP-1252, replacing Latin-1 with CP-1252
in the encodings list fixes the issue.  However, if your site's files use
multiple encodings whose byte ranges overlap but map to different characters,
using CP-1252 may fix some files but break others.  Latin-1 files using the 
0x93 control code, for example, would sprout quotes when displayed (unlikely,
but true).  The real issue here is that content of mixed encodings is 
inherently ambiguous in the Unicode model.

The _better solution_ is to make sure your site's displayable text files 
don't use incompatible encoding schemes.  At showcode's site, the simplest 
fix was to adopt UTF-8 as the site-wide encoding, by opening its handful 
of CP-1252 files as CP-1252, and saving as UTF-8.  The set of suspect files
can be easily isolated by trying UTF-8 opens (e.g., in an os.walk() loop).

Converting to UTF-8 universally will not only help avoid corrupted text 
in showcode, it might also avoid issues in text editors that are given or 
guess encoding types.  If you give the wrong encoding to an editor, saves 
may corrupt your data.  If you expect a tool to deal with mixed encoding 
types, guessing may be its only recourse.  But guessing is overkill; is 
impossible to do accurately anyhow; and is not science.  Skip the drama 
and convert your files.

UPDATE: preset to 'cp1252'

  In light of all the above, 'latin1' was eventually replaced by 'cp1252' 
  in showcode's preset input-encodings list, to accommodate a few files at 
  this site that are intentionally not UTF-8 (this is similar in spirit to 
  the policies for parsing web pages in HTML5).  CP-1252 is a superset of 
  Latin-1 and should work more broadly, but change as needed for your site's 
  files.  This is still only a partial solution for mixed-content ambiguity; 
  use a common Unicode type to avoid encoding mismatches altogether.

FOOTNOTE: Latin-1 pass-through

  Subtly, some scripts, including this site's genhtml web page builder (see
  learning-python.com/genhtml.html), can often get away with treating CP-1252 
  and other 8-bit encodings as Latin-1, because bytes whose interpretations 
  differ between the two are passed through unchanged from load to save. 
  What Latin-1 reads and writes as 0x93 is still '“' to CP-1252, though 
  the equivalence falls apart when comparing non-Latin-1 text:

  >>> '“'.encode('cp1252').decode('latin1').encode('latin1').decode('cp1252')
  '“'
  >>> '“'.encode('cp1252').decode('latin1') == '“'    # cp1252's meaning lost
  False

  This doesn't help in showcode, because data loaded as Latin-1 is not written
  again as Latin-1; encoding as UTF-8 in the reply makes the munging permanent.

FOOTNOTE: bytes processing

  In some use cases, it's also possible to sidestep Unicode encoding dilemmas
  altogether by processing files in bytes (not text) mode.  This works if the
  use case does not need to support text matches for arbitrary Unicode keys
  (genhtml does), and does not need to inform a browser of encodings to properly 
  display text (this script does).  Replacing an all-ASCII string of bytes in 
  mixed-encoding files, for example, can get by with bytes mode as long as all 
  the files store ASCII text as ASCII bytes (but UTF-16 won't!); see ip-anon.py.

FOOTNOTE: encoding guesses

  But if you really must guess Unicode encodings of text content in a Python
  program, you can try with the "chardet" third-party library.  Read all about 
  it at https://chardet.readthedocs.io/en/latest/usage.html, and fetch it at
  https://pypi.org/project/chardet/.  This may be useful in some contexts,
  but its results still are a guess, and come with confidence factors.  How
  in the world did the text story in computing become this convoluted?...


-------------------------------------------------------------------------------
MORE UNICODE CONSIDERATIONS HERE [Sep-2020]
-------------------------------------------------------------------------------

Beyond reply-body content (the displayed code/text), the following three items 
describe issues encountered with non-ASCII filenames in both system calls and 
stdout prints in Python 3.X.  These default to ASCII in CGI scripts only, 
and require special handling here.

NON-ASCII FILENAMES, FIX #1: os.stat

  As of August 2020, this script better supports non-ASCII Unicode characters
  in filenames on Linux, by manually encoding the file's pathname to bytes 
  per UTF-8, prior to passing it to file system calls in Python 3.X (only).
  Before this new manual encoding, a to-ASCII encoding run within os.stat() 
  (called from os.path.isfile()) triggered UnicodeEncodeError exceptions for 
  character codepoints outside the ACSII range; the net result produced 
  server-error reply pages for any non-ASCII filename requested.

  This fix presumably works because Python's default on the Linux server is 
  ASCII, and the patch prevents erroneous to-ASCII auto encoding in os.stat() 
  (but oddly, os.stat() exceptions did not occur in 3.X when running either 
  equivalent code or this same script with MOCK_SERVER=1 directly from a Linux
  shell on the same machine; see CAUSE below for a later explanation of this).

  The new manual encode is neither required  nor used in Python 2.X, because 
  paths are already encoded bytes (str), not decoded codepoints (Unicode); 
  this site's recent move from a 2.X to 3.X host probably spawned the failures.  
  Caveat: this fix should be harmless outside Linux and Python 3.5, and has 
  been verified offline on both Python 2.X and 3.X, but broader verification
  remains a to-do.  Search on "Aug-20" and "aug20" for code changes.

NON-ASCII FILENAMES, FIX #2: header print

  As of September 2020, this script now properly formats non-ASCII filenames 
  in HTTP reply headers per web standards.  Without this, the reply code's 
  print(contenthdr) would raise exceptions for non-ASCII filenames and yield 
  5xx server replies.  This happened only for "view" and "save" requests, 
  which return a filename in headers.  This also was observed only for Python 
  3.X on Linux (and again seems to reflect Linux defaults; see CAUSE below), 
  but the new formatting both avoids print() errors and invokes correct 
  handling in clients that receive the headers.  Search for "Sep-2020" here 
  for more on the changes.

NON-ASCII FILENAMES, CAUSE: CGI locales

  After further research, it's now known that the 3.X non-ASCII filename
  issues fixed in this script stem from the fact that the locale environment
  settings used at the terminal are not available in the CGI context, which
  causes encodings to default to ASCII in CGI scripts *only*.  Hence, CGI 
  code that works well in testing can fail live, and code that is never run as 
  a CGI script won't have the same problems (yes, yuck).  The manual-encoding 
  work-arounds here solve the failures tactically, though strategic approaches 
  (e.g., PYTHONIOENCODING settings in .htaccess) may help too.  For more on 
  this topic, search the web for "python cgi stdout unicode encoding" or see:
  https://stackoverflow.com/questions/9322410/set-encoding-in-python-3-cgi-scripts.


-------------------------------------------------------------------------------
DON'T DISPLAY FILES OUTSIDE THE WEBSITE FOLDER [Feb-2022]
-------------------------------------------------------------------------------

As a security measure, this script no longer shows files located outside
the website's root folder, unless configured to do so.  To enable this
check, set the variable SITE_ROOT_FOLDER ahead to the path to your site's
folder.  To disable this check, set this to a broader path (e.g., '/').

When enabled, all requested files will be checked to ensure that they are 
nested in the site folder, by running both your folder setting and the 
requested path through Python's os.path.realpath (which is like abspath, 
but evaluates any symlinks).  Any requested item whose path is not nested
in the site folder's path will be denied, with an error-message page.

This is done to deny dubious requests to view files outside the site.  A
recent analytics hit revealed that someone requested '../../../../etc/passwd'
by passing it as a parameter in an explicit URL.  The prior version of this 
script happily returned the host system's passwd file in response, though 
it was fully useless to the requester (as usual, all real passwords are in 
the shadow file, which cannot be accessed, and isn't plain text in any event).  

This passwd file worked only because it is world readable; other system files
are naturally off limits.  This script also fetches only files relative to its 
own folder, and there is no way to view folder listings with this script, so
the requester had to know the structure of a bitnami install; creepy, but true.

This new version of this script avoids such security risks for sensitive 
but accessible files, and frustrates similar prying eyes, by disallowing all
requests for anything outside the site's own folder with the setting ahead.
It relies on realpath as is, and could probably check for inodes in paths
too or instead (see stat), but this seems unwarranted here; tbd.


-------------------------------------------------------------------------------
OTHER USAGE IDEAS
-------------------------------------------------------------------------------

This script can also be invoked by URL in the "action" tag of a form 
in an HTML page; could be submitted by a script (see Python's urllib);
and might work as an Apache handler (to be explored).


-------------------------------------------------------------------------------
CAVEATS SUMMARY
-------------------------------------------------------------------------------

As is, this script reflects a number of tradeoffs:

-Its code must run on Python 2.X and 3.X, as hosting servers vary widely.
-Its footer code must avoid copies of text normally generated by genhtml.
-Its error checking is minimal, as it is used only in well-known contexts.
-Its ".." assumption for subject files' paths is not very general.
-Its Apache rewrite rule breaks "README.txt" in index pages (see above).
-Its Apache rewrite rule may complicate robots.txt handling (see above).
-Its always-UTF-8 output policy means others are converted to this on saves.
-Its Unicode encodings list may fail in mixed-type contexts (see above).
-Its manual UTF-8 encoding of filenames may have consequences (see above).

OTOH, it works as intended, and demos CGI; expand and improve as desired.
===============================================================================
"""



#################### 
# CODE STARTS HERE #
####################



# 2.X: not needed for print('onestr'), but is for trace=print
from __future__ import print_function

import cgitb; cgitb.enable()      # route python exceptions to browser/client
import cgi, os, sys, codecs

UsingPython3 = sys.version[0] == '3'
UsingPython2 = sys.version[0] == '2'

if UsingPython3:                                      # py 3.X/2.X compatible
    from html import escape as html_escape            # run on 2.X only initially
    from urllib.parse import quote_plus               # moved to 3.X server later
elif UsingPython2:
    from cgi import escape as html_escape             # for text added to HTML 
    from urllib import quote_plus                     # for text added to URL
else:
    assert False, 'The future remains to be written'



#==============================================================================
# Switches and constants
#==============================================================================


#------------------------------------------------------------------------------
# Jun-26-18 note: Browsers allow "UTF8" but "UTF-8" is technically the HTML 
# encoding name; python allows synonyms, including both "UTF-8" and "utf8".
# For background, see: https://encoding.spec.whatwg.org/#names-and-labels;
#
# Sep-01-18 note: See AVOID MIXED UNICODE ENCODINGS above - 'latin1' was 
# replaced with 'cp1252' in UNICODE_IN for the host site as a half-measure.
#
# See [Feb-2022] above: set SITE_ROOT_FOLDER to your site's root-folder path
# to prevent access to items outside the folder; set to '/' to allow them.
#------------------------------------------------------------------------------


MOCK_VALUES = False                 # 1=simulate parsed inputs
MOCK_SERVER = False                 # 1=simulate client request

UNICODE_IN  = ['UTF8', 'cp1252']    # try in turn for code file content
UNICODE_OUT = 'UTF-8'               # for text in generated reply page

TEMPLATE    = 'showcode-template.txt'    # the reply-page format
FOOTER      = '../dummy-footer.html'     # site-wide footer code

SITE_ROOT_FOLDER = '/opt/bitnami/apache2/htdocs'    # made canonical via realpath

trace = lambda *args: None  # or print, to display on stdout 



#==============================================================================
# Get input filename (and raw-text mode?) sent from the client
#==============================================================================


# Parse and/or forge request

if MOCK_VALUES:
    # simulate parsed request for testing
    class Mock: 
        def __init__(self, value):
            self.value = value
    form = dict(name=Mock('timeformat.py'))    # + rawmode=Mock('view')?
else:
    if MOCK_SERVER:
        # jun18: simulate post-server, pre-pylibs state
        os.environ['CONTENT_TYPE'] = 'Content-type: application/x-www-form-urlencoded'
        os.environ['QUERY_STRING'] = (
            'name=pyedit-products/unzipped/docetc/examples'
                 #'/aaa"bbb"ccc'
                 '/Non-BMP-Emojis/Non-BMP-Emoji-both-%f0%9f%98%8a.txt'
             #'&rawmode=view'
             )

    form = cgi.FieldStorage()         # parse form/url input data


# Extract request inputs

if 'name' not in form:
    name = 'cgi/showcode.py'          # show myself: more useful 
    """
    # error check: custom reply = hdr + blankline=\n + msg
    print('Content-type: text/plain\n')
    print('Please provide a value for "name" in the request.')
    sys.exit(1)
    """
else:
    name = form['name'].value         # real or mocked, pathname relative to '..'

if 'rawmode' not in form:
    rawmode = False
else:
    rawmode = form['rawmode'].value   # 'view' or 'save' or absent=formatted



#==============================================================================
# Load the code from a file in "..", in 1 of N Unicode encodings
#==============================================================================


#------------------------------------------------------------------------------
# "name" may be a basename or a pathname relative to ".." (site root).
# Both open()/read() flavors retain \r on Windows, decode to code points,
# and return a Unicode object: a py2 u'xx' unicode, or a py3 'xx' str.
# Tries N Unicode types for input, but always outputs as UTF-8 bytes.
# os.path.isfile() is a superset of os.path.exists(): don't need both.
# File loads may fail due to Unicode errors or permissions (e.g., 0200);
#
# Aug-20: In Python 3.5, the os.stat() call in os.path.isfile() raised a 
# UnicodeEncodeError encoding exception for filenames having non-ASCII 
# Unicode characters (e.g., both 16-bit BMP symbols, and larger emojis).  
# To fix, now manually encodes to UTF-8 bytes first, which prevents the
# auto ASCII encoding that failed.  The encode isn't required and even 
# fails in Python 2.X (this site's former server version), because path 
# is already encoded bytes (2.X str), not decoded codepoints (2.X unicode).
# See the top-of-file docstring's "UNICODE POLICIES HERE" for more details,
# especially its "NON-ASCII FILENAMES, CAUSE" for more on the exception;
# in short, CGI scripts lack locale settings, so encodings default to ASCII.
#
# Feb-22: see [Feb-2022] docs at top of file - now denies requests for
# all files outside the website folder, unless it's set to '/' or similar.  
# The new code also has to take care to avoid mixing string types in 3.X.
#------------------------------------------------------------------------------


path = '..' + os.sep + name       # _decoded_ str in 3.X, _encoded_ str in 2.X

# aug20: prevent to-ASCII auto encoding in 3.X's os.stat() on Linux
if UsingPython3:
    path = path.encode('utf8')    # convert str codepoints to preencoded bytes

# feb22: avoid mixed-type errors for ops ahead
if UsingPython3:
    SITE_ROOT_FOLDER = SITE_ROOT_FOLDER.encode('utf8')

# feb22: deny access to files outsite site folder
realsite = os.path.realpath(SITE_ROOT_FOLDER)
realpath = os.path.realpath(path)

if not realpath.startswith(realsite):
    code = (u'Error: requested file is outside the website folder.\n\n'
             'Please request only files that are part of this site.\n')     # feb22

elif not os.path.isfile(path):
    code = (u'Error: file does not exist or is not a file.\n\n'
             'Please verify the filename in your request.\n')     # apr18

else:
    for tryenc in UNICODE_IN:
        try:
            if UsingPython3:
                code = open(path, mode='r', encoding=tryenc, newline='').read()
            else:
                code = codecs.open(path, mode='r', encoding=tryenc).read()
        except:
            pass     # try next encoding on list
        else:
            break    # load successful: skip else
    else:
        # none worked
        code = (u'Error: could not open file.\n\n'
                 "Please adjust the script's UNICODE_IN list "    # jun18
                 "or the file's permissions.\n")                  # jun19



#==============================================================================
# Load and expand the HTML template
#==============================================================================


#------------------------------------------------------------------------------
# It's okay to load the template as str, even though "code" is unicode:
# in py3 they're the same - both are str, which is always Unicode text;
# in py2 they differ, but str is coerced up - '%s' % u'spam' => u'spam',
# even for dicts: see learning-python.com/showcode-unicode-demo.txt.
#
# Jun-26-18 - BUT we must decode strs to Unicode for py2 if they may be
# non-ASCII, because py2 expects strs to be all-ASCII whenever mixed with 
# unicodes.  This applies only to "namehtml", a str in 2.X encoded as UTF-8
# per web conventions: "code" is already unicode, "nameurl" URL-escapes any
# non-ASCIIs, and "footer" and "template" are assumed to be ASCII files. 
# Even if name is decoded, error-message "code" must be all-ASCII str or 
# unicode too - use u'xxx' above in both 2.X and 3.X (3.X requires 3.3+).
#------------------------------------------------------------------------------


if rawmode:
    reply = code    # send text as is (after encoding to bytes)

else:
    template = open(TEMPLATE).read()        # template file in '.', ASCII only

    codehtml = html_escape(code)            # HTML-escape any characters special in HTML
    namehtml = html_escape(name)            # template also hardcodes some URL escapes
   
    # no longer need to strip 'cgi/' here: used in URL query, not raw link
    nameurl = quote_plus(name)              # URL-escape this: added to query in template 

    # site-specific footer handling
    footer = open(FOOTER).read()            # load dummy ASCII generated footer html in ..
    for link in ('HREF', 'href', 'SRC'):    # munge it to add ".." to all nested item refs
        old = '%s="'    % link              # this avoids copying code (see template text)
        new = '%s="../' % link
        footer = footer.replace(old, new)

    for undo in ('mailto', '#'):            # undo up-rerouting for two special-cases 
        new = 'HREF="../%s' % undo          # still beats maintaining copied code...
        old = 'HREF="%s'    % undo
        footer = footer.replace(new, old)

    trace('namehtml:', type(namehtml), repr(namehtml))
    trace('codehtml:', type(codehtml))

    # jun-26-18: allow non-ASCII filenames in Python 2.X (see above)
    if UsingPython2:
        namehtml = namehtml.decode(UNICODE_OUT)

    trace('namehtml2:', type(namehtml), repr(namehtml))

    reply = template % dict(                # unicode reply: replace template targets
                __NAME__     = namehtml,    # the sent and escaped filename
                __NAMEURL__  = nameurl,     # the filename for raw-text link
                __CODE__     = codehtml,    # the loaded and escaped Unicode text 
                __FOOTER__   = footer)      # the munged dummy generated toolbar html

trace('reply:', type(reply), repr(reply[:40]))



#==============================================================================
# Print the reply stream back to the client
#==============================================================================


#------------------------------------------------------------------------------
# Write UTF8-encoded bytes, use "charset" to force Unicode type to match.
# "inline" is always view, but may require cmd/ctl-A+C to save contents.
# "attachment" is usually save, but opens may fail on some platforms, and
# this is just view on others (notably, iOS: there's no user file access).
#
# Mar-2020: Usage on an AWS Lightsail VPS uncovered a bug under Python 3.X: 
# stdout has to be flushed after print()s here, else headers are output 
# last - after replybytes.  This is due to buffering, and can be recreated
# by "python3 showcode.py | more" to simulate Apache's flavor.  It was found
# on an Ubuntu Bitnami LAMP stack running Python 3.5.2; it went unseen on a 
# former host using Python 2.X, as well as on Mac OS with PYTHONUNBUFFERED=1.
#
# Sep-2020: Non-ASCII filenames in HTTP reply parameters created for Raw text 
# "view" and "save" requests made print() raise exceptions in Python 3.X on 
# Linux (and yield 5xx server replies).  To fix, instead of using a simple 
# format [filename="%s"], encode non-ASCII filenames per web standards here: 
#     https://tools.ietf.org/html/rfc5987 (original)
#     https://tools.ietf.org/html/rfc8187 (updated)
#     https://tools.ietf.org/html/rfc2616#section-2.2
# This both ensures that filename parameter values are ASCII so that print() 
# works in 3.X/Linux, and invokes proper handling in recipient clients.  
# See "NON-ASCII FILENAMES, CAUSE" above for more on why this is required;
# in short, CGI scripts lack locale settings, so stdout defaults to ASCII.
#------------------------------------------------------------------------------


# Sep-2020
if hasattr(str, 'isascii'):
    isascii = str.isascii               # py 3.7+ only: use builtin method
else:
    def isascii(text):
        try:    text.encode('ascii')    # all others: use custom function
        except: return False
        else:   return True


def httpHeaderFormat(text):             
    """
    ------------------------------------------------------------------------------
    Sep-2020: Format non-ASCII parameters in HTTP replies to ASCII per standard.
    Note that for non-ASCII this formats encoded bytes, not decoded codepoints.
    ASCII is formatted to "..." as before, but any embedded " are now \" escaped.
    Non-ASCII example: ... filename*=UTF-8''%c2%a3%20spam%20%e2%82%ac%20eggs ... 
    ASCII example:     ... filename="spam\"and\"eggs" ...
    ------------------------------------------------------------------------------
    """
    trace('text:', type(text), repr(text))    # 3.X: decoded str, 2.X: encoded str

    if isascii(text):
        return '="%s"' % text.replace('"', '\\"')
    else:
        if UsingPython2:
            text_encoded = text                     # it's already encoded bytes 
        else:
            text_encoded = text.encode('utf8')      # Unicode codepoints => bytes

        text_escaped = quote_plus(text_encoded)     # percent escapes
        return "*=UTF-8" + "''" + text_escaped      # HTTP extended notation (no lang)
 

if not rawmode:
    contenthdr  = 'Content-type: text/html; charset=%s' % UNICODE_OUT
else:
    dispostype  = 'inline' if rawmode == 'view' else 'attachment'
    basename    = os.path.basename(name)
    baseparam   = httpHeaderFormat(basename)   # sep20

    contenthdr  = 'Content-type: text/plain; charset=%s\n' % UNICODE_OUT
    contenthdr += 'Content-Disposition: %s; filename%s' % (dispostype, baseparam)

replybytes = reply.encode(UNICODE_OUT)      # send encoded bytes: print is iffy

print(contenthdr)                           # reply = hdrs + blankline + html
print('')                                   # need '' for 2.X if no __future__
if UsingPython2:
    sys.stdout.write(replybytes)            # py2 accepts a str for the bytes
else:
    sys.stdout.flush()                      # mar20: else headers last on 3.X!
    sys.stdout.buffer.write(replybytes)     # py3 stdout is str: use io layer  


# And now it's up to the client
