APIRouter class¶
Here's the reference information for the APIRouter class, with all its parameters, attributes and methods.

You can import the APIRouter class directly from fastapi:


from fastapi import APIRouter
 fastapi.APIRouter ¶

APIRouter(
    *,
    prefix="",
    tags=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    responses=None,
    callbacks=None,
    routes=None,
    redirect_slashes=True,
    default=None,
    dependency_overrides_provider=None,
    route_class=APIRoute,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    deprecated=None,
    include_in_schema=True,
    generate_unique_id_function=Default(generate_unique_id)
)
Bases: Router

APIRouter class, used to group path operations, for example to structure an app in multiple files. It would then be included in the FastAPI app, or in another APIRouter (ultimately included in the app).

Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

Example¶

from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


app.include_router(router)
PARAMETER	DESCRIPTION
prefix	An optional path prefix for the router.
TYPE: strDEFAULT: ''

tags	A list of tags to be applied to all the path operations in this router.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to all the path operations in this router.
Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

default_response_class	The default response class to be used.
Read more in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

responses	Additional responses to be shown in OpenAPI.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Additional Responses in OpenAPI.

And in the FastAPI docs for Bigger Applications.

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

callbacks	OpenAPI callbacks that should apply to all path operations in this router.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

routes	Note: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility.
A list of routes to serve incoming HTTP and WebSocket requests.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

redirect_slashes	Whether to detect and redirect slashes in URLs when the client doesn't use the same format.
TYPE: boolDEFAULT: True

default	Default function handler for this router. Used to handle 404 Not Found errors.
TYPE: Optional[ASGIApp]DEFAULT: None

dependency_overrides_provider	Only used internally by FastAPI to handle dependency overrides.
You shouldn't need to use it. It normally points to the FastAPI app object.

TYPE: Optional[Any]DEFAULT: None

route_class	Custom route (path operation) class to be used by this router.
Read more about it in the FastAPI docs for Custom Request and APIRoute class.

TYPE: Type[APIRoute]DEFAULT: APIRoute

on_startup	A list of startup event handler functions.
You should instead use the lifespan handlers.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Sequence[Callable[[], Any]]]DEFAULT: None

on_shutdown	A list of shutdown event handler functions.
You should instead use the lifespan handlers.

Read more in the FastAPI docs for lifespan.

TYPE: Optional[Sequence[Callable[[], Any]]]DEFAULT: None

lifespan	A Lifespan context manager handler. This replaces startup and shutdown functions with a single context manager.
Read more in the FastAPI docs for lifespan.

TYPE: Optional[Lifespan[Any]]DEFAULT: None

deprecated	Mark all path operations in this router as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[bool]DEFAULT: None

include_in_schema	To include (or not) all the path operations in this router in the generated OpenAPI.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 websocket ¶

websocket(path, name=None, *, dependencies=None)
Decorate a WebSocket function.

Read more about it in the FastAPI docs for WebSockets.

Example

Example¶

from fastapi import APIRouter, FastAPI, WebSocket

app = FastAPI()
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

app.include_router(router)
PARAMETER	DESCRIPTION
path	WebSocket path.
TYPE: str

name	A name for the WebSocket. Only used internally.
TYPE: Optional[str]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be used for this WebSocket.
Read more about it in the FastAPI docs for WebSockets.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

Source code in fastapi/routing.py
 include_router ¶

include_router(
    router,
    *,
    prefix="",
    tags=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    responses=None,
    callbacks=None,
    deprecated=None,
    include_in_schema=True,
    generate_unique_id_function=Default(generate_unique_id)
)
Include another APIRouter in the same current APIRouter.

Read more about it in the FastAPI docs for Bigger Applications.

Example¶

from fastapi import APIRouter, FastAPI

app = FastAPI()
internal_router = APIRouter()
users_router = APIRouter()

@users_router.get("/users/")
def read_users():
    return [{"name": "Rick"}, {"name": "Morty"}]

internal_router.include_router(users_router)
app.include_router(internal_router)
PARAMETER	DESCRIPTION
router	The APIRouter to include.
TYPE: APIRouter

prefix	An optional path prefix for the router.
TYPE: strDEFAULT: ''

tags	A list of tags to be applied to all the path operations in this router.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to all the path operations in this router.
Read more about it in the FastAPI docs for Bigger Applications - Multiple Files.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

default_response_class	The default response class to be used.
Read more in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

responses	Additional responses to be shown in OpenAPI.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Additional Responses in OpenAPI.

And in the FastAPI docs for Bigger Applications.

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

callbacks	OpenAPI callbacks that should apply to all path operations in this router.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

deprecated	Mark all path operations in this router as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[bool]DEFAULT: None

include_in_schema	Include (or not) all the path operations in this router in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

TYPE: boolDEFAULT: True

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 get ¶

get(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP GET operation.

Example¶

from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/items/")
def read_items():
    return [{"name": "Empanada"}, {"name": "Arepa"}]

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 put ¶

put(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP PUT operation.

Example¶

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.put("/items/{item_id}")
def replace_item(item_id: str, item: Item):
    return {"message": "Item replaced", "id": item_id}

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 post ¶

post(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP POST operation.

Example¶

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return {"message": "Item created"}

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 delete ¶

delete(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP DELETE operation.

Example¶

from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.delete("/items/{item_id}")
def delete_item(item_id: str):
    return {"message": "Item deleted"}

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 options ¶

options(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP OPTIONS operation.

Example¶

from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.options("/items/")
def get_item_options():
    return {"additions": ["Aji", "Guacamole"]}

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 head ¶

head(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP HEAD operation.

Example¶

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.head("/items/", status_code=204)
def get_items_headers(response: Response):
    response.headers["X-Cat-Dog"] = "Alone in the world"

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 patch ¶

patch(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP PATCH operation.

Example¶

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.patch("/items/")
def update_item(item: Item):
    return {"message": "Item updated in place"}

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 trace ¶

trace(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
Add a path operation using an HTTP TRACE operation.

Example¶

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.trace("/items/{item_id}")
def trace_item(item_id: str):
    return None

app.include_router(router)
PARAMETER	DESCRIPTION
path	The URL path to be used for this path operation.
For example, in http://example.com/items, the path is /items.

TYPE: str

response_model	The type to use for the response.
It could be any valid Pydantic field type. So, it doesn't have to be a Pydantic model, it could be other things, like a list, dict, etc.

It will be used for:

Documentation: the generated OpenAPI (and the UI at /docs) will show it as the response (JSON Schema).
Serialization: you could return an arbitrary object and the response_model would be used to serialize that object into the corresponding JSON.
Filtering: the JSON sent to the client will only contain the data (fields) defined in the response_model. If you returned an object that contains an attribute password but the response_model does not include that field, the JSON sent to the client would not have that password.
Validation: whatever you return will be serialized with the response_model, converting any data as necessary to generate the corresponding JSON. But if the data in the object returned is not valid, that would mean a violation of the contract with the client, so it's an error from the API developer. So, FastAPI will raise an error and return a 500 error code (Internal Server Error).
Read more about it in the FastAPI docs for Response Model.

TYPE: AnyDEFAULT: Default(None)

status_code	The default status code to be used for the response.
You could override the status code by returning a response directly.

Read more about it in the FastAPI docs for Response Status Code.

TYPE: Optional[int]DEFAULT: None

tags	A list of tags to be applied to the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[List[Union[str, Enum]]]DEFAULT: None

dependencies	A list of dependencies (using Depends()) to be applied to the path operation.
Read more about it in the FastAPI docs for Dependencies in path operation decorators.

TYPE: Optional[Sequence[Depends]]DEFAULT: None

summary	A summary for the path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

description	A description for the path operation.
If not provided, it will be extracted automatically from the docstring of the path operation function.

It can contain Markdown.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Path Operation Configuration.

TYPE: Optional[str]DEFAULT: None

response_description	The description for the default response.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: strDEFAULT: 'Successful Response'

responses	Additional responses that could be returned by this path operation.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[Dict[Union[int, str], Dict[str, Any]]]DEFAULT: None

deprecated	Mark this path operation as deprecated.
It will be added to the generated OpenAPI (e.g. visible at /docs).

TYPE: Optional[bool]DEFAULT: None

operation_id	Custom operation ID to be used by this path operation.
By default, it is generated automatically.

If you provide a custom operation ID, you need to make sure it is unique for the whole API.

You can customize the operation ID generation with the parameter generate_unique_id_function in the FastAPI class.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Optional[str]DEFAULT: None

response_model_include	Configuration passed to Pydantic to include only certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_exclude	Configuration passed to Pydantic to exclude certain fields in the response data.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: Optional[IncEx]DEFAULT: None

response_model_by_alias	Configuration passed to Pydantic to define if the response model should be serialized by alias when an alias is used.
Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: True

response_model_exclude_unset	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that were not set and have their default values. This is different from response_model_exclude_defaults in that if the fields are set, they will be included in the response, even if the value is the same as the default.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_defaults	Configuration passed to Pydantic to define if the response data should have all the fields, including the ones that have the same value as the default. This is different from response_model_exclude_unset in that if the fields are set but contain the same default values, they will be excluded from the response.
When True, default values are omitted from the response.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

response_model_exclude_none	Configuration passed to Pydantic to define if the response data should exclude fields set to None.
This is much simpler (less smart) than response_model_exclude_unset and response_model_exclude_defaults. You probably want to use one of those two instead of this one, as those allow returning None values when it makes sense.

Read more about it in the FastAPI docs for Response Model - Return Type.

TYPE: boolDEFAULT: False

include_in_schema	Include this path operation in the generated OpenAPI schema.
This affects the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for Query Parameters and String Validations.

TYPE: boolDEFAULT: True

response_class	Response class to be used for this path operation.
This will not be used if you return a response directly.

Read more about it in the FastAPI docs for Custom Response - HTML, Stream, File, others.

TYPE: Type[Response]DEFAULT: Default(JSONResponse)

name	Name for this path operation. Only used internally.
TYPE: Optional[str]DEFAULT: None

callbacks	List of path operations that will be used as OpenAPI callbacks.
This is only for OpenAPI documentation, the callbacks won't be used directly.

It will be added to the generated OpenAPI (e.g. visible at /docs).

Read more about it in the FastAPI docs for OpenAPI Callbacks.

TYPE: Optional[List[BaseRoute]]DEFAULT: None

openapi_extra	Extra metadata to be included in the OpenAPI schema for this path operation.
Read more about it in the FastAPI docs for Path Operation Advanced Configuration.

TYPE: Optional[Dict[str, Any]]DEFAULT: None

generate_unique_id_function	Customize the function used to generate unique IDs for the path operations shown in the generated OpenAPI.
This is particularly useful when automatically generating clients or SDKs for your API.

Read more about it in the FastAPI docs about how to Generate Clients.

TYPE: Callable[[APIRoute], str]DEFAULT: Default(generate_unique_id)

Source code in fastapi/routing.py
 on_event ¶

on_event(event_type)
Add an event handler for the router.

on_event is deprecated, use lifespan event handlers instead.

Read more about it in the FastAPI docs for Lifespan Events.

PARAMETER	DESCRIPTION
event_type	The type of event. startup or shutdown.
TYPE: str

