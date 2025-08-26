
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://clinicaltrials.gov/api/query/study_fields"


params = {
    'expr': 'Johnson',  
    'fields': 'NCTId,BriefTitle,Condition,InterventionName,OverallStatus,StartDate,LocationCity,LocationCountry',
    'min_rnk': 1,
    'max_rnk': 100,
    'fmt': 'json'
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print("Request URL:", response.url)
print("Response snippet:", response.text[:500])

data = response.json()

studies = data['StudyFieldsResponse']['StudyFields']

records = []
for study in studies:
    records.append({
        'NCTId': study.get('NCTId', [''])[0],
        'Title': study.get('BriefTitle', [''])[0],
        'Condition': study.get('Condition', [''])[0],
        'Intervention': study.get('InterventionName', [''])[0],
        'Status': study.get('OverallStatus', [''])[0],
        'StartDate': study.get('StartDate', [''])[0],
    })

df = pd.DataFrame(records)
print(df.head())

df.to_csv("jnj_clinical_trials_api.csv", index=False)

df = pd.read_csv(r"C:\Users\dilek\Desktop\clinical_trial_analysis\data\clinical_trials.csv")


pd.set_option('display.max_columns', None)


print("🔹 First 5 rows:")
print(df.head())


print("\n🔹 Sütunlar ve Türleri:")
print(df.dtypes)


print("\n🔹 Missing Data:")
print(df.isnull().sum())


df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['Start Year'] = df['Start Date'].dt.year


input_path = r"C:\Users\dilek\Desktop\clinical_trial_analysis\data\clinical_trials.csv"


output_path = r"C:\Users\dilek\Desktop\clinical_trial_analysis\data\clinical_trials_cleaned.csv"


df = pd.read_csv(input_path)


def extract_first_city_country(locations_str):
    if pd.isna(locations_str):
        return ("UNKNOWN", "UNKNOWN")

    locations = [loc.strip() for loc in locations_str.split('|')]

    
    for loc in locations:
        parts = [p.strip() for p in loc.split(',')]
        if len(parts) >= 4:
            city = parts[-3]
            country = parts[-1].upper()
            return (city, country)

    return ("UNKNOWN", "UNKNOWN")


df[["City", "Country"]] = df["Locations"].apply(extract_first_city_country).apply(pd.Series)


df.drop(columns=["Locations"], inplace=True)

df.to_csv(output_path, index=False)

print("CSV saved.")

