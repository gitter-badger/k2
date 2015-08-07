from django.forms import widgets

class StyleSelect(widgets.SelectMultiple):
    pass
#    def render(self, *args, **kwargs):
#        print "test"
#        return ""
        #rendered_string = super(StyleSelect, self).render(*args, **kwargs)
        # js only works when an id is set
#        rendered_string = ""
#        if kwargs.has_key('attrs') and kwargs['attrs'].has_key("id"):
#            rendered_string = """<script>
#if (!("autofocus" in document.createElement("input"))) {
#  document.getElementById("%s").focus();
#}
#</script>""" % kwargs['attrs']['id']
#        return rendered_string