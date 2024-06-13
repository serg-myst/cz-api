from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from operations.router import router_marks, router_auth

app = FastAPI(title='CZ API')

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', include_in_schema=False)
async def welcome():
    return {
        'status': 200,
        'details': 'welcome to our api. Read the instructions and go ahead',
        'data': []
    }


app.include_router(router_marks)
app.include_router(router_auth)