# Guitar Website

## Overview

This website is an attempt to collect guitar tabs and songs that I like to play in a way that they can easily be used by me and perhaps even published for others.  I like the idea of building a tool that others could use to easily publish their own guitar songbooks as well.

## History

I've collected these tabs for probably 20 years.  I've put them in text files, word docs, and at one point even published them in a Confluence wiki.  The wiki was great.  It was easy to browse and search.  However, it was deleted when my billing address changed, and I was too upset with the company to stand up another one.  I decided instead to try a static generated website that could would allow me to store the guitar music in basically a "raw" form, but add a nice layout and and publishing mechanism on top of that.  This would also let me store the guitar music in source control so I don't lose it (like I almost did in 2019).

I noticed in my files that at one point I even created XML files that looked like this:

```
<?xml version="1.0"?>
<song>
  <info>
    <title>When I'm Gone</title>
    <artist>3 Doors Down</artist>
  </info>

  <part name="intro" id="intro"/>
  
  <verse>
There's another world inside of me that you may never see 
There's secrets in this life that I can't hide 
Well somewhere in this darkness there's a light that I can't find 
Well maybe it's too far away, or maybe I'm just blind 
     Maybe I'm just blind 
  </verse>
  <part name="post verse"/>
  
  <chorus id="chorus">
So hold me when I'm here - Right me when I'm wrong 
Hold me when I'm scared - And love me when I'm gone 
Everything I am - And everything in me 
Wants to be the one - You wanted me to be 
I'll never let you down - Even if I could 
I'd give up everything - If only for your good 
So hold me when I'm here - Right me when I'm wrong 
Hold me when I'm scared - You won't always be there 
So love me when I'm gone 
     Love me when I'm gone 
  </chorus>
```

and then tried to use an XSL document to translate them into HTML.  This was pretty close to the idea of a static website.  But the static website should be better since it will allow me to write plain text files and include metadata such as:

```
---
title: Loser
artist: 3 Doors Down
---
INTRO

<VERSE>
Breathe in right away,
Nothing seems to fill this place
I need this every time,
Take your lies get off my case
Someday I will find 
A love that flows through me like this
This will fall away,
This will fall away
```

The transformation applied to these can then be pretty light.  We can just drop the page content into a ```<pre>``` tag and add some formatting and navigation.

I'm going to try Metalsmith since I'm OCD and like the complete control it gives over the translation process.  We'll see how it goes...
