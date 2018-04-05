import string
from hypothesis import (
    given,
    strategies as st,
)


def create_form_data(from_email, to_email, message, subject, activation_value):
    return dict(
        from_email=from_email,
        to_email=to_email,
        message=message,
        subject=subject,
        activation_value=activation_value,
    )


def build_email(hostname, domain):
    return hostname + '@' + domain + '.cOm'


given_form_data = given(
    form_data=st.builds(
        create_form_data,
        from_email=st.builds(
                build_email,
                hostname=st.text(alphabet=string.ascii_letters + string.digits, min_size=12, max_size=12),
                domain=st.text(alphabet=string.ascii_letters + string.digits, min_size=12, max_size=12)
            ),
        to_email=st.builds(
                build_email,
                hostname=st.text(alphabet=string.ascii_letters + string.digits, min_size=12, max_size=12),
                domain=st.text(alphabet=string.ascii_letters + string.digits, min_size=12, max_size=12)
            ),
        message=st.text(alphabet=string.ascii_letters + string.digits, min_size=1),
        subject=st.text(alphabet=string.ascii_letters + string.digits, min_size=1),
        activation_value=st.text(alphabet=string.ascii_letters + string.digits, min_size=24),
    )
)