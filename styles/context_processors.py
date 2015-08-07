"Styles context_processors module"
from k2.styles import settings, get_style_list
from k2.styles.models import Style, UserStyle

def styles(request):
    if hasattr(request, 'user') and request.user.is_authenticated():
        style, created = UserStyle.objects.get_or_create(user=request.user)
        name, max_width = style.style,  style.max_width
        if style.night_style:
            # night style support
            from datetime import datetime
            now = datetime.now()
            print now.hour
            if style.night_style_from > style.night_style_to:
                to = style.night_style_to
                style.night_style_to += 24
                if now.hour < to:
                    name = style.night_style
            if style.night_style_from <= now.hour and now.hour < style.night_style_to:
                name = style.night_style
    else:
        name, max_width = settings.STYLES_DEFAULT, None
    style_list = get_style_list()
    if name in style_list:
        style_list.remove(name)
    return {"styles": {"user": Style(name), 
                        "alt": map(lambda x: Style(x), style_list), 
                        "max_width": max_width},}

