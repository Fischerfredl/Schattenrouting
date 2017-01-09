from jinja2 import Markup

class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def script_set_date_value(self):
        return Markup('<script type="text/javascript">\ndocument.getElementById("input_date").value = moment(\"%s\").%s;</script>' % (self.timestamp.strftime('%Y-%m-%dT%H:%M:%S Z'), 'format(\'YYYY-MM-DD\')'))

    def script_set_time_value(self):
        return Markup('<script type="text/javascript">\ndocument.getElementById("input_time").value = moment(\"%s\").%s;</script>' % (self.timestamp.strftime('%Y-%m-%dT%H:%M:%S Z'), 'format(\'hh:mm\')'))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")