"Stories middleware module"

from k2.stories.models import UserPref

class UserPrefMiddleware(object):
    def process_request(self, request):
        pref = self.get_pref(request)
        session = request.session
        get = request.GET

        if not session.get('popular_sort') or not session.get('upcoming_sort') \
            or session.get('comment_threshold') \
            or session.get('comment_rating_style') or session.get('frame'):
            # No pref in session
            self.pref_to_session(request, pref)

        if get.get('popular_sort') or get.get('upcoming_sort'):
            # Sorting changed
            self.update_sort(request, pref)

    def get_pref(self, request):
        try:
            return request.user.get_pref()
        except:
            return None

    def pref_to_session(self, request, pref):
        session = request.session
        if pref:
            session['popular_sort'], session['upcoming_sort'], \
                session['comment_threshold'], session['comment_rating_style'], \
                session['frame'] = pref.popular_sort, pref.upcoming_sort, \
                pref.comment_threshold, pref.comment_rating_style, pref.frame
        else:
            meta = UserPref._meta
            session['popular_sort'], session['upcoming_sort'], \
                session['comment_threshold'], session['comment_rating_style'], \
                session['frame'] = \
                meta.get_field_by_name('popular_sort')[0].default, \
                meta.get_field_by_name('upcoming_sort')[0].default, \
                meta.get_field_by_name('comment_threshold')[0].default, \
                meta.get_field_by_name('comment_rating_style')[0].default, \
                meta.get_field_by_name('frame')[0].default

    def update_sort(self, request, pref):
        get = request.GET
        session = request.session
        if get.get('popular_sort'):
            session['popular_sort'] = int(get.get('popular_sort'))
        if get.get('upcoming_sort'):
            session['upcoming_sort'] = int(get.get('upcoming_sort'))
        if pref:
            pref.popular_sort, pref.upcoming_sort = \
                session.get('popular_sort'), session.get('upcoming_sort')
            pref.save()
