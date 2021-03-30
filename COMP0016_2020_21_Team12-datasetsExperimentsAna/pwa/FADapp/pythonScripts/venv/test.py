import requests
import json
import unittest

BASE = "http://127.0.0.1:5000/"

class TestAPI(unittest.TestCase):
    # Test that all FADs are loaded.
    def testALLFadData(self):
        #Arrange
        url = BASE + "AllFADs"
        #Act
        response = requests.get(url)
        #Assert
        assert response.ok

    def testFADIsCorrectlyAdded(self):
        # Test that a FAD with id 4 is added
        #Arrange
        url = BASE + "FAD/4"
        FADData = {"FADId": 4, "Latitude": 4.4, "Longitude": 4.5, "Year": 2020, "Month": 7, "Day": 6}
        #Act
        requests.put(url, FADData)
        response = requests.get(url).json()[0]
        #Assert
        assert response['FADId'] == 4
        assert response['Latitude'] == 4.4
        assert response['Longitude'] == 4.5

    def testInvalidFADIsNotAdded(self):
        # Test that FAD with id 5 doesn't exist.
        url = BASE + "FAD/5"
        expectedResponse = {'message': 'No FAD was found with specified ID.'}
        response = requests.get(url).json()
        assert response == expectedResponse

    def testRealFADDataIsPresent(self):
        # Test response for FAD with id 8.
        url = BASE + "FAD/8"
        fad8File = open('FAD8.json', 'r')
        response = requests.get(url).json()
        assert response == json.load(fad8File)

if __name__ == '__main__':
    unittest.main()


