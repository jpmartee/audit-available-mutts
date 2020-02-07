import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup

##Function to determine Hospice
def get_available_stage(description):
    if "Hospice" in description:
        return "Available-Hospice"
    else:
        return "Available"

##GET NAMES FROM MV.ORG
def get_mv_mutts():
    url_temp = "https://muttville.org/available_mutts?page="
    mutt_list = list()
    for i in range(1,11):
        try:
            url = url_temp + str(i)
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            mutts = soup.findChildren("article")
            for mutt in mutts:
                name = mutt.h2.text
                stage = get_available_stage(mutt.p.text)
                if "&" in name:
                    for i in name.split("&"):
                        mutt_col = list()
                        mutt_col.append(i.strip())
                        mutt_col.append(stage)
                        mutt_list.append(mutt_col)
                else:
                    mutt_col = list()
                    mutt_col.append(name)
                    mutt_col.append(stage)
                    mutt_list.append(mutt_col)
        except:
            break
    return pd.DataFrame(mutt_list,columns=["Mutt","Stage"])

def get_arn(mutt):
    pattern = r'\d{3,}$'
    result = re.search(pattern, mutt)
    try:
        arn = result.group(0)
        return arn
    except:
        return mutt

def get_name(mutt):
    pattern = r'\d{3,}$'
    name = re.sub(pattern,"",mutt)
    return name

def create_website_inventory():
    df = get_mv_mutts()
    df["Name"] = df["Mutt"].apply(get_name)
    df["ARN"] = df["Mutt"].apply(get_arn)
    return df

if __name__ == "__main__":
    pass