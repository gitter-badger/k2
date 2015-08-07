def InstallOEmbed():
    from oembed.models import StoredOEmbed
    from oembed.sites import ProviderSite
    from models import thumbnail_url, db_type, match
    from sites import embed

    # Replaces match field
    StoredOEmbed._meta.local_fields[1] = match
    StoredOEmbed._meta.local_fields[1].set_attributes_from_name('match')
    StoredOEmbed._meta.local_fields[1].model = StoredOEmbed
    # Adds thumbnail field
    StoredOEmbed.add_to_class('thumbnail_url', thumbnail_url)
    # Adds thumbnail embed
    ProviderSite.embed = embed

