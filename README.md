GitHub Connector

# **GitHub Connector**

GitHub Connector is a social media application that allows people with similar experience to connect with each other, people who use similar tech stacksare suggested as connections to each other. It allows users to:

  - Create a GitHub Connector User Acccount
  - Attach a valid GitHub account
  - Once a GitHub account is linked, a profile will be built and suggestions for connections will be made based on the tech stack the user is using.
    - Connections can be accepted or rejected
  - Sign in and out of the application and ability to delete your profile.
  
  ## **Software Architecture and Design**
GitHub Connector is built with a PostgreSQL(Under Consideration), Express(Under Consideration), Node.js(Under Consideration) and Bootstrap stack. Express is the structural framework and Node.js us used for the backend. 

The app will use JWT authentication. This is a token based technocloy that allows for users to only access their data and prevents users from accessing other peoples data. Each time a user tries to access another resource the JWT will be validated.

The backend works with different API calls to make requests to the Postgres database, as well as making requests out to the GitHub API. 

The backend allows for different API calls to make requests to the database as well as the GitHub API. This will be hosted on Heroku. This will be a three-tiered architecture shown below.

![Image of Structure] (361 Structure.png)






