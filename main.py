
from typing import Annotated
from fastapi import FastAPI, Form
from helper.readingfiles import readJsonFile, writeJsonFile
from helper.tryenums import ModelName
from requestbody.items_request_body import Items


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}

@app.get("/items")
async def read_items():
    #lets read items.json file and return as response
    json_content = await readJsonFile("items.json")
    return json_content

@app.get("/items/{item_id}")
async def read_items_by_id(item_id: str):
    #lets read items.json file and return the item with the given id
      json_content = await readJsonFile("items.json")
      for item in json_content:
            if item["id"] == item_id:
                return item
            
#lets write an endpoint for post call of items
@app.post("/items")
async def add_items(item: Items):
    #we will read items.json file and append items 
    model_names = [ModelName.alexnet, ModelName.resnet, ModelName.lenet]
    try:
        json_content = await readJsonFile("items.json")
        if item.dict()["model"] not in model_names:
            return {"message": "Model name and item model should be same"}
        json_content.append(item.dict())
        await writeJsonFile("items.json", json_content)
        return {"message": "Item added successfully"}
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}

#lets write an endpoint for put call of items
# this endpoint will update the item with the given id
# if item with the given id is not present, it will return an error message
# if item with the given id is present, it will update the item and return success message
@app.put("/items/{item_id}")
async def update_items(item_id: str, item: Items):
    model_names = [ModelName.alexnet, ModelName.resnet, ModelName.lenet]
    try:
        # Read existing items from the JSON file
        json_content = await readJsonFile("items.json")
        
        # Check if the model is valid
        if item.dict()["model"] not in model_names:
            return {"message": "Model name and item model should be same"}
        
        # Check if the item_id exists in the JSON file
        item_found = False
        for content in json_content:
            if content["id"] == item_id:
                # Update the item details
                content.update(item.dict())
                item_found = True
                break
        
        if not item_found:
            return {"message": "Item with the given id not found"}
        
        # Write updated content back to the JSON file
        await writeJsonFile("items.json", json_content)
        return {"message": "Item updated successfully"}
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}


#lets write an endpoint for adding user with form data as input
@app.post("/users")
async def user_signup(id:Annotated[str, Form()], firstName:Annotated[str, Form()],
                        lastName:Annotated[str, Form()],
                        email:Annotated[str, Form()],
                        phone:Annotated[str, Form()],
                        role:Annotated[str, Form()],
                        isActive:Annotated[bool, Form()],
                        createdAt:Annotated[str, Form()],
                        preferences:Annotated[dict, Form()],
                        #itemsUsed is list of dictionaries
                        itemsUsed:Annotated[list[Items], Form()]):

                        
    try:
        #read existing users from json file
        json_content = await readJsonFile("users.json")
        #create a new user object
        user = {
            "id": id,
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phone": phone,
            "role": role,
            "isActive": isActive,
            "createdAt": createdAt,
            "preferences": preferences,
            "itemsUsed": itemsUsed
        }
        #append the new user object to existing users list
        json_content.append(user)
        #write the updated users list to json file
        await writeJsonFile("users.json", json_content)
        return {"message": "User added successfully"}
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}
    

@app.get("/users")
async def get_users():
    #lets read users.json file to get list of all users
    json_content = await readJsonFile("users.json")
    return json_content

#lets create get all users endpoint with pagination support with the help of query parama
@app.get("/users/all")
async def get_users(skip: int = 0, limit: int = 10):
    json_content = await readJsonFile("users.json")
    return json_content[skip : skip + limit]

    
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    json_content = await readJsonFile("users.json")
    for user in json_content:
        if user["id"]==user_id:
            return user
            

@app.get("/users/userbyname/{user_name}")
async def get_users_by_name(name:str):
    try:
        json_content = await readJsonFile("users.json")
        for user in json_content:
                print("user with name -> ", user["firstName"])
                if user["firstName"]==name:
                    return user
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}
    
@app.get("/getmodels/{model_name}")
async def get_models(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#lets write an endpoint which will show all items bought by a user
@app.get("/users/{user_id}/items")
async def get_all_user_items(user_id : str):
    try:
        user = await get_user_by_id(user_id)
        response_object = user["itemsUsed"]
        #iwant to generate response with only some fields - "itemId", "name", "count", "category", "price", "quantity", "description"

        response_data = []
        for item in response_object:
            response_data.append({
                "itemId": item["id"],
                "name": item["name"],
                "count": item["count"],
                "category": item["category"],
                "price": item["price"],
                "quantity": item["quantity"],
                "description": item["description"]
            })
        return response_data
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}

#lets write an endpoint which will show specific items bought by a user
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_items(user_id: str, item_id: str):
    try:
        user = await get_user_by_id(user_id)
        for item in user["itemsUsed"]:
            if item["itemId"]==item_id:
                return item
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}