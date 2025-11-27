import json
import pandas as pd
import matplotlib.pyplot as plt


# Load your file here
with open("agent/toy_corpus.json", "r") as f:
    corpus = json.load(f)


records = []
for item in corpus["data"]:
    attr = item["attributes"]
    records.append({
        "species": attr["animalSpecies"],
        "sex": attr["animalSex"],
        "age": attr["animalAgeString"]
    })

df = pd.DataFrame(records)


summary = (
    df.groupby("species")
      .agg(
          count=("species", "count"),
          pct_of_total=("species", lambda x: 100 * len(x)/len(df)),
          female=("sex", lambda x: (x=="Female").sum()),
          male=("sex", lambda x: (x=="Male").sum()),
      )
      .sort_values("count", ascending=False)
)

summary["pct_of_total"] = summary["pct_of_total"].round(2)

print("\n=== SUMMARY TABLE ===\n")
print(summary)

plt.figure(figsize=(8,4))
df["species"].value_counts().plot(kind="bar", color="steelblue")
plt.title("Number of Animals by Species")
plt.xlabel("Species")
plt.ylabel("Count")
plt.tight_layout()
plt.show()


age_order = ["Baby", "Young", "Adult", "Senior"]

plt.figure(figsize=(8,4))
df["age"].value_counts().reindex(age_order).plot(kind="bar", color="darkorange")
plt.title("Number of Animals by Age Category")
plt.xlabel("Age Category")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
