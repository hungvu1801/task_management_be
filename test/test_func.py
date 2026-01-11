from app.utils import (
    send_email,
    EmailData,
    generate_new_account_email,
    render_email_template,
)


def test_send_email():
    email_data = generate_new_account_email(
        email_to="vutienhung2212@gmail.com",
        username="testuser",
        password="testpassword",
    )
    send_email(
        email_to="vutienhung2212@gmail.com",
        subject=email_data.subject,
        html_content=email_data.html_content,
    )


def test_generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    email_data = generate_new_account_email(
        email_to=email_to,
        username=username,
        password=password,
    )

    return email_data


def test_render_email_template():
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "username": "testuser",
            "password": "testpassword",
            "email": "vutienhung2212@gmail.com",
        },
    )
    return html_content


if __name__ == "__main__":
    # print(
    #     test_generate_new_account_email(
    #         email_to="vutienhung2212@gmail.com",
    #         username="testuser",
    #         password="testpassword",
    #     )
    # )
    test_send_email()
