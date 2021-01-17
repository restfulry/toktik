from django.core.cache import cache
from micawber.providers import Provider, bootstrap_basic

oembed_providers = bootstrap_basic(cache)

# add a custom provider
oembed_providers.register('https://www.tiktok.com/\S*',
                          Provider('https://www.tiktok.com/oembed?'))
