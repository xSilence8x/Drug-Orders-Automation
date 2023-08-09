import json, csv    

class Data:
    def __init__(self):
        pass
    
    def create_json(self, csv_file):
        """
        Opens CSV file, creates dictionary and exports 
        data as JSON file.
        """
        with open(csv_file, "r") as f:
            lines = csv.reader(f)
            data = [line for line in lines]

        my_data = list()
        for ele in data:
            my_dict = dict()
            my_dict["kod"] = ele[1]
            my_dict["nazev"] = ele[2]
            my_dict["pocet"] = 10
            my_dict["objednat"] = True
            if ele[9] == "":
                my_dict["stav"] = "Dostupný"
            else:
                my_dict["stav"] = ele[9]
            my_data.append(my_dict)

        with open("leky.json", "w") as f:
            leky = json.dumps(my_data, indent=4)
            f.write(leky)
        

    def open_json(self, file):
        """
        Opens JSON file and returns data.
        """
        with open(file, "r") as f:
            data = json.load(f)
        return data
