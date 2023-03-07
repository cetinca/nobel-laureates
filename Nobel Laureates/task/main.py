import os

import matplotlib.pyplot as plt
import pandas as pd
import requests

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        print('Nobel_laureates.json')
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        with open('../Data/Nobel_laureates.json', 'wb') as f:
            f.write(r.content)
        print('Loaded.')
    df = pd.read_json('../Data/Nobel_laureates.json')

    # write your code here

    """Stage 1"""

    # df.info()

    # check for duplicated rows
    # print(df.duplicated().any())

    # drop rows where gender is None
    index_ = df[df["gender"].isnull()].index
    df.drop(index_, inplace=True)

    # reset index
    df.reset_index(drop=True, inplace=True)

    # print first 20 rows
    # print(df[['name', 'country']].head(20).to_dict())

    """Stage 2"""

    # replace place of birth with country name
    df["place_of_birth"] = df["place_of_birth"].apply(lambda x: x.split(',')[-1].strip() if x and ',' in x else None)
    df["born_in"] = df[["place_of_birth", "born_in"]].apply(
        lambda row: row["place_of_birth"] if not row["born_in"] else row["born_in"], axis=1)

    # drop null values
    index_ = df[df["born_in"].isnull()].index
    df.drop(index_, inplace=True)

    # Fix issues in USA and UK
    df["born_in"] = df["born_in"].apply(lambda x: "USA" if x in ["US", "United States", "U.S."] else x)
    df["born_in"] = df["born_in"].apply(lambda x: "UK" if x in ["United Kingdom"] else x)

    # print(df["born_in"].to_list())

    """Stage 3"""

    # Extract the year of birth
    df["year_born"] = df["date_of_birth"].apply(lambda x: int(x[:4]) if "-" in x else int(x[-4:]))
    # Calculate age of winning
    df["age_of_winning"] = df["year"] - df["year_born"]

    # print(df["year_born"].to_list())
    # print(df["age_of_winning"].to_list())

    """Stage 4"""

    country_count = df.groupby("born_in")["born_in"].aggregate("count")
    countries_filtered = country_count[lambda x: x < 25]
    countries_filtered_set = (set(countries_filtered.index))

    df["born_in"] = df["born_in"].apply(lambda x: "Other countries" if x in countries_filtered_set else x)
    # print(list(df["born_in"]))

    # After filtering find count by country
    countries = df.groupby("born_in")["born_in"].aggregate("count").sort_values(ascending=False)
    # plt.figure(figsize=(12, 12))
    # # print(countries)
    # plt.pie(
    #     x=countries.values,
    #     labels=countries.index,
    #     colors=["blue", "orange", "red", "yellow", "green", "pink", "brown", "cyan", "purple"],
    #     autopct=lambda p: f'{p:.2f}%\n({p * sum(countries.values) / 100:.0f})',
    #     counterclock=True,
    #     explode=[0, 0, 0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    # )
    # plt.show()

    """Stage 5"""

    index_ = df[df["category"] == ""].index
    df.drop(index_, inplace=True)

    categories = sorted(df["category"].unique())
    #
    # # count_by_category = df[df["gender" == "male"]].groupby(["category", "gender"])["gender"].aggregate("count")
    # count_by_category_male = df[df["gender"] == "male"].groupby("category")["category"].aggregate("count")
    # count_by_category_female = df[df["gender"] == "female"].groupby("category")["category"].aggregate("count")
    #
    # # Data to plot
    # males, females = [], []
    # for category in categories:
    #     males.append(count_by_category_male.get(category, 0))
    #     females.append(count_by_category_female.get(category, 0))
    #
    # # create plot
    # plt.figure(figsize=(10, 10))
    # index = np.arange(len(categories))
    # bar_width = 0.4
    # opacity = 0.8
    #
    # # First group
    # plt.bar(index, males, bar_width,
    #                  alpha=opacity,
    #                  color='blue',
    #                  label='Males')
    #
    # # Second group
    # plt.bar(index + bar_width, females, bar_width,
    #                  alpha=opacity,
    #                  color='orange',
    #                  label='Females')
    #
    # plt.xlabel('Category', fontsize=14)
    # plt.ylabel('Nobel Laureates Count', fontsize=14)
    # plt.title('The total count of male and female Nobel Prize winners in each category', fontsize=20)
    # plt.xticks(index + bar_width, categories)
    # plt.yticks(np.arange(0, 201, 25))
    # plt.legend()
    #
    # plt.tight_layout()
    # plt.show()

    """Stage 6"""

    all_data = dict()
    for category in categories:
        data = df["age_of_winning"][df["category"] == category].tolist()
        all_data.update({category: data})

    # fig, ax = plt.subplots()
    # ax.boxplot(all_data.values(), )
    # ax.set_xticklabels(all_data.keys())
    # plt.show()

    # MultipleBoxplot
    plt.boxplot(
        all_data.values(),
        vert=True,
        patch_artist=True,
        labels=all_data.keys(),
        showmeans=True,
    )
    plt.xlabel('Category')
    plt.ylabel('Age of Obtaining The Nobel Prize')
    plt.title('The total count of Nobel Prize winners in each category')
    plt.show()
