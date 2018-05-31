import string
from hypothesis import strategies as st


def builds_email(**kwargs):
    defaults = dict(
        hostname=st.text(
            alphabet=string.ascii_letters + string.digits, min_size=3, max_size=20
        ),
        domain=st.text(
            alphabet=string.ascii_letters + string.digits, min_size=3, max_size=20
        ),
    )
    defaults.update(kwargs)
    return st.builds(lambda hostname, domain: "%s@%s.cOm" % (hostname, domain), **defaults)


class Builds:
    @staticmethod
    def form_data(**kwargs):
        d = dict(
            from_email=builds_email(),
            to_email=builds_email(),
            message=st.text(alphabet=string.ascii_letters + string.digits, min_size=1),
            subject=st.text(alphabet=string.ascii_letters + string.digits, min_size=1),
            activation_value=st.text(
                alphabet=string.ascii_letters + string.digits, min_size=24
            ),
        )
        d.update(kwargs)
        return st.builds(lambda **k: k, **d)
