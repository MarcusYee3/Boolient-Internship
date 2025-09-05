def import_new_users(self, request):
    if request.method == 'POST':
        num_created_users = 0
        df = pandas.read_csv(request.FILES['new_users_file'])
        if {'last_name', 'first_name', 'email'} <= set(df.columns):
            num_requested_users = df.shape[0]
            for _, row in df.iterrows():
                if not User.objects.filter(email=row['email']).exists():
                    password_length = 13
                    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                    random.seed = (os.urandom(1024))
                    temp_password = ''.join(random.choice(chars) for i in range(password_length))
                    user: object = User.objects.create_user(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        email=row['email'],
                        username=row['email'],
                        password=temp_password)

                    subject = 'Welcome to Boolient!'
                    html_message = render_to_string(
                        'welcome_email_template.html',
                        {'client': os.environ.get('BOOLIENT_CLIENT'),
                         'first_name': row['first_name'],
                         'temp_password': temp_password,
                         'email': row['email']})
                    plain_message = strip_tags(html_message)
                    from_email = 'Boolient <auth@boolient.com>'
                    to = row['email']

                    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    num_created_users += 1
            messages.success(request, f"""
            New user creation successful: {num_created_users} out of {num_requested_users} in CSV were 
            created successfully.  An email has been sent to each new user with their temporary password.
            {num_requested_users - num_created_users} users were not created because they already exist in the system.
            """)
        else:
            messages.error(request,
                           """
                           Incorrect CSV format. Please ensure that the CSV file contains columns for 'first_name',
                           'last_name', and 'email'.
                           """)
    return views.render(request, 'import_new_users.html')
