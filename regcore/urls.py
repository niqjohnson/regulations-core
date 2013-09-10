from collections import defaultdict

from django.conf import settings
from django.conf.urls import patterns

from regcore_read.views import diff as rdiff, layer as rlayer
from regcore_read.views import notice as rnotice, regulation as rregulation
from regcore_read.views import search
from regcore_write.views import diff as wdiff, layer as wlayer
from regcore_write.views import notice as wnotice, regulation as wregulation
from regcore.urls_utils import by_verb_url


# Migration strategy for settings files
if not hasattr(settings, 'WRITE_VERB'):
    settings.WRITE_VERB = 'PUT'


mapping = defaultdict(dict)


if 'regcore_read' in settings.INSTALLED_APPS:
    mapping['diff']['GET'] = rdiff.get
    mapping['layer']['GET'] = rlayer.get
    mapping['notice']['GET'] = rnotice.get
    mapping['notices']['GET'] = rnotice.listing
    mapping['regulation']['GET'] = rregulation.get
    mapping['reg-versions']['GET'] = rregulation.listing
    mapping['search']['GET'] = search.search


if 'regcore_write' in settings.INSTALLED_APPS:
    mapping['diff'][settings.WRITE_VERB] = wdiff.add
    mapping['layer'][settings.WRITE_VERB] = wlayer.add
    mapping['notice'][settings.WRITE_VERB] = wnotice.add
    mapping['regulation'][settings.WRITE_VERB] = wregulation.add


# Re-usable URL patterns.
def seg(label):
    return r'(?P<%s>[-\d\w]+)' % label


urlpatterns = patterns(
    '',
    by_verb_url(r'^diff/%s/%s/%s$' % (seg('label_id'), seg('old_version'),
                                      seg('new_version')),
                'diff', mapping['diff']),
    by_verb_url(r'^layer/%s/%s/%s$' % (seg('name'), seg('label_id'),
                                       seg('version')),
                'layer', mapping['layer']),
    by_verb_url(r'^notice/%s$' % seg('docnum'),
                'notice', mapping['notice']),
    by_verb_url(r'^regulation/%s/%s$' % (seg('label_id'), seg('version')),
                'regulation', mapping['regulation']),
    by_verb_url(r'^notice$', 'notices', mapping['notices']),
    by_verb_url(r'^regulation/%s$' % seg('label_id'),
                'reg-versions', mapping['reg-versions']),
    by_verb_url(r'^search$', 'search', mapping['search'])
)
