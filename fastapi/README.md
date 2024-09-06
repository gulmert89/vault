# Notes
## 1. Project 1 & 2: Introduction
* `pip3 install "fastapi[all]"`
* `Uvicorn` is the web server we use to start a FastAPI application.
* The decorator `@app.get('/')` is for to tell FastAPI *"Hey, this function is our API endpoint."* It's our HTTP route.
* `> uvicorn books:app --reload` (reloads whenever the file changes.)
* OAS (OpenAPI Specification): Universal standard on how to create & handle APIs.
* FastAPI generated the OpenAPI schema so you can view. Visit: `http://127.0.0.1:8000/openapi.json`
```json
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/": {
            "get": {
                "summary": "First Api",
                "operationId": "first_api__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        }
    }
}
```
* It helps the developer to create RESTul APIs based on the standard.
* Swagger-UI: Interactive API documentation. It automatically documents all of our APIs so we can easily call them. It can be found on: `http://127.0.0.1:8000/docs` It visualizes our API.
* `--reload` We don't use it on production since prod code doesn't change much.
* We use `async` in FastAPI, due to asynchronous code, concurrency, and parallelism. And it typically provides performance optimizations when handling asynchronous functions. FastAPI automatically makes the normal functions asynchronous in the background.
* Path parameters: `@app.get("/books/{book_title}")` **(This is a dynamic path parameter!)**
* Query parameters: `http://127.0.0.1:8000/?skip_book=book_5`
* Last `/` at the end (e.g. `@app.get("/read_book/")`) tells FastAPI that this is not a path parameter, but a query parameter.
* Mert: The URLs at the `assignment` APIs are the same but the HTTP request methods are different! Thus, if you request `GET` method for that query parameter, you get the book. If you send `DELETE`, it kills the book. Get it?
* Assignment Notes:
    * What is a path parameter: _Variables that are part of the API URL, i.e. they are request parameters that have been attached to the URL._
    * What is a query parameter: _Sort and filter through data that is not marked by a path parameter._
* GET request cannot have a **body** but POST and GET have. So, what is a body? -->
* What is the body in a POST request: By design, the POST request method requests that a web server accept the data enclosed in the body of the request message, most likely for storing it. It is often used when uploading a file or when submitting a completed web form. In contrast, the HTTP GET request method retrieves information from the server.
* What is the body of a URL: HTTP Message Body is the data bytes transmitted in an HTTP transaction message immediately following the headers if there are any (in the case of HTTP/0.9 no headers are transmitted).
* Mert: So, importing the `Body()`from the library will validate and say that there is going to be a data! In the Swagger-UI, now **Request body** will appear and it'll be required. 
* `Pydantic` is a data validation and settings management that you can use on Python and type annotatios. _pydantic_ <u>enforces</u> type hints at runtime, and provides user friendly errors when data is invalid.
* A `UUID (Universal Unique Identifier)` is a 128-bit value used to uniquely identify an object or entity on the internet. Depending on the specific mechanisms used, a UUID is either guaranteed to be different or is, at least, extremely likely to be different from any other UUID generated until A.D. 3400.
* During the parsing of `Book` object, due to data validation of Pydantic, example of title, `13`, turned to string because we hinted its type as `str` on the `Book` class.
* If we miss a field, say `author`, we get this error:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "description"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
* If we provide an empty string to, let's say, `title`, it adds our `Book` object to the `BOOK` list. However, we can add extra data validation layer for such empty strings by using `Field`s. We can have more control over the input (min length, max value etc.)
* Why did we give `book_request` a type hint of `BookRequest` class (which inherits `BaseModel`)? Because defining the class helps FastAPI to create a schema and an example value out of it. You can see them on the Swagger UI. This is a good example of data validation by `pydantics`.
* We converted `book_id` to optional and now we don't have to provide any data related to it, even though we kept it in our `Book` class' constructor since we use it in our object. However, we can just remove the `book_id` from our POST request. The `BookRequest` class _knows_ that it is empty and it assigns `null` to it in the background.
* If we add `min_length=1` to our Field variable, we get this `422: Unprocessable Entity` error if we leave the `title` as an empty string:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "title"
      ],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {
        "limit_value": 1
      }
    }
  ]
}
```
* We can see these parameters of the `Field` in the Schema tab under the Swagger UI.
* For example, the `description` keyword argument of `Field` helps us to provide additional information that can be read in the schema.
* To add an example value to the Schema and the request body in the POST method, we added a `Config` class inside the `Book` class. These example values are created by the class variable `schema_extra`.
* Assignment Notes:
    * What is `Pydantics`: `Pydantics` is used for data parsing and data validation.
    * What is the purpose of `class Config` within our `class Book(BaseModel)`: _To create a more descriptive request within our Swagger documentation_
* We imported and added `Path` and `Query` to our path & query parameters in our functions. Why? To add data validation for them.
* HTTP Request Methods (CRUD operations):
    * GET: Read method that retrieve data
    * POST: Create method, to submit data
    * PUT: Update the entire source
    * PATCH: Update part of the source
    * DELETE: Delete the source
* HTTP Response Status Codes:
    * 1xx: Informational Response: Request still processing
    * 2xx: Success: Request successfully complete
        * 200: OK
        * 201: Created (Used when a POST creates an entity.)
        * 204: No Content (Didn't create or return anything. Commonly used with PUT requests.)
    * 3xx: Redirection: Further action must be completed by the client (YOU!)
    * 4xx: Client Error: Client are told that s/he has fucked up things.
        * 400: Bad Request (Used for invalid request methods.)
        * 401: Unauthorized
        * 404: Not Found
        * 422: Unprocessable Entity (Semantic errors in client request)
    * 5xx: Server Errors: It's not you, client. It's me.
        * 500: Internal Server Error
* We added `HTTPException` to the functions for proper exception handling. It has been wrapped in a function for ease of use.
* Why did we use `raise HTTPException(status_code=404)` in our `read_book_from_id` function instead of providing a string "Item not found."? Because we don't want to send 200 code (Our application is successful.) to the client. We want to show them the `Not Found` code.
* What is Starlette?
    * **Starlette** is a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python. Much of FastAPI’s web code is based on the Starlette package, created by Tom Christie. It can be used as a web framework in its own right, or as a library for other frameworks, such as FastAPI. Like any other web framework, Starlette handles all the usual HTTP request parsing and response generation. It’s similar to Werkzeug, the package that underlies Flask. But its most important feature is its support of the modern Python asynchronous web standard: ASGI. Until now, most Python web frameworks (like Flask and Django) have been based on the traditional synchronous WSGI standard. Because web applications so frequently connect to much slower code (e.g., database, file, and network access), ASGI avoids the blocking and “busy waiting” of WSGI-based applications. As a result, Starlette and frameworks that use it are the fastest Python web packages, rivalling even Golang and NodeJS applications. [[Source](https://www.oreilly.com/library/view/fastapi/9781098135492/ch04.html#:~:text=Starlette%20is%20a%20lightweight%20ASGI,async%20web%20services%20in%20Python.)]
    * ASGI: The Asynchronous Server Gateway Interface (ASGI) is a calling convention for web servers to forward requests to asynchronous-capable Python programming language frameworks, and applications.
* `status.HTTP_204_NO_CONTENT` in POST or DELETE methods helps client to understand that the server doesn't return anything, no body. 200 code or an empty list may not be as helpful as these explicit status codes.
* In our `create_book` function, we return 201 (which means _something has been created_) even though the response body is `null`.

## 2. Project 3: Complete RESTful APIs
### 2.1. Setup Database
* Object Relational Mapping (ORM) is a technique used in creating a "bridge" between object-oriented programs and, in most cases, relational databases. Put another way, you can see the ORM as the layer that connects object oriented programming (OOP) to relational databases. [[Source](https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/#:~:text=Object%20Relational%20Mapping%20(ORM)%20is,(OOP)%20to%20relational%20databases.)]
* Also, see: [What is an ORM, how does it work, and how should I use one?](https://stackoverflow.com/questions/1279613/what-is-an-orm-how-does-it-work-and-how-should-i-use-one)
* `sqlalchemy.ext.declarative.declarative_base`: Construct a base class for declarative class definitions. The new base class will be given a metaclass that produces appropriate [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) objects and makes the appropriate [`mapper()`](https://docs.sqlalchemy.org/en/13/orm/mapping_api.html#sqlalchemy.orm.mapper) calls based on the information provided declaratively in the class and any subclasses of the class. [[Source](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base)]
* Simple code on how to insert data to a DB:
```sql
INSERT INTO todos (title, description, priority, complete)
VALUES ('Go to the vet.', 'At around 3pm', 5, False)
```
* Simple code on how to update data on a DB:
```sql
UPDATE todos
SET complete=True
WHERE id=5
;
```
* Simple code on how to delete data on a DB:
```sql
DELETE FROM todos WHERE id=5;
```
* `apt install sqlite3`
* `> sqlite3 todos.db`
    * `.schema`: Shows all the tables within the db.
* Different SQLite3 `.mode` for the terminal: `column`, `markdown`, `table`, `box` etc. You can see them all by typing `.help mode`. There are also options for these modes.
### 2.2. API Request Methods
* `from fastapi import FastAPI, Depends`
    * `async def read_all(db: Annotated[Session, Depends(get_db)])`
    * `Depends`: Dependency injection. Means that we need to do something before we execute what we are trying to execute. In other words, it calls a function beforehand. i.e. a way to declare things that are required for the application/function to work by injecting the dependencies.
    * `Annotated`: Add context specific metadata to a type. Example: `Annotated[int, runtime_check.Unsigned]` indicates to the hypothetical `runtime_check` module that this type is an unsigned int. ***Every other consumer of this type can ignore this metadata*** and treat this type as int. The first argument to `Annotated` must be a valid type. (From its doctype)
### 2.3. Authentication & Authorization
* The initial `auth.py` file was a different FastAPI application (bc we defined `app = FastAPI()`). Thus, we didn't see the other methods we created in `main.py` file. We need **routing** and scale our application.
* `APIRouter` will route our `main.py` **to** our `auth.py` file.
    * So we use `router = APIRouter()` instead of `app = FastAPI()`.
    * Don't forget to include our `auth.py` as a route of the FastAPI application. Thus, it is necessary to add `app.include_router(auth.router)` in the `main.py` file.
* We created a `todos.py` inside the `routers` folder and copied everything from `main.py`. Now, we don't need this part (and their imports) in the `todos.py` file:<br>
```python
app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(
    bind=engine
)  # Creates everything from database.py & models.py files.
# So we have created a DB without writing any SQL code.
```
* Also, we cleaned everything in the `main.py` file and kept the necessary imports and `include_router` methods and db creation command only. All the API endpoints are moved to `todos.py` file.
* **One to Many Relationship:** A user can have many todos, but one todo cannot have multiple users.
    * We add a ***foreign key*** to the **Todos** table, called `owner` to link todos to **Users** table.
* To hash & encrypt/decrypt the passwords, we installed `passlib` library by `pip3 install "passlib[bcrypt]"`.
* We use `python-multipart` library (seems already installed) to submit forms to our app.
* `OAuth2PasswordRequestForm` creates various Form request parameters in our endpoint, like `grant_type`, `username`, `password`, `scope` etc.
* **JSON WEB TOKEN (JWT):** A self-contained way to securely transmit data and information between two parties using a JSON Object. It's not an authentication method but used when dealing with authorization. It consists of three parts separated by dots. `aaaaaaaa.bbbbbbbbb.cccccccccc` where `a`: Header, `b`: Payload, `c`: Signature. (more info [here](https://www.geeksforgeeks.org/json-web-token-jwt/))
    * **Header:** Usually consists of two parts:
    ```json
    {
        "alg": "HS256",  // algorithm for signing
        "typ": "JWT"  // specific type of token
    }
    ```
    The header is then encoded using Base64 to create the first part of the JWT (`a`). (The payload as well is encoded later.)
    * **Payload:** Consists of data (e.g. json file with `name`, `email` etc.) which also contains claims. There are 3 types of claims:
        * Registered
        * Public
        * Private
    ```json
    {
        "name": "some_name",
        "email": "sample@email.com",
        "iss": "https://provider.domain.com/",  // issuer
        "sub": "auth/some-hash-here",  // subject
        "exp": 153452683  // expiration date
    }
    ```
    * **Signature:** Created by using the algorithm in the header to hash out the encoded header, encoded payload with a secret. The secret can be anything, saved somewhere on the server that the client doesn't have access to.
    ```
    HMACSHA256(
        base64UrlEncode(header) + "." +
        base64UrlEncode(payload),
        some_secret
    )
    ```
* `pip3 install python-jose[cryptography]`: The JavaScript Object Signing and Encryption (JOSE) technologies. We installed it because now we can return a professional JWT to the client. It can be used to encrypt and/or sign content using a variety of algorithms. 
    * Example usage:
    ```python
    from jose import jwt

    encode = {...}  # a json with data
    some_variable = jwt.encode(
        claims=encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    ```
* To see some encoded and decoded examples of a JWT, visit https://jwt.io/. You can copy and paste your own JWT to decode it to see your data.
* About the line `payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)` under the `get_current_user` function: Someone can create a fake token but also must know the secret key and the algorithm because the function will check the authenticity of the token by using these.
* Why did we even use `OAuth2PasswordBearer` to define a `oauth2_bearer`? FastAPI checks the endpoint before validating the user request. Also, see [this](https://stackoverflow.com/questions/67307159/what-is-the-actual-use-of-oauth2passwordbearer).
### 2.4. Authenticate Requests
* I understand a bit better why we created `oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")` and put a dependency of it on the `get_current_user` function. It provides FastAPI more control over authentication under the hood. When we remove the dependency to that OAuth2 bearer, the _lock_ icon on the Swagger-UI disappears and we lose the authentication. The dependency makes the communication between functions and endpoints easier.
### 2.5. Large Production Database Setup
* Production DMBS (e.g. `PostgreSQL`, `MySQL`) vs. `SQLite`
    * SQLite3 strives to provide local data storage for individual apps and devices. It emphasizes economy, efficiency & simplicity (hence, focuses on different concepts). Works perfectly for small/medium applications. Runs in-memory or local disk and deploys easily with your application.
    * Production DBMS run on their own server & port. You need authentication linkling to the DBMS. It needs to be deployed separately from the application.
* PostgreSQL
    * Open-source RDBMS
    * Secure
    * Requires a server
    * Scalable
* For PostgreSQL or MySQL install the libraries `psycopg2-binary` or `pymysql` respectively.
## 3. Project 3.5: Alembic Data Migration
* Lightweight db migration tool for when using SQLAlchemy. These tools allow us to plan, transfer and upgrade resources with databases. Alembic allows us to change a SQLAlchemy db table after it has been created.
* Alembic keeps track of the changes we made on the db (like adding or deleting columns). Or it helps you to downgrade your db to its original form safely. It allows us to modify our db schemas.
* `pip3 install alembic`
* Git Commands:
    * `alembic init <folder name>` : Initializes a new, generic environment
        * `alembic.ini` file and an _alembic directory_ will appear.
            * `ìni` file has configuration for alembic. It's the file that alembic looks for when invoked. Holds the properties (password, username etc.) specific to the project.
            * In the directory, all environmental properties for alembic, all revisions of our app, migrations for upgrading/downgrading are located.
    * `alembic revisiom -m <message>` : Creates a new revision of the env
        * Example: `alembic revision -m "Create phone number for user column"`
    * `alembic upgrade <revision #>` (Revision number is stored in an alembic file.)
        * We fill the `downgrade` and `upgrade` functions in newly created revision py file. Then, example: `alembic upgrade 3c3edfa93236`
    * `alembic downgrade <revision #>`
        * Example: `alembic downgrade -1` (if it's the first, else, -1 will be another `down_revision`)
* Actually, we don't need the `Address` class in the `address.py` since it has been created by alembic operations but just in case we need it (if we change our DB or somethig), we created it.
* Remember: We always fill the `downgrade` and `upgrade` functions.
* Remember the connect `ForeignKeys` correctly.
* I edited the alembic with the command `alembic edit <revision #>` then had to downgrade and upgrade again.
## 4. Project 4: Full Stack Application
### 4.1 Jinja Introduction
* We have created a `home.html` file.
* `pip3 install aiofiles jinja2`
* `templates = Jinja2Templates(directory="templates")`
* return the template respons under an endpoint:
```python
return templates.TemplateResponse(
        name="home.html",
        context={
            "request": request
        }
    )
```
### 4.2 Static & CSS
* Foldering:
    * `static`
        * `todo`
            * `js`
            * `css`
                * `base.css`
* Import to `main.py` file: `from starlette.staticfiles import StaticFiles`
* Then we `mount` it to our app in `main.py` file.
* After this, we import our css in the `base.html` file (the `<link ...>` line).
    * `"{{ url_for('static', path='/todo/css/base.css')}}"` this code is **Jinja** specific.
### 4.3 Adding CSS & JS to Static Files
* I copied these files (the instructor's advice), didn't touch them:
    * **css** folder: `base.css` (mine is overwritten), `bootstrap.css` (we include this to our project to avoid version changes in bootstrap).
    * **js** folder: `bootstrap.js`, `jquery-slim.js`, `popper.js` (these are required for bootstrap to render js.)
* bootstrap is a framework that allows us to deal with css and js easily. It has prebuild components.
* I didn't copy the templates. I'll code along with the instructor.
### 4.4 Jinja Templating Overview
* **Jinja:** Fast, expressive and extensible templating language. Able to write code similar to Python in the DOM _(The HTML DOM is a standard object model and programming interface for HTML. It defines: The HTML elements as objects. The properties of all HTML elements. The methods to access all HTML elements)._ The template is passed data to render within the final document. 
* Jinja templating and scripts:
    * In the `todos.py`, we can define the todos and pass the entire list of todos into the front-end.
    ```python
    context: {
        "todos": "todo_list"
    }
    ```
    * And in the DOM, we loop through the list in the html file:
    ```jinja
    {% for todo in todos %}
        Do something with todo
    {% endfor %}
    ```
    * We can also use Jinja templating language with if/else statements:
    ```jinja
    {% if todos %}
        Displaying: {{ todos|length }} Todos
    {% else %}
        You don't have any todos.
    {% endif %}
    ```
    * `{% ... %}`: Control flow, loops or logic
    * `{ ... }`: specific variable
### 4.5 HTML Parts
* bootstrap specific line in the `home.html`: `<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">`
* The `<script ...>` orders matter!
* The `required` parameter in the `input` and `textarea` tags make sure the boxes won't be empty!
* We deleted unnecessary code and created new endpoints for our templates.
* All the templates have the `link`s and ***css*** with the `navbar` at the top, and `script`s at the bottom. However, if there is a bug in one of them, we need to change each one of these templates. So, it's better to have a parent `layout` file in charge of the navbar, scripts, css etc. in which each html file can inherit. That's why we are going to create a `layout.html` file.
    * We put this in the `layout.html` file just before the `script`s.
        ```jinja
        {% block content %}

        {% endblock %}
        ```
    * Then, we included the `layout.html` file in the others by deleting the unnecessary code already included in the layout except the `container` and writing `{% include 'layout.html' %}` at the top of these templates.
* We also extract the `navbar` **div** out of the `layout.html` and put it in another html file. Thus, in the `layout.html` file, we have to `{% include 'navbar.html' %}` just above the `{% block content %}`.
* We put a loop in `home.html` file as shown above (Section 4.4) and provided the parameters by `{{todo.title}}`.
* We modified the `<form>` to `<form method="POST">` in the `add-todo.html` file. Both endpoints (**GET** and **POST**) will go to the exact address but with a different HTTP request.
* To edit the todo in our endpoint in the `todos.py`, we added `"todo": todo` in the context. Also, we modified `edit-todo.html` file and added a value `"{{todo.title}}"` to the `<input ...>`.
* In the **complete** functionality, we added a if/else block in the `home.html`:
```jinja
                {% for todo in todos %}
                {% if todo.complete == False %}
                <... some html code here for Complete ...>
                {% else %}
                <... some different html code here for Undo ...>
                {% endif %}
                {% endfor %}
```
* To make the todo green on Complete: `<tr class="pointer">` ---> `<tr class="pointer alert alert-success">`
* We modified the `auth.py` and added cookie. Later, changed the `<form ...>` in the `login.html` file to `<form method="POST" action="/auth">`.
## 5. Git: Version Control
* `git init`: Initializes a new, empty repository.
* `git add .`: Adds file from a non-staged area to a staging GIT area.
* `git commit -m "some info here"`: Moves files from staging area to commit.
* `git checkout <commit #>`: Opens up previous commits.
* `git log`: Shows comitted Snapshots.
    * For example, you can find the commit # in these logs, checkout to specific one and create a branch out of it by `git switch -c <branch name>` if you like.
* `git branch <branch name>`: Create a new isolated branch.
* `git checkout branch <branch name>`: Change root to branch selected.
* `git switch <branch name>`: Same but works for the newer versions.
* `git merge <branch name>`: Merges two branches.
* About `HEAD`: In Git, HEAD refers to the currently checked-out branch's latest commit. However, in a detached HEAD state, the HEAD does not point to any branch, but instead points to a specific commit or the remote repository.
* `git remote add origin <url>`: Add a remote repo
* `git push -u origin main`: Pusher your code to the remote repo
## 6. Deploying FastAPI Application
* What is **render**? It's a PaaS. Helps developers build, run and operate apps entirely on cloud.   