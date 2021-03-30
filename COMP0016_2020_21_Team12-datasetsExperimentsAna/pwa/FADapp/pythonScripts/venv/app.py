from pathlib import Path, PurePosixPath
from flask_restful import Api, Resource, reqparse, abort, fields, marshal
import getFADsTableStorage
from flask_cors import CORS

from flask import Flask, jsonify
app = Flask(__name__)
CORS(app)

def getLatitudeAndLongitudeForBorder():
    filePath = "data/StLuciaCoords.txt"
    f = open(filePath, "r")
    border = []
    while True:
        crtLine = f.readline()
        if not crtLine:
            break
        crtLine = crtLine.split()
        border.append({"longitude":crtLine[0], "latitude": crtLine[1]})
    return border

@app.route('/AllFADs')
def getAllFADData():
    return jsonify(getFADsTableStorage.getAllFADs())

@app.route('/StLuciaBorder')
def index():
    border = getLatitudeAndLongitudeForBorder()
    return jsonify(border)

def abortFADIfIdDoesntExist(fadId):
    if getFADsTableStorage.findFadById(fadId) == None:
        abort(404, message = "No FAD was found with specified ID.")

def abortFADIfIdAlreadyExists(fadId):
    if getFADsTableStorage.findFadById(fadId) != None:
        abort(409, message = "FAD with given ID already exists!")

def namespaceToDict(args):
    return {"FADId": args["FADId"],
            "Latitude": args["Latitude"],
            "Longitude": args["Longitude"]}

class FAD(Resource):
    def get(self, fadId):
        abortFADIfIdDoesntExist(fadId)
        return getFADsTableStorage.findFadById(fadId)
    def put(self, fadId):
        abortFADIfIdAlreadyExists(fadId)
        args = fadPutArgs.parse_args()
        getFADsTableStorage.addFAD(namespaceToDict(args))

def createFADFields():
    mfields = {'FADId': fields.Integer,
               "Latitude": fields.Float,
               "Longitude": fields.Float}
    return mfields

def createFadRequestParser():
    fadPutArgs = reqparse.RequestParser()
    fadPutArgs = fadPutArgs.add_argument("FADId", type=int, help = "The identifier of FAD")
    fadPutArgs = fadPutArgs.add_argument("Latitude", type=float, help="The latitude of FAD")
    fadPutArgs = fadPutArgs.add_argument("Longitude", type=float, help="The longitude of FAD")

    return fadPutArgs


api = Api(app)
api.add_resource(FAD, "/FAD/<int:fadId>")
fadPutArgs = createFadRequestParser()
mfields = createFADFields()
getFADsTableStorage.setFADData()
if __name__ == "__main__":
    app.run(host="0.0.0.0")
