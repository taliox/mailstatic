# mailstatic
A small python based server which allows you to send mails from a static webpage via a simple HTML form.

Amongst others, mailstatic is based on technologies like `flask`, `sqlalchemy` and `gunicorn`. 

# How does it work?
## Workflow

Simple and straight forward:

1. The POST request of your form is forwarded to your mailstatic server. 
2. The server accepts the post request and it's parameters and sends a mail with the given information towards the provided adress.
3. The provided email address receives the mail that was created by the HTML form.

## Usecases & Advantages

mailstatic really comes in handy if you want to provide a static HTML page with no actual backend.
By using mailstatic, there is no need for additional technologies like Javascript or PHP which enables your project to have a much smaller code base and to be much thinner in total. If you want to build a lightweight page, mailstatic is an easy-to-use tool to process user inputs by simply adding HTML forms.

Additionally to a much thinner project, mailstatic brings a seperate system taking care of all the user input processing which can be scaled to any need. The server saves all of the received input in a PostgreSQL DB which allows you to track, retrace and process the received input.

Due to security mechanisms like [Googles Recaptcha v2](https://developers.google.com/recaptcha/docs/display) an abuse of the service is prevented.

Also there is a configurable ratelimit set for every endpoint which is capable of sending emails to prevent abuse. 

# Setup

## Server Setup

There are two ways to run the server. But in any case you should make sure the server is configured correctly.

The `web-example.env` provides neccessary environment variables that the server uses to process certain actions:

```env
RECAPTCHA_SITEKEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_SECRET=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
IMAP_SERVER=mail.test.server
IMAP_USER=system@mailstatic.net
IMAP_PASSWORD=XXXXXXXXXXXXX
SERVER_ADDRESS=https://mailstatic.net
DATABASE_URI=postgresql+psycopg2://postgres:postgres@db/postgres
```

You need to provide details for your IMAP Server and it's user so that the server can use a provided email account to forward the content of the POST request received from the HTML form.
Additionally you can configure your server adress, the URI of the database and your Google Recaptcha information (check out the [Googles Recaptcha Site](https://developers.google.com/recaptcha/docs/display) to receive your information).

After providing the necessary information you can start the server.

### Using python on your machine

1. Open your commandline and navigate inside the project folder.
2. Run `pip install -r .\requirements.txt` to install neccessary dependencies (in case it's not working try `python -m pip install -r .\requirements.txtpip install -r .\requirements.txt`).
3. Run `python .\runserver.py` to boot the server.
4. You should see the following message `Running on http://[::]:5000/ (Press CTRL+C to quit)`.
5. If you want to start the production server, start it with gunicorn:  `pipenv run pipenv run gunicorn mailstatic:app --bind 0.0.0.0:5000`. It may be a good idea [to use a reverse-proxy](http://docs.gunicorn.org/en/stable/deploy.html) like nginx in front of it to terminate SSL and buffer slow requests. Checkout the project for configuration examples.

### Using docker

1. Open your commandline and navigate inside the project folder.
2. Check if the provided `docker-compose.yml` file serves your needs. (E.g. the run command)
3. Use `docker-compose up` or `docker-compose -f docker-compose.prod.yml up` to start the container.
4. You should see the following message: `Running on http://[::]:5000/ (Press CTRL+C to quit)`

Alternatively you can also pull our image directly from the docker hub using `docker pull taliox/mailstatic`.

## HTML setup

To setup a HTML form on your webpage simply copy the following code:

```html
<form action="yourdomain/s/your@mail.com" method="POST">
    <input name="name" required="" type="text">
    <input name="replyto" required="" type="email">
    <textarea name="message"></textarea>
    <input value="Send" type="submit">
</form>
```

All input of this form is now forwarded to your server.

# Contributing
Pull requests for improvements of the project or it's documentation are also highly appreciated.

# Licenses
This library and its content is released under the [MIT License](https://choosealicense.com/licenses/mit/).
