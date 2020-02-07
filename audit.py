import pandas as pd
import re
import webscrape

##READ CSV FOR NAMES FROM PETPOINT
def read_petpoint_inventory(csv_file):
    inventory = pd.read_csv(csv_file,skiprows=3)
    inventory = inventory[["AnimalName","ARN","Stage"]]
    inventory = inventory.loc[(inventory["Stage"] == "Available") | (inventory["Stage"] == "Available-Hospice")]
    inventory["ARN"] = inventory["ARN"].astype(str)
    return inventory

##COMPARE
###Get dogs in inventory, but not on mv.org
def dogs_to_add(website_inventory, petpoint_inventory):
    available_on_website = website_inventory.loc[website_inventory["Stage"] == "Available"]
    website_arn = list(available_on_website["ARN"])
    available_on_pp = petpoint_inventory.loc[petpoint_inventory["Stage"] == "Available"]
    to_add = available_on_pp[~available_on_pp["ARN"].isin(website_arn)]
    return to_add

def hospice_dogs_to_add(website_inventory, petpoint_inventory):
    hospice_on_website = website_inventory.loc[website_inventory["Stage"] == "Available-Hospice"]
    website_arn = list(hospice_on_website["ARN"])
    hospice_on_pp = petpoint_inventory.loc[petpoint_inventory["Stage"] == "Available-Hospice"]
    to_add = hospice_on_pp[~hospice_on_pp["ARN"].isin(website_arn)]
    return to_add
    
###Get dogs on mv.org and not on inventory
def dogs_to_remove(website_inventory, petpoint_inventory):
    petpoint_arn = list(petpoint_inventory["ARN"])
    to_remove = website_inventory[~website_inventory["ARN"].isin(petpoint_arn)]
    return to_remove[["Name","ARN"]]

def main():
    website_inventory = webscrape.create_website_inventory()
    petpoint_inventory = read_petpoint_inventory("AnimalInventory.csv")
    print("Dogs to make available regular on site:")
    print(dogs_to_add(website_inventory, petpoint_inventory),"\n")
    print("Dogs to make hospice on site:")
    print(hospice_dogs_to_add(website_inventory, petpoint_inventory),"\n")
    print("Dogs to remove from site:")
    print(dogs_to_remove(website_inventory,petpoint_inventory))

if __name__ == "__main__":
    main()

