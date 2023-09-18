Innotter - Django & FastAPI based Twitter analogue 🌐
🎈 Main Purpose 🎈

Write a backend for Twitter analogue with awesome features.
🚧 Foundation 🚧

A user can have one of 3 roles:

    Administrator
    Moderator
    User

    The administrator has the right to view any pages, block them for any period of time and permanently, delete any posts and block users. The administrator also has access to the admin panel.
    The moderator has the right to view any pages, block them for any period of time, delete any posts.
    The user can:
        register, log in
        create a page, edit its title, uuid and description, add and remove tags to it, make it private/public
        subscribe to other people's pages (throw a subscription request in case of private pages)
        view the list of those wishing to subscribe to the page (in case of private) and confirm / refuse to subscribe ( one by one or all at once)
        write posts on their pages, edit them, delete
        like/unlike posts, reply to them on behalf any of his own pages
        View Liked Posts
    User and page avatars are stored in the cloud storage.

🌀 System capabilities 🌀

    Send email notifications to subscribers about new posts.
    Show news feed (all new posts of signed and own pages)
    Automatically block all user pages if the user is blocked
    Provide page search by title/uuid/tag and users by username/name (using one endpoint)
    Check extensions of uploaded files
    Show page statistics (number of posts, subscribers, likes, etc.), which is generated on the microservice, only to page owners

🖥️ Technologies 🖥️

    Databases: PostgreSQL, DynamoDB
    Authorization: PyJWT
    Scheduler: Celery, Flower
    Broker: RabbitMQ
    Backend: Django, Django Rest Framework, FastAPI, boto3, Pydantic
    Cloud: AWS(SES, S3, EC2)
    DevOps: Docker, Docker-compose

🛠 How to Use 🛠

    Clone project to your folder

      git clone https://github.com/amarjin6/innotter.git

Check for updates and install all necessary requirements

  pipenv shell
  pipenv install -r requirements.txt

Create env folder in project root & declare all env variables

  mkdir env
  cd env
  touch db.env fastapi.env localstack.env rabbitmq.env

Build docker services

   docker-compose up --build
   docker-compose run django
   docker-compose up
   docker-compose down

Open project in your browser & check its functionality

  google-chrome --no-sandbox

📌 Active endpoints 📌

Django:
admin
__debug__
api/swagger
api/v1/login
api/v1/login/refresh
api/v1/login/verify
api/v1/users
api/v1/customer/tags
api/v1/dealer/pages
api/v1/posts
api/v1/register
api/v1/dealers
api/v1/feed

FastAPI:
docs
statistics
