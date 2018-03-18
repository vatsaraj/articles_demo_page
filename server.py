from flask import Flask, request, render_template, flash, url_for, redirect, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import hashlib
import random

app = Flask(__name__)

# Sample list of registered user.
people = ['gabbar', 'kalia', 'sambha', 'basanti', 'jai', 'veeru', 'jailor', 'thakur', 'ramlal']

# Taglinies to be shown at the main page.
taglines = ('Never let your friends get lonely. Keep disturbing them.',
            'If only closed minds came with closed moouths.',
            'Keep rolling your eyes. Maybe you\'ll find a brain back there.',
            'I\'m so athletic. I surf the internet...',
            'I see no reason to act my age.',
            'I\'m not always sarcastic. Sometimes I\'m sleeping.',
            'Mirrors can\'t talk. Lucky for you they can\'t laugh either.',
            'You\'d be in good shape if you ran as much as your mouth.',
            'I\'ll try being nice if you try being smarter.',
            'I clapped because it finished, not because I liked it.',
            'I\'m not sleeping. I\'m just looking into my eyelids.')

# Samples of posts created by registered users.
posts = [ { 'id'     : 1984,
            'title'  : 'It is all Latin for me',
            'author' : 'basanti',
            'body'   : """ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vestibulum aliquam mauris, ac ultrices enim sollicitudin eu. Nulla facilisi. Integer non magna a nunc faucibus finibus. Nullam tristique fringilla lorem a placerat. Nam commodo rhoncus facilisis. Sed egestas et justo non ultrices. Aliquam scelerisque lorem ligula, et efficitur diam faucibus sit amet. Proin dolor justo, accumsan ut mattis vitae, eleifend sed odio. Pellentesque vel vestibulum enim."""},
          { 'id'     : 1800,
            'title'  : 'The Mooring Story',
            'author' : 'gabbar',
            'body'   : """Out in the straits, ships sail on in grey smoke: some with decks empty, some with men checking ropes, and one with a milling crowd taking their last glimpses. Each passing bow wave, rolling over a grey sea flecked with white, sighs on pebbles ,stretched out to muddy patches of harsh grass held back by a rock wall. Overhead, a seagull screeches, falling behind me towards the wooden framed house, where a lit window beckons in the early morning gloom. Five ships have drawn by and away since I rose to sit in the cold wind and remember a child not of mine, but one I loved. As always too soon he becomes a man, losing all innocence except hope. On birthday mornings. I would wake him with a tray made of sea-shore wood piled with a plate of scrambled eggs and the tea in a cracked bull mug. On a full moon, laughing together, it would be thrown high over the beach into the sea. In the mornings, alone on the shore, I would search for another year or to learn if the sea called. When he stirred, I would straighten the eiderdown and then sit on the nearby bench, moving aside his clothes. Sitting up, he would smile and reach for the tray. He always ate quickly before slowly sipping his tea, in silence. When ready we talked according to the mood of the sea: slow some days, others with stories taller then a mast. All the time I ignored the paintings and drawings; some of sailors weeping, others of ships, some with oars, some with sails, breaking apart in wild waves, and others of women like bleached bones on the beach looking out to sea. Some were by him but most were by the others who had rested here.""" },
          { 'id'     : 1601,
            'title'  : 'Food for the belly',
            'author' : 'kalia',
            'body'   : """Lush has brought back its glittery golden bath bomb eggs for Easter 2018.""" },
          { 'id'     : 2020,
            'title'  : 'Solid Groups',
            'author' : 'gabbar',
            'body'   : """Notes in a metallic music go like this... 'Mn Fe Co Al Ni Cu Zn Ga Li Rb Sr Pd Be Sn Hg Au Ti Ag Pb Hf...'""" },
          { 'id'     : 1632,
            'title'  : 'The mystery of the mutant bird',
            'author' : 'jailor',
            'body'   : """ Birdwatchers are rushing to a town in Alabama in hopes of glimpsing a one-in-a-million look at a yellow bird, after a local resident posted images to social media of the bird feeding in her backyard, according to news reports.

So what's so special about this bird? It's a cardinal that has yellow feathers due to a rare genetic mutation that blocks its ability to assimilate red hues. The mutant bird is so rare that one ornithologist says that, if there were a million or so backyard bird feeders in the United States and Canada, just two or three would get a visit from one.

"There are probably a million bird feeding stations in that area, so very, very roughly, yellow cardinals are a one-in-a-million mutation," Geoffrey Hill, a professor and curator of birds at Auburn University in Alabama, told AL.com.""" } ]
# -------------------------------------------------------------------

@app.route('/')
@app.route('/index')
@app.route('/home')
@app.route('/root')
def welcome() :
  taggy = taglines[random.randint(0, len(taglines)-1)]

  return render_template('welcome.html', quote=taggy)
# -------------------------------------------------------------------


@app.route('/help')
@app.route('/help/')
def help_show() :
  return render_template('help.html')
# -------------------------------------------------------------------


@app.route('/about')
@app.route('/about/')
def about_show() :
  return render_template('about.html')
# -------------------------------------------------------------------

@app.route('/profile/<username>')
@app.route('/profile/<username>/')
def profile_show(username) :
  topicsid = []

  if(username in people) :
    for item in posts :
      if(item['author'] == username) :
        topicsid.append(item['id'])

    sentence = render_template('profiler.html', name=username, posts=topicsid)
  else :
    sentence = render_template('nosuch.user.html', username=username)

  return sentence
# -------------------------------------------------------------------


@app.route('/posts')
@app.route('/posts/')
def post_show_teaser() :
  return render_template('posts.teaser.html', posts=posts)
# -------------------------------------------------------------------

@app.route('/fullposts')
@app.route('/fullposts/')
def posts_show_all_posts() :
  return render_template('posts.html', posts=posts)
# -------------------------------------------------------------------

@app.route('/posts/<string:title>')
@app.route('/posts/<string:title>/')
def post_by_title_get(title) :
  sentence = 'NO'

  for post in posts :
    if(post['title'].lower() == title.lower()) :
      sentence = render_template('apost.html', post=post)
      break

  if(sentence == 'NO') :
    sentence = render_template('apost.html', post={'id': 0, 'title': 'ERROR', 'author': 'admin', 'body': 'Article "' + title + '" not found.'})

  return(sentence)
# -------------------------------------------------------------------

@app.route('/posts/<int:articleid>')
@app.route('/posts/<int:articleid>/')
def post_by_id_get(articleid) :

  try :
    post = (item for item in posts if(item['id'] == articleid)).next()

  except StopIteration :
    post = { 'id': 0, 'title': 'ERROR', 'author': 'admin', 'body': 'Article id:' + str(articleid) + ' not found.' }

  return(render_template('apost.html', post=post))
# -------------------------------------------------------------------

@app.route('/members')
@app.route('/members/')
def members_show() :

  return(render_template('members.html', posts=posts))
# -------------------------------------------------------------------

@app.route('/method', methods=['GET', 'POST'])
def method_show() :
  return(render_template('methodical.html', method=request.method))
# -------------------------------------------------------------------





# Launch this webserver only if this script is
# invoked as the main file, not imported from
# another file.
if(__name__) == '__main__':
  app.run(host='0.0.0.0', port=8080)
  # To enter debug mode, comment the line above and uncomment the one below.
  # app.run(host='0.0.0.0', port=8080, debug=True)
# -------------------------------------------------------------------
