import sys
from faker import DEFAULT_LOCALE, DEFAULT_PROVIDERS, AVAILABLE_LOCALES
from faker import Generator
from faker import providers as providers_mod


class Factory(object):

    @classmethod
    def create(cls, locale=None, providers=None):

        # fix locale to package name
        locale = locale.replace('-', '_') if locale else DEFAULT_LOCALE
        if '_' in locale:
            locale = locale[:2] + locale[2:].upper()
        if locale not in AVAILABLE_LOCALES:
            raise AttributeError('Invalid configuration for faker locale "%s"' % locale)

        providers = providers or DEFAULT_PROVIDERS

        generator = Generator()
        for provider in providers:

            provider_class = cls._get_provider_class(provider, locale)
            if not hasattr(provider_class, '__provider__'):
                provider_class.__provider__ = provider
            generator.add_provider(provider_class(generator))

        return generator

    @classmethod
    def _get_provider_class(cls, provider, locale=''):

        provider_class = cls._find_provider_class(provider, locale)

        if provider_class:
            return provider_class

        if locale and locale != DEFAULT_LOCALE:
            # fallback to default locale
            provider_class = cls._find_provider_class(provider, DEFAULT_LOCALE)
            if provider_class:
                return provider_class

        # fallback to no locale
        provider_class = cls._find_provider_class(provider)
        if provider_class:
            return provider_class

        raise ValueError('Unable to find provider "%s" with locale "%s"' % (provider, locale))

    @classmethod
    def _find_provider_class(cls, provider, locale=''):

        path = "{providers}{lang}.{provider}".format(
            providers=providers_mod.__package__,
            lang='.' + locale if locale else '',
            provider=provider
        )

        try:
            __import__(path)
        except ImportError:
            return None

        return sys.modules[path].Provider