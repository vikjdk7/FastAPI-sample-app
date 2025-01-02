import json

async def readJsonFile(file_name):
    try:
        with open(file_name, "r") as file:
            file_content = file.read()
            json_content = json.loads(file_content)
            return json_content
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}
    
async def writeJsonFile(file_name, data):
    try:
        with open(file_name, "w") as file:
            json.dump(data, file)
            return {"message": "Data written successfully"}
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}